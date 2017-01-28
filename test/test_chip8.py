from context import chip8

def test_stack_class():
    """ Tests aspects of the Stack class """

    stack = chip8.chip8.Stack(["foo", "bar"])

    list = stack.list()
    assert list == ["foo", "bar"]

    stack.push("baz")
    assert stack.list() == ["foo", "bar", "baz"]

    item == stack.pop()
    assert item == "baz"
    assert stack.list() == ["foo", "bar"]

