import sequtils, strutils
import ../../common/jmc
import ../common/emulator

let
    state = JMCState.new()
    file = readFile("../assembler/out.bin").string

var bytes = newSeq[uint8](file.len)
for i, c in file.pairs():
    bytes[i] = c.uint8
state.loadMemory(bytes, 0x0000)

echo toHex(state.stackPointer.int)
for i in 0..300:
  state.executeNext()

for i, r in state.registers.values.pairs():
    echo $(i.Register) & " -> " & $r
echo "PC -> " & toHex(state.programCounter.int)
echo "SP -> " & toHex(state.stackPointer.int)