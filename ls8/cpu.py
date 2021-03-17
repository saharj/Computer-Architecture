"""CPU functionality."""

import sys


LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = {}
        self.output = []
        self.reg = [0] * 8

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
        print(self.ram)
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

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            inst = self.ram_read(self.pc)
            operand_a = self.pc + 1
            operand_b = self.pc + 2

            # decode
            if inst == HLT:
                # execute
                running = False
                self.pc += 1

            elif inst == LDI:
                # execute
                # get the num.
                num = self.ram[operand_b]
                # get the reg index.
                reg_index = self.ram[operand_a]
                # put the number in the registers list at the index of reg_index
                self.ram_write(num, reg_index)
                self.pc += 3

            elif inst == PRN:
                # execute
                reg_index = self.ram[operand_a]
                print(self.reg[reg_index])
                self.pc += 2

            elif inst == MUL:
                # execute
                reg_index1 = self.ram[operand_a]
                reg_index2 = self.ram[operand_b]
                res = self.reg[reg_index1] * self.reg[reg_index2]
                self.ram_write(res, reg_index1)
                self.pc += 3

            # decode
            else:
                print(f"Unknown instruction {inst}")
                running = False

    def ram_read(self, pc):
        if pc:
            self.pc = pc

        return self.ram[self.pc]

    def ram_write(self, num, index):
        self.reg[index] = num
