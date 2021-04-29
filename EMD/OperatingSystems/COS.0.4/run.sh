#assemble boot.s file
as --32 src/boot.s -o boot.o

#compile kernel.c file
gcc -m32 -c src/kernel.c -o kernel.o -std=gnu99 -ffreestanding -O2 -Wall -Wextra

#linking the kernel with kernel.o and boot.o files
ld -m i386pe -T src/link.ld kernel.o boot.o -o COS.bin -nostdlib

#check MyOS.bin file is x86 multiboot file or not
grub-file --is-x86-multiboot COS.bin

#building the iso file
mkdir -p isodir/boot/grub
cp COS.bin isodir/boot/COS.bin
cp grub.cfg isodir/boot/grub/grub.cfg
grub-mkrescue -o COS.iso isodir

#run it in qemu
qemu-system-x86_64 -cdrom COS.iso
