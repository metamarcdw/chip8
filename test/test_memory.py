import pytest

from .context import chip8


mem = chip8.Memory()

def test_memory_class():
    """ Tests attributes of the Memory class. """
    assert isinstance(mem, chip8.Memory)
    assert isinstance(mem._bytes[0], int)
    assert len(mem._bytes) == 4096

def test_save_method():
    mem.save(0xFF, 0x200)
    assert mem._bytes[0x200] == 0xFF

def test_save_valueerror():
    with pytest.raises(ValueError):
        mem.save(0x100, 0x200)

def test_save_indexerror():
    with pytest.raises(IndexError):
        mem.save(0xFF, 0x1000)

def test_load_method():
    item = mem.load(0x200)
    assert item == 0xFF

def test_load_indexerror():
    with pytest.raises(IndexError):
        mem.load(0x1000)


