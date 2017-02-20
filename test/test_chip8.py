import pytest

from .context import chip8


vm = chip8.Chip8()

def test_chip8_class():
    """ Tests attributes of the Chip8 class. """
    assert isinstance(vm, chip8.Chip8)
    assert vm.pc == 0x200
    assert vm.i == 0
    assert vm.dt == 0
    assert vm.st == 0
    assert isinstance(vm.v, chip8.Registers)
    assert isinstance(vm.mem, chip8.Memory)
    assert isinstance(vm.call_stack, chip8.Stack)
    assert isinstance(vm.keyboard, chip8.Keyboard)
    assert isinstance(vm.display, chip8.Display)
    assert not vm.buzzing
    assert not vm.step_mode

def test_vm_font_loaded():
    assert vm.mem.load(0) == 0xf0
    assert vm.mem.load(15*5) == 0xf0

def test_vm_load_program():
    vm.load_program([123, 221])
    assert vm.mem.load(0x200) == 123
    assert vm.mem.load(0x201) == 221

def test_vm_increment_pc():
    vm.increment_pc()
    assert vm.pc == 0x202
    vm.pc -= 2
    assert vm.pc == 0x200

def test_vm_fetch():
    opcode_str = vm.fetch()
    b1 = vm.mem.load(0x200)
    b2 = vm.mem.load(0x201)
    assert opcode_str == hex((b1 << 8) + b2)[2:]
    assert vm.pc == 0x202
    vm.pc -= 2

def test_vm_decode():
    opcode = vm.fetch()
    instr = vm.decode(int(opcode, 16))
    assert instr[0] == 0x7
    assert instr[1] == 0xb
    assert instr[2] == 0xd
    assert instr[3] == 0xd
    assert instr[4] == 0xdd
    assert instr[5] == 0xbdd

def test_decrement_timers():
    vm.dt = 1
    vm.st = 1
    vm.decrement_timers()
    assert vm.dt == 0
    assert vm.st == 0
    vm.decrement_timers()
    assert vm.dt == 0
    assert vm.st == 0

def asm(opcode_list):
    """ Helper function, converts opcode
        strings to a program list.
    """
    byte_list = list()
    for op in opcode_list:
        i = int(op, 16)
        b1 = (i & 0xff00) >> 8
        b2 = i & 0x00ff
        byte_list.append(b1)
        byte_list.append(b2)
    return byte_list

def update_program(opcode_list):
    """ Helper function. Assemble a new program,
        wipe the old, and load the new into memory.
    """
    prog = asm(opcode_list)
    vm.wipe_program()
    vm.load_program(prog)
    vm.pc = 0x200

"""
def test_opcode_CLS():
    code = [    "600a", # LOAD 0x0a into v0
                "6105", # LOAD 0x05 into v1
                "6205", # LOAD 0x05 into v2
                "f029", # LOAD index for glyph of v0 into I
                "d125"] # DRAW sprite from I at (v1, v2)
    update_program(code)
    for i in range(len(code)):
        vm.emulate_cycle()
    d_bytes = vm.display.load_bytes(5, 5, 5)
    assert d_bytes == [0xf0, 0x90, 0xf0, 0x90, 0x90]
"""

