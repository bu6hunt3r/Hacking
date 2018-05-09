#include <r_asm.h>
#include <r_lib.h>
#include <r_types.h>

static int disassemble(RAsm *a, RAsmOp *op, const ut8 *buf, int len) {

    snprintf(op->buf_asm, R_ASM_BUFSIZE, "invalid");

    ut8 opcode_s[4];
    opcode_s[0]=buf[3];
    opcode_s[1]=buf[2];
    opcode_s[2]=buf[1];
    opcode_s[3]=buf[0];

    ut32 opcode=*(ut32*)opcode_s;

    ut8 f_op_s[4];
    f_op_s[0]=buf[4];
    f_op_s[1]=buf[5];
    f_op_s[2]=buf[6];
    f_op_s[3]=buf[7];

    ut32 f_op=*(ut32*)f_op_s;

    ut8 s_op_s[4];
    s_op_s[0]=buf[8];
    s_op_s[1]=buf[9];
    s_op_s[2]=buf[10];
    s_op_s[3]=buf[11];

    ut32 s_op=*(ut32*)s_op_s;

    ut8 mode_f = buf[12];
    ut8 mode_s = buf[13];
    
    switch(opcode) {
        case 0x4d4f5600:
<<<<<<< HEAD
            snprintf(op->buf_asm, R_ASM_BUFSIZE, "MOV %c%u, %c%u", mode_f, f_op, mode_s, s_op);
=======
            snprintf(op->buf_asm, R_ASM_BUFSIZE, "MOV %c%d, %c%d", mode_f,  f_op, mode_s, s_op);
>>>>>>> dced1729be60361e21ce8b72de57b715d08a5d3c
            op->size=14;
            return 14;

        case 0x44415400:
<<<<<<< HEAD
            snprintf(op->buf_asm, R_ASM_BUFSIZE, "DAT %c%u, %c%u", mode_f, f_op, mode_s, s_op);
=======
            snprintf(op->buf_asm, R_ASM_BUFSIZE, "DAT %c%d, %c%d", mode_f, f_op, mode_s, s_op);
>>>>>>> dced1729be60361e21ce8b72de57b715d08a5d3c
            op->size=14;
            return 14;
    };
}

RAsmPlugin r_asm_plugin_redcode = {
    .name="redcode",
    .author="bu6hunt3r@web.de",
    .arch="redcode",
    .license="none",
    .desc="Redcode disassembler",
    .disassemble=&disassemble,
    .bits=32,
    .modify=NULL,
    .assemble=NULL,
};

#ifndef CORELIB
struct r_lib_struct_t radare_plugin = {
    .type = R_LIB_TYPE_ASM,
    .data = &r_asm_plugin_redcode
}; 
#endif
