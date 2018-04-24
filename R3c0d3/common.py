import struct

BYTECODE_INSTRUCTION_SIZE = 14

class DATException:
    pass

class Program(list):

    def to_bytecode(self):
        return b"".join([instruction.to_bytecode() for instruction in self])

    @staticmethod
    def from_bytecode(bytecode):
        program=Program()
        start=0
        size=len(bytecode)
        assert not size % BYTECODE_INSTRUCTION_SIZE
        while start < size:
            end=start+BYTECODE_INSTRUCTION_SIZE
            program.append(Instruction.from_bytecode(bytecode[start:end]))
            start = end
        return program

class Instruction:
     __slots__ = ('name', 'a', 'b', 'amode', 'bmode')
     CODE = None

     @staticmethod
     def from_bytecode(bytecode):
         code = bytecode[:3]
         a, b, amode, bmode = struct.unpack('iicc', bytecode[4:])
         return INSTRUCTION_MAP[code](a, b, amode.decode(), bmode.decode())

     def __init__(self, a=0, b=0, amode='$', bmode='$'):
        assert isinstance(a, int)
        assert isinstance(b, int)
        assert amode in ('#', '@', '$')
        assert bmode in ('#', '@', '$')

        self.a = a
        self.b = b
        self.amode = amode
        self.bmode = bmode

     def to_bytecode(self):
        return (
            self.CODE + b"\x00" + 
            struct.pack("i", self.a) +
            struct.pack("i", self.b) +
            struct.pack("c", self.amode.encode()) +
            struct.pack("c", self.bmode.encode())
        )

     def __repr__(self):
        return ("<{self.CODE} Instruction object(a={self.a}, b={self.b},),"
                "amode={self.amode}, bmode={self.bmode}>".format(self=self))

     #def execute(self, core):
     #   raise NotImplemented

class ADDInstruction(Instruction):
    CODE=b'ADD'
    def show_opcode(self):
        print "In show_opcode"
        return self.__repr__()

    def execute(self, core):
        aval=core.read(self.a, self.amode)
        bval=core.read(self.b, self.bmode)
        print "\033[1;31m aval={}, bval={}\033[0m".format(aval, bval)
        core.write_b_field(self.b, aval+bval, self.bmode)


class MOVInstruction(Instruction):
    CODE=b'MOV'
    def show_opcode(self):
        print "In show_opcode"
        return self.__repr__()

    def execute(self, core):
        val = core.read(self.a, self.amode)
        core.write(self.b, val, self.bmode)

class JMPInstruction(Instruction):
    CODE=b'JMP'

    def execute(self, core):
        return core.read(self.a, self.amode)

class CMPInstruction(Instruction):
    CODE=b"CMP"

    def execute(self, core):
        aval=core.read(self.a, self.amode)
        bval=core.read(self.b, self.bmode)
        return 2 if aval == bval else 1

class SLTInstruction(Instruction):
    CODE=b"SLT"

    def execute(self, core):
        aval=core.read(self.a, self.amode)
        bval=core.read(self.b, self.bmode)
        return 2 if aval < bval else 1
    
class DATInstruction(Instruction):
    CODE=b"DAT"

    def execute(self, core):
        raise DATException()

INSTRUCTION_MAP = {i.CODE: i for i in (MOVInstruction, ADDInstruction, JMPInstruction, CMPInstruction, SLTInstruction, DATInstruction)}
