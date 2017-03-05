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
    assert not vm.pause_flag
    assert not vm.rom_loaded
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
    factor = 60/500
    vm.decrement_timers()
    assert vm.dt == 1 - factor
    assert vm.st == 1 - factor
    vm.decrement_timers()
    assert vm.dt == 1 - factor * 2
    assert vm.st == 1 - factor * 2

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
    vm.__init__()
    prog = asm(opcode_list)
    vm.load_program(prog)

"""
def test_opcode_DRW_CLS():
    code = [    "600a", # LD v0, 0x0a
                "6105", # LD v1, 0x05
                "6205", # LD v2, 0x05
                "f029", # LD F, v0
                "d125"] # DRW (v1, v2), 0x5
    update_program(code)
    for i in range(len(code)):
        vm.emulate_cycle()
    d_bytes = vm.display.load_bytes(5, 5, 5)
    assert d_bytes == [0xf0, 0x90, 0xf0, 0x90, 0x90]
"""

def test_opcode_CALL_RET():
    code = [    "2204", # 200| CALL 0x204
                "0000", # 202| blank
                "00ee"] # 204| RET
    update_program(code)
    assert vm.pc == 0x200
    vm.emulate_cycle()
    assert vm.pc == 0x204
    assert vm.call_stack.size() == 1
    assert vm.call_stack.peek() == 0x202
    vm.emulate_cycle()
    assert vm.call_stack.size() == 0
    assert vm.pc == 0x202

def test_opcode_JP_addr():
    code = ["1210"]
    update_program(code)
    assert vm.pc == 0x200
    vm.emulate_cycle()
    assert vm.pc == 0x210

def test_opcode_LD_SE_vx_byte():
    code = [    "6023", # 200| LD v0, 0x23
                "3023"] # 202| SE v0, 0x23
    update_program(code)
    vm.emulate_cycle()
    assert vm.pc == 0x202
    vm.emulate_cycle()
    assert vm.pc == 0x206


