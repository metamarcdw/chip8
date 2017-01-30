
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

    def _is_byte(self, byte, length=4):
        """ Returns true if byte is int class,
            and has a hex string <= length.
        """
        return isinstance(byte, int) and len(hex(byte)) <= length

    def save(self, byte, address):
        """ Saves a byte at an address in memory.
            Raises: ValueError and IndexError.
        """
        if not self._is_byte(byte):
            raise ValueError("'byte' was not a byte.")
            # Address must not be over 5 characters (4k in hex).
        if not self._is_byte(address, length=5):
            raise IndexError("'address' was not formed correctly.")

        self._bytes[address] = byte

    def load(self, address):
        """ Loads a byte from an address in memory.
            Raises: IndexError.
        """
            # Address must not be over 5 characters (4k in hex).
        if not self._is_byte(address, length=5):
            raise IndexError("'address' was not formed correctly.")
        return self._bytes[address]


class Sprite(Memory):
    """ Sprite object, wraps a list of 'size' Bytes.
        'size' defaults to fifteen. Subclass of Memory.
    """
    def __init__(self, size=15):
        """ Sprite initializer. """
        super().__init__(size)


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
    """ """
    pass


