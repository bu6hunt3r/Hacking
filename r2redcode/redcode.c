#include <r_asm.h>
#include <r_lib.h>

#define OPS 19

/*
DAT -- data (kills the process)
MOV -- move (copies data from one address to another)
ADD -- add (adds one number to another)
SUB -- subtract (subtracts one number from another)
MUL -- multiply (multiplies one number with another)
DIV -- divide (divides one number with another)
MOD -- modulus (divides one number with another and gives the remainder)
JMP -- jump (continues execution from another address)
JMZ -- jump if zero (tests a number and jumps to an address if it's 0)
JMN -- jump if not zero (tests a number and jumps if it isn't 0)
DJN -- decrement and jump if not zero (decrements a number by one, and jumps unless the result is 0)
SPL -- split (starts a second process at another address)
CMP -- compare (same as SEQ)
SEQ -- skip if equal (compares two instructions, and skips the next instruction if they are equal)
SNE -- skip if not equal (compares two instructions, and skips the next instruction if they aren't equal)
SLT -- skip if lower than (compares two values, and skips the next instruction if the first is lower than the second)
LDP -- load from p-space (loads a number from private storage space)
STP -- save to p-space (saves a number to private storage space)
NOP -- no operation (does nothing)
*/

static const char *ops[OPS*2] = {
	"DAT", NULL,
	"MOV", "ii"
	"ADD", "ii"
	"SUB", "ii",
	"MUL", "ii",
	"DIV", "ii",
	"MOD", "ii",
	"JMP", "i",
	"JMZ", "ii",
	"JMN", "ii",
	"DJN", "ii",
	"SPL", "i",
	"CMP", "ii",
	"SEQ", "ii",
	"SNE", "ii",
	"SLT", "ii",
	"LDP", "i",
	"STP", "i"
	"NOP", NULL
};

/* Main function for disassembly */
//b for byte, l for length

static int disassemble(RAsm *a, RAsmOp *op, const ut8 *b, int l) {
	char arg[32];

	int idx=(b[0]&0xf)*4;
	op->size=4;
	if(idx>=(OPS*2)) {
		strcpy(op->buf_asm, "invalid");
		return -1;
	}
	strcpy(op->buf_asm, ops[idx]);
	if(ops[idx+1]) {
		const char *p=ops[idx+1];
		arg[0]=0;
		if(!strcmp(p,"i")) {
			sprintf(arg, "%d", b[4]&0xffffffff);
		}
		if(!strcmp(p,"ii")) {
			sprintf(arg, "%d, %d", b[4]&0xffffffff, b[8]&0xffffffff);
		}
		if (*arg) {
			strcat (op->buf_asm, " ");
			strcat (op->buf_asm, arg);
		}
	}
	return op->size;
}

/* Structure of exported functions and data */
RAsmPlugin r_asm_plugin_redcode= {
	.name = "redcode",
	.arch = "redcode",
	.license = "LGPL3",
	.bits = 32,
	.desc = "Recode disassembler",
	.disassemble = &disassemble,
};

#ifndef CORELIB
struct r_lib_struct_t radare_plugin = {
	.type = R_LIB_TYPE_ASM,
	.data = &r_asm_plugin_redcode
};
#endif
