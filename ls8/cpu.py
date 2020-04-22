"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add list properties to the CPU class to hold 256 bytes of memory and 8 general-purpose registers.
        self.reg = [0] * 8  # 8 general purpose registers: 8 bits
        self.pc = 0
        self.ram = [0] * 256  # 256 bytes of memory

    # ram_read() accepts the address to read and return the value stored there.
    # The MAR contains the address that is being read or written to.
    def ram_read(self, mar):
        return self.ram[mar]

    # ram_write() accepts a value to write, and the address to write it to.
    # The MDR contains the data that was read or the data to write.
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, prog):
        """Load a program into memory."""

        address = 0

        with open(prog) as f:
            for instruction in f:
                inst_split = instruction.split("#")
                inst = inst_split[0].strip()

                if inst == "":
                    continue

                inst_int = int(inst, 2)
                self.ram_write(inst_int, address)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        running = True

        while running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if ir == HLT:
                running = False
                self.pc += 1
                sys.exit()
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == MUL:
                print(self.alu("MUL", operand_a, operand_b))
                # print(self.reg[operand_a] * self.reg[operand_b])
                self.pc += 3
            else:
                print("Unknown instruction")
                running = False
                sys.exit()
