#include <stdio.h>
#include <string.h>
#include <r_types.h>
#include <r_lib.h>
#include <r_asm.h>
#include <r_anal.h>



#define Redcode_OP_MOV 1297044992 
// MOV -- move (copies data from one address to another)
#define Redcode_OP_ADD 1094992896
// ADD -- add (adds one number to another)
#define Redcode_OP_JMP 1246580736
// JMP -- jump (continues execution from another address)
#define Redcode_OP_CMP 1129140224
// CMP -- compare (same as SEQ)
#define Redcode_OP_SLT 1397511168
// SLT -- skip if lower than (compares two values, and skips the next instruction if the first is lower than the second)
#define Redcode_OP_DAT 1145132032
// DAT -- data (kills the process)

// Immediate mode
#define IMM_MODE 0x23
// Indirect mode
#define IND_MODE 0x40
// Direct mode
#define DIR_MODE 0x24

static int set_reg_profile(RAnal *anal)  {
    const char *p = 
        "=A0  eax\n"
        "=PC  eip\n"
        "gpr eax .32 0 0\n gpr eip .32 14 0\n";
    return r_reg_set_profile_string(anal->reg, p);
}

static const struct {
  char *name;
} regs[] = {
{"eax"},
{"eip"}
};

static ut32 register_value(const char *reg_name, RAnal *anal) {
    return r_reg_get_value(anal->reg, r_reg_get(anal->reg, reg_name, -1));
}

static int redcode_anal_op(RAnal *anal, RAnalOp *op, ut32 addr, const ut8 *data, int len) {
    ut8 big_end[4];
    big_end[0]=data[3];
    big_end[1]=data[2];
    big_end[2]=data[1];
    big_end[3]=data[0];

    const ut32 op_index = *(ut32*)big_end;

    // Initialize 1st and 2nd operand

    ut8 first_operand[4];
    for (int i=0; i<=3; i++) {
        first_operand[i]=data[i+4];
    }

    const ut32 f_op = *(ut32*)first_operand;

    ut8 second_operand[4];
    for (int j=0; j<=3; j++) {
        second_operand[j]=data[j+8];
    }

    const ut32 s_op = *(ut32*)second_operand;

    // Initialize modes of operands

    ut8 mode_f = data[12];
    ut8 mode_s = data[13];

    // Initialize op to some default values
    memset(op, '\0', sizeof(RAnalOp));

    op->id = op_index;
    op->addr = addr;
    op->size = 14;
    op->nopcode = 1;
    op->jump = -1;
    op->fail = -1;
    op->ptr = -1;
    op->val = -1;
    op->type = R_ANAL_OP_TYPE_UNK;
    op->family = R_ANAL_OP_FAMILY_CPU;

    r_strbuf_init(&op->esil);

    // Some "scratch" registers
    ut32 eax=0x0;
    char *eax_reg = regs[eax].name;

    switch(op_index) {
        case Redcode_OP_ADD:
            eax=register_value(eax_reg, anal);
            switch(mode_f) {
                case IMM_MODE:
                    if(mode_s==IMM_MODE) {
                        eax=f_op+s_op;
                        op->type = R_ANAL_OP_TYPE_ADD;
                        r_strbuf_setf(&op->esil,"%d,%x,=[4],", eax, f_op);
                    }
                    break;
                    
            }
            break;

        case Redcode_OP_DAT:
            // Declare DAT as illegal instruction regardless of operands
            op->type=R_ANAL_OP_TYPE_ILL;
            break;
    }
}

static int esil_redcode_init() {
    return true;
}

static int esil_redcode_fini() {
    return true;
}

RAnalPlugin r_anal_plugin_redcode = {
    .name = "redcode",
    .desc = "redcode analysis plugin",
    .license = "None",
    .arch = "redcode",
    .author = "bu6hunt3r@web.de",
    .bits = 32,
    .esil = true,
    .op = &redcode_anal_op,
    .set_reg_profile = &set_reg_profile,
    .esil_init = esil_redcode_init,
    .esil_fini= esil_redcode_fini,
};

#ifndef CORELIB
struct r_lib_struct_t radare_plugin = {
    .type = R_LIB_TYPE_ANAL,
    .data = &r_anal_plugin_redcode,
    .version = R2_VERSION
};
#endif