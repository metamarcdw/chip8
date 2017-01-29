from .context import chip8

def test_stack_class():
    """ Tests aspects of the Stack class """

    stack = chip8.Stack(["foo", "bar"])
    assert isinstance(stack, chip8.Stack)

    list_ = stack.list_
    assert list_ == ["foo", "bar"]
    assert stack.size() == 2

    stack.push("baz")
    assert stack.list_ == ["foo", "bar", "baz"]
    assert stack.size() == 3

    item = stack.pop()
    assert item == "baz"
    assert stack.list_ == ["foo", "bar"]
    assert stack.size() == 2

