import os
import sys
import time
import random
import pdb  #<-- REMOVE ME

from bitstring import BitArray


class BadOpcodeError(Exception):
    pass

class StackOverflowError(Exception):
    pass

class KeyboardError(Exception):
    pass


class Stack:
    """ Stack object. Wraps a list. """
    MAX_SIZE = 16

    def __init__(self, list_=[]):
        """ Stack initializer.
            Initializes to a given list.
            Defaults to empty list.
        """
        self._list = list_

    def push(self, item):
        """ Push an item onto the stack.
            Raises: chip8.StackOverflowError.
        """
        self._list.append(item)
        if self.size() > self.MAX_SIZE:
            raise StackOverflowError(
                "Only {} levels available in the stack.".format(
                    self.MAX_SIZE))

    def pop(self):
        """ Pop an item off the top of the stack. """
        return self._list.pop()

    def peek(self):
        """ Returns the current item at the top of the stack. """
        return self._list[-1]

    def list_(self):
        """ Returns the current underlying list. """
        return self._list

    def size(self):
        """ Returns the current size of the stack. """
        return len(self._list)


class Memory:
    """ Memory object. Wraps a list of 'size' Bytes.
        'size' defaults to 4K.
    """

    def __init__(self, size=0x1000):
        """ Memory initializer.
            Initializes _bytes to a list of 'size' bytes.
        """
        self._bytes = [0x00 for x in range(size)]

    def _is_byte(self, byte, maximum=0xFF):
        """ Returns true if byte is int class,
            and has a value <= maximum.
        """
        return isinstance(byte, int) and byte <= maximum

    def save(self, byte, address):
        """ Saves a byte at an address in memory.
            Raises: ValueError and IndexError.
        """
        if not self._is_byte(byte):
            raise ValueError("'byte' was not a byte.")
            # Address must not be over 5 characters (4k in hex).
        if not self._is_byte(address, maximum=0xFFF):
            raise IndexError("'address' was not formed correctly.")

        self._bytes[address] = byte

    def load(self, address):
        """ Loads a byte from an address in memory.
            Raises: IndexError.
        """
            # Address must not be over 5 characters (4k in hex).
        if not self._is_byte(address, maximum=0xFFF):
            raise IndexError("'address' was not formed correctly.")
        return self._bytes[address]


class Registers(Memory):
    """ Memory object.
        Specifically 16 individual bytes of memory.
    """
    def __init__(self):
        super().__init__(size=16)

    def __str__(self):
        str_list = list()
        for i, val in enumerate(self._bytes):
            str_list.append("V{0}: {1}\t".format(hex(i)[2:], val))
            if (i + 1) % 4 == 0:
                str_list.append("\n")
        return "".join(str_list)


class Sprite(Memory):
    """ Sprite object, wraps a list of 'size' Bytes.
        'size' defaults to fifteen. Subclass of Memory.
    """
    MAX_SIZE = 15
    def __init__(self, size=15):
        """ Sprite initializer. """
        if size > self.MAX_SIZE:
            raise Exception("Sprite length too damn high!")
        super().__init__(size)

    def size(self):
        """ Returns the size in bytes. """
        return len(self._bytes)


