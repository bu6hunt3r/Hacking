ASM = nasm
LD = ld
SRCS = $(basename $(notdir $(wildcard *.asm)))

all: $(SRCS).o
	ld -m elf_x86_64 $(SRCS).o -o $(SRCS)
%.o: %.asm
	nasm -f elf64 $(SRCS).asm -o $(SRCS).o

hex: 
	@echo "Size of shellcode:"
	@size $(SRCS)
	@echo ""
	@echo "Shellcode:"
	@objdump -d ./$(SRCS)|grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:| \
	cut -f1-7 -d' '|tr -s ' '|tr '\t' ' '|sed "s| $$||g" |sed "s/ /\\\\x/g"| \
	paste -d '' -s | sed "s|^|\"|" | sed "s|$$|\"|g" > $(SRCS).txt
	@cat $(SRCS).txt

.PHONY:
list:
	ls $(objects)

clean:
	ls | grep -vE "(.*\.asm|.*\.o|.*.txt|Make.*)" | xargs rm
