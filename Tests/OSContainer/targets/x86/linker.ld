ENTRY(_start)

SECTIONS {
    . = 1M

    .header: *build\x86\header.o
    .text: *build\x86\main.o
}
