import pytest

from .context import chip8


sprite = chip8.Sprite()

def test_sprite_class():
    """ Tests attributes of the Sprite class. """
    assert isinstance(sprite, chip8.Sprite)
    assert isinstance(sprite._bytes[0], int)
    assert len(sprite._bytes) == 15

def test_save_indexerror():
    with pytest.raises(IndexError):
        sprite.save(0xFF, 16)


