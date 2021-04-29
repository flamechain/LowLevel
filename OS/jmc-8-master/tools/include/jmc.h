#ifndef __JMC_H
#define __JMC_H

typedef enum Register {
	A, B, C, D, I, J, Z, F
} Register;

typedef enum Instruction {
	PUSH,		/* arg = [SP++] */
	POP,		/* [--SP] = arg */
	JNZ,		/* arg > 0 ? PC = IJ */
	MW,			/* arg0 = arg1 */
	LW,			/* arg0 = [arg1] */
	SW,			/* [arg0] = arg1 */
	LDA,		/* IJ = arg */
	ADD,		/* reg = arg + arg */
	ADC,		/* reg = arg + arg + c */
	SUB,		/* reg = arg - arg */
	SBB,		/* reg = arg - arg - b */
	AND,		/* reg = arg & arg */
	OR,			/* reg = arg | arg */
	NOR,		/* reg = ~(arg | arg) */
	CMP			/* Compare and load F */
} Instruction;

typedef struct JMCState {
	int _dummy;
} JMCState;

#endif