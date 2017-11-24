ASM = nasm
LD = ld
SRCS = $(basename $(notdir $(wildcard *.asm)))

all: $(SRCS).o
	ld -m elf_x86_64 $(SRCS).o -o $(SRCS)
%.o: %.asm
	nasm -f elf64 $(SRCS).asm -o $(SRCS).o

list:
	ls $(objects)
