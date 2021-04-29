import "../../common/jmc"
import "../common/assembler"

for x in assemble("test.asm", "lda [0xFF00]"):
  echo $(x.int)