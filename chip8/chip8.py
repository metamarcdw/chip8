
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
        """ Push an item onto the stack. """
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

    def size(self):
        """ Returns the current size of the stack. """
        return len(self._list)


