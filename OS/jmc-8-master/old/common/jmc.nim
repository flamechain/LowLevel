import sequtils
import util

type
    # Opcodes
    Instruction* {.pure.} = enum
        PUSH    = 0x00
        POP     = 0x01
        JNZ     = 0x02
        MW      = 0x03
        LW      = 0x04
        SW      = 0x05
        LDA     = 0x06
        ADD     = 0x08
        ADC     = 0x09
        SUB     = 0x0A
        SBB     = 0x0B
        AND     = 0x0C
        OR      = 0x0D
        NOR     = 0x0E
        CMP     = 0x0F

    FlagMask* {.pure.} = enum
        Less = 0x1,
        Equal = 0x2,
        Greater = 0x4,
        Carry = 0x8,
        Borrow = 0x10,
        OverFlow = 0x20

    # Register codes
    Register* {.pure.} = enum
        A = 0, B = 1, C = 2, D = 3, I = 4, J = 5, Z = 6, F = 7

    # Register state object
    Registers* = object
        values*: array[0..7, uint8]

    # RAM object. Always tied to state so that it can accurately supply
    # values for PC and SP.
    Memory* = object
        state: JMCState
        values: array[0..0xFFFB, uint8]

    # Dummy object for flags
    Flags* = object
        state: JMCState

    # Dummy obejct for each flag
    Flag* = bool

    # JMC state object
    JMCState* = ref object
        stackPointer*: uint16
        programCounter*: uint16
        memory*: Memory
        registers*: Registers
        flags*: Flags

proc constructor*(self: JMCState): void {.ctor.} =
    self.memory.state = self
    self.flags.state = self

# Memory access that handles PC, SP and out of bounds errors
proc `[]`*[T: SomeInteger](self: Memory, address: T): uint8 =
    if address.int >= 0 and address.int < 0xFFFC:
        return self.values[address]
    elif address.int >= 0xFFFC and address.int <= 0xFFFF:
        return case address
            of 0xFFFC: (self.state.programCounter and 0xFF).uint8
            of 0xFFFD: ((self.state.programCounter shr 8) and 0xFF).uint8
            of 0xFFFE: (self.state.stackPointer and 0xFF).uint8
            of 0xFFFF: ((self.state.stackPointer shr 8) and 0xFF).uint8
            else: 0
    else:
        raise newException(Exception, "Invalid memory address " & $(address.int))

# Same as above, but a setter
proc `[]=`*[T0: SomeInteger, T1: SomeInteger](self: var Memory, address: T0, data: T1): void =
    if address.int >= 0 and address.int < 0xFFFC:
        self.values[address.int] = data.uint8
    elif address.int >= 0xFFFC and address.int <= 0xFFFF:
        case address
        of 0xFFFC: self.state.programCounter = (self.state.programCounter and 0xFF00) or uint16(data and 0xFF)
        of 0xFFFD: self.state.programCounter = (self.state.programCounter and 0x00FF) or uint16(data.int shl 8)
        of 0xFFFE: self.state.stackPointer = (self.state.stackPointer and 0xFF00) or uint16(data and 0xFF)
        of 0xFFFF: self.state.stackPointer = (self.state.stackPointer and 0x00FF) or uint16(data.int shl 8)
        else: discard
    else:
        raise newException(Exception, "Invalid memory address " & $(address.int))

proc `[]`*[T: SomeInteger | Register](self: Registers, index: T): uint8 =
    let regIndex =
        when T is SomeInteger: index
        else: index.ord
    return self.values[regIndex.uint8]

proc `[]=`*[T0: SomeInteger | Register, T1: SomeInteger](self: var Registers, index: T0, value: T1): void =
    let regIndex =
        when T0 is SomeInteger: index
        else: index.ord
    self.values[regIndex.uint8] = value.uint8

proc `indirectAddress`*(self: JMCState): uint16 =
    (self.registers[Register.I].uint16 shl 8) or self.registers[Register.J].uint16

proc `indirectAddress=`*[T: SomeInteger](self: JMCState, value: T): void =
    self.registers[Register.I] = uint8((value shr 8) and 0xFF)
    self.registers[Register.J] = uint8(value and 0xFF)

# Converters so that flags can be easily used among different contexts
converter flagToBoolean*(self: Flag): bool = self
converter flagToI*(self: Flag): int = (if self: 1 else: 0)
converter flagToU*(self: Flag): uint = (if self: 1 else: 0)
converter flagToU8*(self: Flag): uint8 = (if self: 1 else: 0)

# Declares a flag in the F register
template declFlag(name: untyped, mask: FlagMask, index: uint8): void =
    proc `name`*(self: Flags): Flag =
        Flag((self.state.registers[Register.F] and mask.ord.uint8) != 0)

    proc `name=`*[T: SomeInteger | bool](self: Flags, value: T): void =
        let
            tValue =
                when T is bool: if value: 1 else: 0
                else: value
            fValue = self.state.registers[Register.F]

        # Find index at compile time of this mask
        self.state.registers[Register.F] =
            fValue xor (cast[uint8](-tValue) xor fValue) and (1 shl index)

declFlag(less, FlagMask.Less, 0)
declFlag(equal, FlagMask.Equal, 1)
declFlag(greater, FlagMask.Greater, 2)
declFlag(carry, FlagMask.Carry, 3)
declFlag(borrow, FlagMask.Borrow, 4)
declFlag(overflow, FlagMask.Overflow, 5)