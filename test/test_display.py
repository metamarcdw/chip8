import pytest
import bitstring

from .context import chip8


display = chip8.Display()

def test_display_class():
    """ Tests attributes of the Display class. """
    assert isinstance(display, chip8.Display)
    assert isinstance(display._pixels, list)
    assert isinstance(display._pixels[0], bitstring.BitArray)
    assert len(display._pixels[0]) == display.WIDTH
    assert isinstance(display.glyph_sprites, list)
    assert isinstance(display.glyph_sprites[0], chip8.Sprite)

def test_save_bytes():
    display.save_bytes(2, 3, [0xff, 0xff])
    assert display._pixels[3][2:10].bin == "11111111"

def test_load_bytes():
    bytes_ = display.load_bytes(2, 3, 2)
    bytes_ = [0xff, 0xff]

def test_check_collision():
    assert display._check_collision(0xff, 0x00)
    assert not display._check_collision(0x00, 0xff)

def test_draw_sprite():
    display.clear_screen()
    sprite = chip8.Sprite(1)
    sprite.save(0b01010101, 0)
    assert display.draw_sprite(3, 5, sprite) == 0
    bytes_ = display.load_bytes(3, 5, 1)
    assert bytes_[0] == 0b01010101

def test_draw_glyph():
    display.clear_screen()
    glyph = display.glyph_sprites[0x3]
    assert display.draw_sprite(23, 4, glyph) == 0
    bytes_ = display.load_bytes(23, 4, 5)
    assert bytes_[3] == 0b00010000

def test_x_error():
    with pytest.raises(ValueError):
        glyph = display.glyph_sprites[0xf]
        display.draw_sprite(57, 0, glyph)

def test_y_error():
    with pytest.raises(ValueError):
        display.load_bytes(0, 28, 5)


