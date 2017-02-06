import os
import sys
import time
import pdb  #<-- REMOVE ME

from bitstring import BitArray


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

    def _check_boundary(self, x, y, sprite_width, sprite_height):
        """ Raises ValueError if accessing outside of display."""
        xerr = False
        if x < 0 or x + sprite_width > self.WIDTH:
            xerr = True
        yerr = False
        if y < 0 or y + sprite_height > self.HEIGHT:
            yerr = True
        if xerr or yerr:
            raise ValueError("Accessing outside of display.")

    def load_bytes(self, x, y, size):
        """ Load some bytes from the display. """
        self._check_boundary(x, y, 8, size)
        bytes_ = list()
        for i in range(size):
            byte = int(self._pixels[y + i][x:x+8].bin, 2)
            bytes_.append(byte)
        return bytes_

    def save_bytes(self, x, y, bytes_):
        """ Save some bytes to the display.
            Raises ValueError if saving outside of display.
        """
        self._check_boundary(x, y, 8, len(bytes_))
        for i, byte in enumerate(bytes_):
            d_line = self._pixels[y+i]
            d_line[x:x+8] = byte

    @staticmethod
    def _check_collision(d_byte, x_byte):
        """ Check a display byte against a xor'd byte.
            Return true if collision, or False if not.
        """
        d_ba = BitArray(hex(d_byte))
        x_ba = BitArray(hex(x_byte))
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


class Chip8:
    """ CHIP-8 object. Contains all components.
        Implements actual instruction set
        and emulation functionality.
    """

    def __init__(self, prog_path):
        """ CHIP-8 Initializer.
            Initialize all components and load program.
        """
        self.pc = 0x200
        self.i = 0x0000
        self.dt = 0x00
        self.st = 0x00

        self.v = Registers()
        self.mem = Memory()
        self.call_stack = Stack()

        self.keyboard = Keyboard()
        self.display = Display()

        self.load_font()
        self.load_program(prog_path)

    def load_font(self):
        """ Loads the font from self.display.glyph_sprites
            Into memory.
        """
        for i, glyph in enumerate(self.display.glyph_sprites):
            size = glyph.size()
            for j in range(size):
                byte = glyph.load(j)
                self.mem.save(byte, (i * size) + j)

    def load_program(self, prog_path):
        """ Loads the given program file into memory. """
        addr = self.pc
        with open(prog_path, "rb") as prog:
            byte = prog.read(1)
            while byte:
                byte = int.from_bytes(byte, byteorder="big")
                self.mem.save(byte, addr)
                addr += 1
                byte = prog.read(1)

    def increment_pc(self):
        """ Increment the program counter. """
        self.pc += 2
        if self.pc > 0xfff:
            sys.exit(0)

    def emulate_cycle(self):
        """ Emulate one processor cycle. """
        opcode = int(self.fetch(), 16)
        instr = self.decode(opcode)
        self.execute(instr)
        self.decrement_timers()

    def fetch(self):
        """ Fetch an opcode from program memory. """
        b1 = self.mem.load(self.pc)
        b2 = self.mem.load(self.pc + 1)
        opcode = (BitArray(hex(b1)) + BitArray(hex(b2))).hex.zfill(4)
        self.increment_pc()
        print(opcode)
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
        """ Execute a decoded instruction! """
        
        oper, x, y, n, kk, nnn = instr

        if oper == 0x0:
            if y == 0xe:
                if n == 0x0:
                    # CLS
                    pass
                elif n == 0xe:
                    # RET
                    pass
            else:
                # SYS
                pass
        elif oper == 0x1:
            # JP addr
            pass
        elif oper == 0x2:
            # CALL addr
            pass
        elif oper == 0x3:
            # SE Vx, byte
            pass
        elif oper == 0x4:
            # SNE Vx, byte
            pass
        elif oper == 0x5:
            # SE Vx, Vy
            pass
        elif oper == 0x6:
            # LD Vx, byte
            pass
        elif oper == 0x7:
            # ADD Vx, byte
            pass
        elif oper == 0x8:
            if n == 0x0:
                # LD Vx, Vy
                pass
            elif n == 0x1:
                # OR Vx, Vy
                pass
            elif n == 0x2:
                # AND Vx, Vy
                pass
            elif n == 0x3:
                # XOR Vx, Vy
                pass
            elif n == 0x4:
                # ADD Vx, Vy
                pass
            elif n == 0x5:
                # SUB Vx, Vy
                pass
            elif n == 0x6:
                # SHR Vx {, Vy}
                pass
            elif n == 0x7:
                # SUBN Vx, Vy
                pass
            elif n == 0xe:
                # SHL Vx {, Vy}
                pass
        elif oper == 0x9:
            # SNE Vx, Vy
            pass
        elif oper == 0xa:
            # LD I, addr
            pass
        elif oper == 0xb:
            # JP V0, addr
            pass
        elif oper == 0xc:
            # RND Vx, byte
            pass
        elif oper == 0xd:
            # DRW Vx, Vy, size
            pass
        elif oper == 0xe:
            if y == 0x9 and n == 0xe:
                # SKP Vx
                pass
            elif y == 0xa and n == 0x1:
                # SKNP Vx
                pass
        elif oper == 0xf:
            if y == 0x0:
                if n == 0x7:
                    # LD Vx, DT
                    pass
                elif n == 0xa:
                    # LD Vx, K
                    pass
            elif y == 0x1:
                if n == 0x5:
                    # LD DT, Vx
                    pass
                elif n == 0x8:
                    # LD ST, Vx
                    pass
                elif n == 0xe:
                    # ADD I, Vx
                    pass
            elif y == 0x2 and n == 0x9:
                # LD F, Vx
                pass
            elif y == 0x3 and n == 0x3:
                # LD B, Vx
                pass
            elif y == 0x5 and n == 0x5:
                # LD [I], Vx
                pass
            elif y == 0x6 and n == 0x5:
                # LD Vx, [I]
                pass

    def decrement_timers(self):
        """ Decrement the timers every cycle. """
        if self.dt > 0:
            self.dt -= 1
        if self.st > 0:
            self.st -= 1
            # TODO: Play sound
            print("BEEP!")


    def run(self):
        """ Run processor cycles at 60Hz. """
        FREQ = 1 / 60
        starttime=time.time()
        while True:
            self.emulate_cycle()
            time.sleep(FREQ - ((time.time() - starttime) % FREQ))


def main():
    PROG = "MERLIN"
    basepath = os.path.dirname(__file__)
    progpath = os.path.abspath(
        os.path.join(basepath, "..", "roms", PROG))
    vm = Chip8(progpath)
    vm.run()

if __name__ == "__main__":
    main()