class Keyboard:
    """ Keyboard object. Wraps a dict {str:boolean}. """
    KEYS = "0123456789ABCDEF"

    def __init__(self):
        """ Keyboard initializer.
            Initializes to a dict containing False
            for all extant keys. """
        self._keys = {s: False for s in self.KEYS}

    def press(self, key):
        """ Changes state of 'key' from unpressed to pressed.
            Raises: chip8.KeyboardError.
        """
        if key not in self.KEYS:
            raise KeyboardError(
                "'{}' key does not exist.".format(key))
        if self._keys[key]:
            raise KeyboardError(
                "'{}' is already pressed.".format(key))

        self._keys[key] = True

    def unpress(self, key):
        """ Changes state of 'key' from pressed to unpressed.
            Raises: chip8.KeyboardError.
        """
        if key not in self.KEYS:
            raise KeyboardError(
                "'{}' key does not exist.".format(key))
        if not self._keys[key]:
            raise KeyboardError(
                "'{}' key is already unpressed.".format(key))

        self._keys[key] = False

    def is_pressed(self, key):
        """ Checks whether state of 'key' is pressed or not.
            Raises: chip8.KeyboardError.
        """
        if key not in self.KEYS:
            raise KeyboardError(
                "'{}' key does not exist.".format(key))

        return self._keys[key]

    def get_pressed(self):
        """ Returns a list of strings representing all keys
            that are currently pressed.
        """
        list_ = list()
        for key, value in self._keys.items():
            if value:
                list_.append(key)
        return list_


class Display:
    """ Display object. Monochrome.
        Wraps a list of BitArrays, 64X32 bits.
    """
    WIDTH = 64
    HEIGHT = 32
    GLYPHS = "0123456789ABCDEF"
    FONT = {
        "0": "F999F", "1": "26227", "2": "F1F8F", "3": "F1F1F",
        "4": "99F11", "5": "F8F1F", "6": "F8F9F", "7": "F1244",
        "8": "F9F9F", "9": "F9F1F", "A": "F9F99", "B": "E9E9E",
        "C": "F888F", "D": "E999E", "E": "F8F8F", "F": "F8F88"}

    def __init__(self):
        """ Display initializer.
            Initialize self.glyph_sprites and clear the screen.
        """
        self._init_font()
        self.clear_screen()
        self.draw_flag = False

    def _init_font(self):
        """ Implements init of glyph_sprites. """
        self.glyph_sprites = list()
        for glyph in self.GLYPHS:
            sprite = Sprite(size=5)
            for i, s in enumerate(self.FONT[glyph]):
                byte = int("0x{}0".format(s), 16)
                sprite.save(byte, i)
            self.glyph_sprites.append(sprite)

    def clear_screen(self):
        """ Clear the screen. Set all pixels to off (False). """
        self._pixels = list()
        for y in range(self.HEIGHT):
            self._pixels.append(BitArray(self.WIDTH))
        self.draw_flag = True

    def _check_boundary(self, x, y):
        """ Raises ValueError if accessing outside of display."""
        if (0 <= x <= self.WIDTH and
            0 <= y <= self.HEIGHT):
            pass
        else:
            raise ValueError(
                "Accessing outside of display. X:{0} Y:{1}".format(x, y))

    @staticmethod
    def _ba_from_byte(byte):
        """ Convert an int to an 8bit BitArray. """
        return BitArray("0x{}".format(hex(byte)[2:].zfill(2)))

    def load_bytes(self, x, y, size):
        """ Load some bytes from the display. """
        self._check_boundary(x, y)
        bytes_ = list()
        for i in range(size):
            yi = (y + i) % self.HEIGHT
            ba = BitArray(8)
            for j in range(8):
                xj = (x + j) % self.WIDTH
                ba[j] = self._pixels[yi][xj]
            byte = int(ba.hex, 16)
            bytes_.append(byte)
        return bytes_

    def save_bytes(self, x, y, bytes_):
        """ Save some bytes to the display.
            Raises ValueError if saving outside of display.
        """
        self._check_boundary(x, y)
        for i, byte in enumerate(bytes_):
            ba = Display._ba_from_byte(byte)
            yi = (y + i) % self.HEIGHT
            d_line = self._pixels[yi]
            for j in range(8):
                xj = (x + j) % self.WIDTH
                d_line[xj] = ba[j]
        self.draw_flag = True

    @staticmethod
    def _check_collision(d_byte, x_byte):
        """ Check a display byte against a xor'd byte.
            Return true if collision, or False if not.
        """
        d_ba = Display._ba_from_byte(d_byte)
        x_ba = Display._ba_from_byte(x_byte)
        for i, bit in enumerate(d_ba):
            if bit and not x_ba[i]:
                return True
        return False

    def draw_sprite(self, x, y, sprite):
        """ Draw an arbitrary Sprite to an arbitrary coordinate
            on the display.
            Returns 1 if collision, or 0 if not.
        """
        collision = 0
        size = sprite.size()
        d_bytes = self.load_bytes(x, y, size)
        xor_bytes = list()
        for i in range(size):
            d_byte = d_bytes[i]
            s_byte = sprite.load(i)
            xor = d_byte ^ s_byte
            if self._check_collision(d_byte, xor):
                collision = 1
            xor_bytes.append(xor)
        self.save_bytes(x, y, xor_bytes)
        return collision

    def get_data(self):
        """ Return all display data as a 'bytes' object. """
        data = BitArray()
        for line in self._pixels:
            data += line[:self.WIDTH]
        return data.bytes

    def __str__(self):
        list_ = list()
        for line in self._pixels:
            list_.append(line.bin)
        return "{}\n".format("\n".join(list_))


