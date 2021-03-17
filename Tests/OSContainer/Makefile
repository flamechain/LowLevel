x86_source_files := $(shell find src/impl/x86/boot *.asm)
x86_object_files := $(patsubst src/impl/x86/boot/%.asm, build/x86/%.o, $(x86_source_files))

$(x86_object_files):
	mkdir $(dir $@)
	asm $(patsubst build/x86/%.o, src/impl/x86/boot/%.asm $@) -o $@

mkdir dist/x86
Mx86 targets/x86/linker.ld -o dist/x86/kernel.bin
