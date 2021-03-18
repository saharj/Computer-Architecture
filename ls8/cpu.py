"""CPU functionality."""

import sys


LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110

SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ir = 0
        self.ram = {}
        self.output = []
        self.reg = [0] * 8
        self.branchtable = {}
        self.reset()
        self.branchtable[LDI] = {"fn": self.handle_ldi, "step": 3}
        self.branchtable[PRN] = {"fn": self.handle_prn, "step": 2}
        self.branchtable[MUL] = {"fn": self.handle_mul, "step": 3}
        self.branchtable[HLT] = {"fn": self.handle_hlt, "step": 1}
        self.branchtable[PUSH] = {"fn": self.handle_push, "step": 2}
        self.branchtable[POP] = {"fn": self.handle_pop, "step": 2}

    def reset(self):
        """
        This method resets the CPU's registers to their defaults.
        """
        self.pc = 0  # : Program Counter
        self.ir = 0  # : Instruction Register
        self.running = False

    def load(self):
        """Load a program into memory."""

        try:
            file_name = sys.argv[1]
            with open(file_name) as f:
                address = 0

                for line in f:
                    num_string = line.split("#")[0].strip()

                    if num_string == "":
                        continue
                    else:
                        self.ram[address] = int(num_string, 2)
                        address += 1
        except FileNotFoundError:
            print("I can not find the file!!!!!!!!")
        # print(self.ram)
        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        # elif op == "MUL":
        #     self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_ldi(self, operand_a, operand_b):
        num = self.ram[operand_b]
        # get the reg index.
        reg_index = self.ram[operand_a]
        # put the number in the registers list at the index of reg_index
        self.ram_write(num, reg_index)

    def handle_prn(self, operand_a, operand_b):
        reg_index = self.ram[operand_a]
        print(self.reg[reg_index])

    def handle_hlt(self, operand_a, operand_b):
        self.running = False

    def handle_mul(self, operand_a, operand_b):
        reg_index1 = self.ram[operand_a]
        reg_index2 = self.ram[operand_b]
        # self.alu("MUL", reg_index1, reg_index2)
        self.reg[reg_index1] *= self.reg[reg_index2]
        self.ram_write(self.reg[reg_index1], reg_index1)

    def handle_push(self, operand_a, operand_b):
        self.reg[SP] -= 1
        reg_index = self.ram[operand_a]
        self.ram[self.reg[SP]] = self.reg[reg_index]

    def handle_pop(self, operand_a, operand_b):
        reg_index = self.ram[operand_a]
        self.reg[reg_index] = self.ram[self.reg[SP]]
        self.reg[SP] += 1

    def run(self):
        """Run the CPU."""
        self.reg[SP] = 0xf4
        self.running = True

        while self.running:
            inst = self.ram_read(self.pc)
            operand_a = self.pc + 1
            operand_b = self.pc + 2

            self.branchtable[inst]["fn"](operand_a, operand_b)
            self.pc += self.branchtable[inst]["step"]

    def ram_read(self, pc):
        if pc:
            self.pc = pc

        return self.ram[self.pc]

    def ram_write(self, num, index):
        self.reg[index] = num
