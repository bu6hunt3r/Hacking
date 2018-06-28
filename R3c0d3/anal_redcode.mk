OBJ_REDCODE = anal_redcode.o

STATIC_OBJ+=(OBJ_REDCODE)
TARGET_REDCODE=anal_redcode.$(EXT_SO)

ALL_TARGETS+=$(TARGET_REDCODE

$(TARGET_REDCODE): $(OBJ_REDCODE)
	$(CC) $(call libname,anal_redcode) ${LDFLAGS} ${CFLAGS} -o anal_redcode.$(EXT_SO) $(OBJ_REDCODE)
