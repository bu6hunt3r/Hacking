from copy import copy

from rca2 import redcode_compile
from common2 import Program, Instruction, DATInstruction, DATException
import random
import struct

VERBOSE = False

signedHex = lambda n: n & (0x7fffffff) | -(n & 0x80000000)

is_square = lambda x: x**0.5 == int(x**0.5)

class Warrior:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.alive = True


class RelativeCore:
    def __init__(self, offset, core):
        self._offset = offset
        self._core = core
        self._len = len(core)

    def read(self, val, mode='#'):
        if mode == '#':
            return val

        elif mode == '$':
            #return self[val]
            #print "b-field (repr):", repr(self[val].to_bytecode()[8:12])
            #print "b-Field (num): ",signedHex(struct.unpack("<I", self[val].to_bytecode()[8:12])[0])
            return signedHex(struct.unpack("<I", self[val].to_bytecode()[8:12])[0])
            i#return self[val].to_bytecode()

        elif mode == '@':
            ptr = self[val]
            return self[ptr]

    def write(self, addr, instruction, mode='#'):
        if mode == '#':
            return
        elif mode == '$':
            self[addr] = copy(instruction)
        elif mode == '$':
            ptr_b = self[addr]
            self[ptr_b] = copy(instruction)

    def write_b_field(self, addr, field_val, mode='#'):
        if mode == '#':
            return
        elif mode == '$':
            self[addr].b = field_val
        elif mode == '$':
            ptr_b = self[addr]
            self[ptr_b].b = field_val

    def __getitem__(self, i):
        #print "offset: {}, i: {}".format(type(self._offset), type(i))
        return self._core[(self._offset + i) % self._len]

    def __setitem__(self, i, v):
        if isinstance(i, slice):
            for j, k in enumerate(range(i.start, i.stop, i.step or 1)):
                self._core[(self._offset + k) % self._len] = v[j]
        else:
            self._core[(self._offset + i) % self._len] = v

    def __len__(self):
        return self._len


class CoreWarVM:
    def __init__(self, size=8000, max_code_size=100):
        self.size = size
        self.max_code_size = max_code_size
        self.core = RelativeCore(0, [DATInstruction()] * size)
        self.warriors = []

    def load_warrior(self, name, address, instructions):
        assert len(instructions) < self.max_code_size
        assert address >= 0
        address_end = address + len(instructions)
        assert address_end < self.size
        self.core[address:address_end] = instructions
        self.warriors.append(Warrior(name, address))

    def run(self, steps):
        for _ in range(steps):
            for warrior in self.warriors:
                if not warrior.alive:
                    continue
                try:
                    instruction = self.core[warrior.address]
                    if VERBOSE:
                        print('0x%x ==> %s' % (warrior.address, instruction))
                    jmp = instruction.execute(RelativeCore(warrior.address, self.core))
                    if VERBOSE:
                        for i in range(4):
                            print('0x%x -- %s' % (warrior.address + i, self.core[warrior.address + i]))
                    if jmp:
                        warrior.address += jmp
                    else:
                        warrior.address += 1
                except DATException:
                    print('%s has been killed !' % warrior.name)
                    warrior.alive = False
                    alives = [w for w in self.warriors if w.alive]
                    if len(alives) == 1:
                        return alives[0]
                    elif len(alives) == 0:
                        raise RuntimeError('All warrior have died !')

class GridArray:
    def __init__(self, size):
        assert is_square(size)
        self.rows, self.cols = int(size**0.5), int(size**0.5)
        print "rows: {}, cols: {}".format(self.rows,self.cols)
        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Corewar VM.')
    parser.add_argument('infiles', type=argparse.FileType('rb'),
                        nargs='+', help='code files to run')
    parser.add_argument('-s', '--size', type=int, default=80000,
                        help="VM's memory size")
    parser.add_argument('-r', '--max-steps', type=int,
                        help="Run the VM for a number of steps.")
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    VERBOSE = args.verbose
    address = 0
    max_code_size = int(args.size / len(args.infiles))
    vm = CoreWarVM(size=args.size, max_code_size=max_code_size)

    print "Generating grid array..."
    g=GridArray(int(args.size))

    print "rows: {}, cols: {}".format(g.rows, g.cols)

    #r1=random.sample(list(args.infiles), 1)
    #print "r1 = {}".format(r1)
    w={}
    for idx, item in enumerate(args.infiles):
        w[idx] = item
        #print w
    j = random.randrange(2)
    #print "j : {}".format(j)
    s1=w[j]
    k=[0, 1]
    k.remove(j)
    s2=w[k[0]]

    print "\033[1;31m{} vs. {}\033[0m".format(s1.name.split(".")[0], s2.name.split(".")[0])

    #for i, infile in enumerate(args.infiles):
    for i, infile in enumerate((s1, s2)):
        if infile.name.endswith('.rc'):
            # Compile the file
            print('Compiling %s' % infile.name)
            program = redcode_compile(infile.read().decode())
        elif infile.name.endswith('.rco'):
            program = Program.from_bytecode(infile.read())
        else:
            raise RuntimeError("Code file should be a .rc or a .rco, exiting...")
        name = infile.name.rsplit('/', 1)[-1].rsplit('.', 1)[0] + '-%s' % i
        print('\033[1;32m\xE2\x9C\x94 Loading %s (%s) at 0x%x\033[0m' % (name, infile.name, address))
        vm.load_warrior(name, address, program)
        address += max_code_size

    print('\033[1;32m\xE2\x9C\x94 Starting VM !\033[0m')
    if args.max_steps:
        winner = vm.run(args.max_steps)
    else:
        while True:
            winner = vm.run(8000)
            if winner:
                break
    if winner:
        print("%s have won !" % winner.name)
    else:
        print("Warriors still alive:")
        for warrior in vm.warriors:
            print(' - %s' % warrior.name)
