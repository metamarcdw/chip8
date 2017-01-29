
class Stack:
    """ Stack object. Wraps a list. """

    def __init__(self, list_=[]):
        """ Stack initiator.
            Initiate with a given list.
            Defaults to empty list.
        """
        self.list_ = list_

    def push(self, item):
        """ Push an item onto the stack. """
        self.list_.append(item)

    def pop(self):
        """ Pop an item off the top of the stack. """
        return self.list_.pop()


