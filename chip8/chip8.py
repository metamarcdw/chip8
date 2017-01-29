
class StackOverflowError(Exception):
    pass


class Stack:
    """ Stack object. Wraps a list. """
    MAX_SIZE = 16

    def __init__(self, list_=[]):
        """ Stack initiator.
            Initiate with a given list.
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
    """ Memory object. Wraps a list of 4K Bytes. """

    def __init__(self):
        """ Memory initiator.
            Initiates mem to a list of 4096 bytes.
        """
        self._bytes = [0x00 for x in range(0x1000)]

    def _is_byte(self, byte, length=4):
        """ Returns true if byte is int class,
            and has a hex string <= length.
        """
        return isinstance(byte, int) and len(hex(byte)) <= length

    def save(self, byte, address):
        """ Saves a byte at an address in memory.
            Raises: ValueError and IndexError
        """
        if not self.is_byte(byte):
            raise ValueError("'byte' was not a byte.")
            # Address must not be over 5 characters (4k in hex).
        if not self.is_byte(address, length=5):
            raise IndexError("'address' was not formed correctly")

        self._bytes[address] = byte


