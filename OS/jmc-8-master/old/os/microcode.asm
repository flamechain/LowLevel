; JMC-8 microcode

.microcode
.block
JMC-8 microcode is meant to be written onto either one 16-bit ROM or two
chained 8-bit ROMs addressed as though they were one 16-bit ROM. The
microcode directly controls the internal state of the minicomputer through
two types of control words, one being used mostly for read/write operations
and data movement and the other being used for data processing. Each word of
microcode is 16-bits.

The top two bits of the microcode are special.
	- Bit 16 specifies the microcode type (1 = read/write, 0 = processing)
	- Bit 15 is 1 if this word of microcode is the last word in this
	  instruction's microcode sequence.

The microcode is indexed in memory (ROM) as follows:
0000XXXX000YZZZZ
	- X are the 4 bits that specify the instruction's opcode'
	- The Y bit corresponds to the Y-bit of the instruction (Y = 0 means
	  constant/immediate argument(s), Y = 1 means register argument(s))
	- Z are the index of each sequential microcode word. This allows for
	  a maximum of 16 words of microcode, though each instruction is
	  considerably less.

Each word of microcode corresponds directly to one clock cycle.
This means that the total time (in cycles) of an instruction can be computed as:
	number of microcode words + number of instruction bytes = total cycles

Microcode type 1 includes the following available bits (LSB to MSB):
r0_out
r1_out
reg_in
ir1_out
ir2_out
addr_imm
addr_ij
addr_sp
mem_in
mem_out
i_in
j_in
UNUSED
UNUSED
<LAST>
<1>

Microcode type 0:
r0_out
r1_out
reg_in
ir1_out
ir2_out
load_f
alu_out
load_x
load_y
sp_inc
sp_dec
load_pc_ij
stop_if_zero
UNUSED
<LAST>
<0>
.endblock

; Microcode for all arithmetic instructions is the same, the CPU deals with
; making the ALU do each specific operation
add, adc, sub, sbb, and, or, nor, cmp:
.const:
	r0_out, load_x
	ir1_out, load_y
	alu_out, reg_in
	load_f
.else:
	r0_out, load_x
	r1_out, load_y
	alu_out, reg_in
	load_f

push:
.const:
	sp_inc
	addr_sp, mem_in, ir1_out
.else:
	sp_inc
	addr_sp, mem_in, r0_out

; 'pop' can't accept constant arguments
pop:
.const:
.else:
	addr_sp, mem_out, reg_in
	sp_dec

; 'jnz' is the only operation that uses stop_if_zero and load_pc_ij
jnz:
.const:
	ir1_out, stop_if_zero
	load_pc_ij
.else:
	r0_out, stop_if_zero
	load_pc_ij

mw:
.const:
	ir1_out, reg_in
.else:
	r1_out, reg_in

lw:
.const:
	addr_imm, mem_out, reg_in
.else:
	addr_ij, mem_out, reg_in

sw:
.const:
	addr_imm, mem_in, r0_out
.else:
	addr_ij, mem_in, r0_out

; 'lda' does not accept register arguments
lda:
.const:
	ir1_out, j_in, reg_in
	ir2_out, i_in, reg_in
.else: