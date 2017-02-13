import pytest

from .context import chip8


keyboard = chip8.Keyboard()

def test_keyboard_class():
    """ Tests attributes of the Keyboard class. """
    assert isinstance(keyboard, chip8.Keyboard)
    assert not keyboard._keys["0"]
    assert len(keyboard._keys) == 16

def test_press_method():
    keyboard.press("A")
    assert keyboard._keys["A"]

def test_unpress_method():
    keyboard.unpress("A")
    assert not keyboard._keys["A"]

def test_is_pressed_method():
    assert not keyboard.is_pressed("A")
    keyboard.press("B")
    assert keyboard.is_pressed("B")

def test_press_keyboarderror():
    """ Test that the KeyboardError is raised when
        the key to be pressed does not exist.
    """
    with pytest.raises(chip8.KeyboardError):
        keyboard.press("Z")

def test_press_already_pressed():
    """ Test that KeyboardError is raised when
        the key is already pressed.
    """
    with pytest.raises(chip8.KeyboardError):
        keyboard.press("B")

def test_unpress_keyboarderror():
    """ Test that the KeyboardError is raised when
        the key to be unpressed does not exist.
    """
    with pytest.raises(chip8.KeyboardError):
        keyboard.unpress("Z")

def test_unpress_already_unpressed():
    """ Test that KeyboardError is raised when
        the key is already unpressed.
    """
    with pytest.raises(chip8.KeyboardError):
        keyboard.unpress("A")

def test_is_pressed_keyboarderror():
    """ Tests that the KeyboardError is raised when
        the key being checked does not exist.
    """
    with pytest.raises(chip8.KeyboardError):
        keyboard.is_pressed("Z")

def test_get_pressed_method():
    """ Tests that the correct list is returned by
        get_pressed().
    """
    keyboard.press("1")
    keyboard.press("A")
    assert keyboard.get_pressed() == ["1", "A", "B"]


