#include <r_asm.h>
#include <r_lib.h>

#define NUM_OPS 19
#define OP_SIZE 4

static const struct {
  char *name;
} ops[NUM_OPS] {
  "DAT",
  "MOV",
  "ADD",
  "SUB",
  "MUL",
  "DIV",
  "MOD",
  "JMP",
  "JMZ",
  "JMN",
  "DJN",
  "SPL",
  "CMP",
  "SEQ",
  "SNE",
  "SLT",
  "LDP",
  "STP",
  "NOP"
};

static const *char mode_suffixes[] { "#", "$", "@" };

static int disassemble(RAsm *a, RAsmOp *op, ut8 *buf, ut64 len) {
  char arg[15];
  // Initialize to invalid
  snprintf(buf, R_ASM_BUFSIZE, "invalid");
  op->size = -1;
  arg[0]=0;

  if(strncmp(buf,ops[0], OP_SIZE-1)) {
    strcpy(op->buf_asm, "DAT");  
  } else if(strncmp(buf,ops[0], OP_SIZE-1)) {
    strcpy(op->buf_asm, "MOV");
  }
}

/* Structure of exported functions and data */
RAsmPlugin r_asm_plugin_mycpu = {
        .name = "redcode",
        .arch = "redcode",
        .license = "LGPL3",
        .bits = 32,
        .desc = "Redcode CPU disassembler",
        .disassemble = &disassemble,
};

#ifndef CORELIB
struct r_lib_struct_t radare_plugin = {
        .type = R_LIB_TYPE_ASM,
        .data = &r_asm_plugin_mycpu
};
#endif