class Chip8:
    """ CHIP-8 object. Contains all components.
        Implements actual instruction set
        and emulation functionality.
    """

    def __init__(self, prog_path=None):
        """ CHIP-8 Initializer.
            Initialize all components and load program.
        """
        self.clock_speed = 500 #Hz

        self.pc = 0x200
        self.i = 0x0000
        self.dt = 0x00
        self.st = 0x00

        self.v = Registers()
        self.mem = Memory()
        self.call_stack = Stack()

        self.keyboard = Keyboard()
        self.display = Display()

        self.pause_flag = False
        self.rom_loaded = False
        self.step_mode = False
        self.play_callback = None
        self.stop_callback = None

        self.load_font()
        if prog_path:
            self.load_from_file(prog_path)

    def load_font(self):
        """ Loads the font from self.display.glyph_sprites
            Into memory.
        """
        for i, glyph in enumerate(self.display.glyph_sprites):
            size = glyph.size()
            for j in range(size):
                byte = glyph.load(j)
                self.mem.save(byte, (i * size) + j)

    def load_from_file(self, prog_path):
        """ Loads the given program file into memory. """
        list_ = list()
        with open(prog_path, "rb") as prog:
            byte = prog.read(1)
            while byte:
                byte = int.from_bytes(byte, byteorder="big")
                list_.append(byte)
                byte = prog.read(1)
        self.load_program(list_) 

    def load_program(self, list_):
        """ Loads an integer list representing a chip8 program
            into memory.
        """
        addr = 0x200
        for i, byte in enumerate(list_):
            self.mem.save(byte, addr + i)
        self.rom_loaded = True

    def increment_pc(self):
        """ Increment the program counter. """
        self.pc += 2
        if self.pc > 0xfff:
            sys.exit(0)

    def print_register(self, index):
        val = self.v.load(index)
        print("V{0}: {1}".format(hex(index)[2:], val))

    def debug(self):
        str_ = input()
        if str_ in ("Q", "q"):
            sys.exit(0)
        elif str_.startswith("v"):
            reg = int(str_[1], 16)
            self.print_register(reg)
        elif str_ == "dump":
            print(str(self.v))
            print("Call Stack: {} <-top\n".format(
                self.call_stack.list_()))

    def emulate_cycle(self):
        """ Emulate one processor cycle. """
        opcode = self.fetch()
        if self.step_mode:
            print("EXECUTING OPCODE:{0} PC:{1} SP:{2} I:{3}".format(
                opcode.zfill(4),
                self.pc - 2,
                self.call_stack.size(),
                self.i))
            self.debug()
        instr = self.decode(int(opcode, 16))
        self.execute(instr)
        self.decrement_timers()

    def fetch(self):
        """ Fetch an opcode from program memory. """
        b1 = self.mem.load(self.pc)
        b2 = self.mem.load(self.pc + 1)
        opcode = hex((b1 << 8) + b2)[2:]
        self.increment_pc()
        return opcode

    def decode(self, opcode):
        """ Decode opcode and return instruction list. """
        instr = [(opcode & 0xf000) >> 12,
                (opcode & 0x0f00) >> 8,
                (opcode & 0x00f0) >> 4,
                opcode & 0x000f,
                opcode & 0x00ff,
                opcode & 0x0fff]
        return instr

    def execute(self, instr):
        """ Execute a decoded instruction!
            Raises BadOpcodeError if instruction
            is not recognized. """
        oper, x, y, n, kk, nnn = instr
        vx, vy = (self.v.load(x), self.v.load(y))

        if oper == 0x0:
            if y == 0xe:
                if n == 0x0:
                    # CLS
                    self.display.clear_screen()
                elif n == 0xe:
                    # RET
                    self.pc = self.call_stack.pop()
            else:
                # SYS
                """ 'This instruction is only used on the old
                    computers on which Chip-8 was originally
                    implemented. It is ignored by modern interpreters.'
                """
                pass
        elif oper == 0x1:
            # JP addr
            self.pc = nnn
        elif oper == 0x2:
            # CALL addr
            self.call_stack.push(self.pc)
            self.pc = nnn
        elif oper == 0x3:
            # SE Vx, byte
            if vx == kk:
                self.increment_pc()
        elif oper == 0x4:
            # SNE Vx, byte
            if vx != kk:
                self.increment_pc()
        elif oper == 0x5:
            # SE Vx, Vy
            if vx == vy:
                self.increment_pc()
        elif oper == 0x6:
            # LD Vx, byte
            self.v.save(kk, x)
        elif oper == 0x7:
            # ADD Vx, byte
            result = vx + kk
            result = result % 0x100
            self.v.save(result, x)
        elif oper == 0x8:
            if n == 0x0:
                # LD Vx, Vy
                self.v.save(vy, x)
            elif n == 0x1:
                # OR Vx, Vy
                result = vx | vy
                self.v.save(result, x)
            elif n == 0x2:
                # AND Vx, Vy
                result = vx & vy
                self.v.save(result, x)
            elif n == 0x3:
                # XOR Vx, Vy
                result = vx ^ vy
                self.v.save(result, x)
            elif n == 0x4:
                # ADD Vx, Vy
                carry = 0
                result = vx + vy
                if result > 0xff:
                    result = result % 0x100
                    carry = 1
                self.v.save(result, x)
                self.v.save(carry, 0xf)
            elif n == 0x5:
                # SUB Vx, Vy
                not_borrow = 0
                if vx > vy:
                    not_borrow = 1
                elif vx < vy:
                    vx += 0x100
                result = vx - vy
                self.v.save(result, x)
                self.v.save(not_borrow, 0xf)
            elif n == 0x6:
                # SHR Vx {, Vy}
                lsb = 0
                if BitArray(hex(vy))[-1]:
                    lsb = 1
                result = vy >> 1
                self.v.save(result, x)
                self.v.save(lsb, 0xf)
            elif n == 0x7:
                # SUBN Vx, Vy
                not_borrow = 0
                if vy > vx:
                    not_borrow = 1
                elif vy < vx:
                    vy += 0x100
                result = vy - vx
                self.v.save(result, x)
                self.v.save(not_borrow, 0xf)
            elif n == 0xe:
                # SHL Vx {, Vy}
                msb = 0
                if BitArray(hex(vy))[0]:
                    msb = 1
                result = vy << 1
                result = result % 0x100
                self.v.save(result, x)
                self.v.save(msb, 0xf)
            else:
                raise BadOpcodeError("Trying to execute bad opcode.")
        elif oper == 0x9:
            # SNE Vx, Vy
            if vx != vy:
                self.increment_pc()
        elif oper == 0xa:
            # LD I, addr
            self.i = nnn
        elif oper == 0xb:
            # JP V0, addr
            self.pc = nnn + self.v.load(0)
        elif oper == 0xc:
            # RND Vx, byte
            rnd = random.randint(0, 255)
            result = rnd & kk
            self.v.save(result, x)
        elif oper == 0xd:
            # DRW Vx, Vy, size
            sprite = Sprite(n)
            for i in range(n):
                byte = self.mem.load(self.i + i)
                sprite.save(byte, i)
            collision = self.display.draw_sprite(vx, vy, sprite)
            self.v.save(collision, 0xf)
        elif oper == 0xe:
            if y == 0x9 and n == 0xe:
                # SKP Vx
                keys = self.keyboard.KEYS
                if self.keyboard.is_pressed(keys[vx]):
                    self.increment_pc()
            elif y == 0xa and n == 0x1:
                # SKNP Vx
                keys = self.keyboard.KEYS
                if not self.keyboard.is_pressed(keys[vx]):
                    self.increment_pc()
            else:
                raise BadOpcodeError("Trying to execute bad opcode.")
        elif oper == 0xf:
            if y == 0x0:
                if n == 0x7:
                    # LD Vx, DT
                    self.v.save(int(self.dt), x)
                elif n == 0xa:
                    # LD Vx, K
                    pressed = self.keyboard.get_pressed()
                    if pressed != []:
                        result = int(pressed[0], 16)
                        self.v.save(result, x)
                    else:
                        self.pc -= 2
                else:
                    raise BadOpcodeError("Trying to execute bad opcode.")
            elif y == 0x1:
                if n == 0x5:
                    # LD DT, Vx
                    self.dt = vx
                elif n == 0x8:
                    # LD ST, Vx
                    self.st = vx
                elif n == 0xe:
                    # ADD I, Vx
                    result = self.i + vx
                    self.i = result
                else:
                    raise BadOpcodeError("Trying to execute bad opcode.")
            elif y == 0x2 and n == 0x9:
                # LD F, Vx
                font_size = self.display.glyph_sprites[0].size()
                self.i = vx * font_size
            elif y == 0x3 and n == 0x3:
                # LD B, Vx
                DIGITS = 3
                str_ = str(vx).zfill(DIGITS)
                for i, c in enumerate(str_):
                    self.mem.save(int(c), self.i + i)
            elif y == 0x5 and n == 0x5:
                # LD [I], Vx
                for i in range(x + 1):
                    byte = self.v.load(i)
                    self.mem.save(byte, self.i)
                    self.i += 1
            elif y == 0x6 and n == 0x5:
                # LD Vx, [I]
                for i in range(x + 1):
                    byte = self.mem.load(self.i)
                    self.v.save(byte, i)
                    self.i += 1
            else:
                raise BadOpcodeError("Trying to execute bad opcode.")

    def decrement_timers(self):
        """ Decrement the timers every cycle. """
        timer_freq = 60
        if self.dt > 0:
            self.dt -= timer_freq / self.clock_speed
        if self.st > 0:
            self.st -= timer_freq / self.clock_speed
            self.play_callback()
            # print("BUZZ!")
        else:
            self.stop_callback()

    def run(self):
        """ Run processor cycles at 500Hz. """
        FREQ = 1 / self.clock_speed
        starttime=time.time()
        while True:
            if not self.pause_flag:
                self.emulate_cycle()
            time.sleep(FREQ - ((time.time() - starttime) % FREQ))


def main():
    if sys.argv[1] == "-s":
        step = True
        prog = sys.argv[2].upper()
    else:
        step = False
        prog = sys.argv[1].upper()
    basepath = os.path.dirname(__file__)
    progpath = os.path.abspath(
        os.path.join(basepath, "..", "roms", prog))
    vm = Chip8(progpath)
    vm.step_mode = step
    vm.run()

if __name__ == "__main__":
    main()


