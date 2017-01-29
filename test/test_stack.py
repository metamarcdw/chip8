import pytest

from .context import chip8


stack = chip8.Stack(["foo", "bar"])

def test_stack_class():
    """ Tests attributes of the Stack class. """

    assert isinstance(stack, chip8.Stack)
    assert chip8.Stack.MAX_SIZE == 16

    list_ = stack._list
    assert list_ == ["foo", "bar"]
    assert stack.size() == 2

def test_push_method():
    """ Tests the Stack class' push() method. """
    stack.push("baz")
    assert stack._list == ["foo", "bar", "baz"]
    assert stack.size() == 3

def test_pop_method():
    """ Tests the Stack class' pop() method. """
    item = stack.pop()
    assert item == "baz"
    assert stack._list == ["foo", "bar"]
    assert stack.size() == 2

def test_peek_method():
    """ Tests the Stack class' peek() method. """
    item = stack.peek()
    assert item == "bar"
    assert stack._list == ["foo", "bar"]
    assert stack.size() == 2

def test_size_method():
    """ Tests the Stack class' size() method. """
    size = stack.size()
    assert size == 2

    for x in range(chip8.Stack.MAX_SIZE - size):
        stack.push(x)
    assert stack.size() == chip8.Stack.MAX_SIZE

def test_overflow_error():
    """ Tests that the StackOverflowError gets raised, as it should
        when the size of the stack exceeds Stack.MAX_SIZE
    """
    with pytest.raises(chip8.StackOverflowError):
        stack.push("final")


