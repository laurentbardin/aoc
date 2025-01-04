from dataclasses import dataclass, field

@dataclass
class Register:
    A: int = 0
    B: int = 0
    C: int = 0

@dataclass
class Program:
    instructions: list[int] = field(default_factory=list)
    sp: int = 0
    update_sp: bool = True

    def next(self):
        while self.sp < len(self.instructions) - 1:
            yield self.instructions[self.sp:self.sp+2]
        
            if not self.update_sp:
                #print("Not updating SP")
                self.update_sp = True
            else:
                #print("Update SP")
                self.sp += 2

@dataclass
class VM:
    registers: Register = field(default_factory=Register)
    program: Program = field(default_factory=Program)
    output: list = field(default_factory=list)

    def reset(self, a, b, c, program):
        self.registers = Register(a, b, c)
        self.program = Program([n for n in map(int, program.split(','))])
        self.output = []

    def run(self):
        for opcode, operand in self.program.next():
            opcodes[opcode](operand)

        return self.output

vm = VM()

def combo(fn):
    def wrapper(operand):
        match operand:
            case 4:
                arg = vm.registers.A
            case 5:
                arg = vm.registers.B
            case 6:
                arg = vm.registers.C
            case _:
                arg = operand

        return fn(arg)

    return wrapper

@combo
def adv(operand):
    vm.registers.A //= 2**operand

def bxl(operand):
    vm.registers.B ^= operand

@combo
def bst(operand):
    vm.registers.B = operand % 8

def jnz(operand):
    if vm.registers.A != 0:
        vm.program.sp = operand
        vm.program.update_sp = False

def bxc(operand):
    vm.registers.B ^= vm.registers.C

@combo
def out(operand):
    vm.output.append(operand % 8)

@combo
def bdv(operand):
    vm.registers.B = vm.registers.A // 2**operand

@combo
def cdv(operand):
    vm.registers.C = vm.registers.A // 2**operand

opcodes = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
