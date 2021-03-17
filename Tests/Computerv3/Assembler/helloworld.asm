PORTB = $6000
PORTA = $6001
DDRB = $6002
DDRA = $6003

E = %00000100
RS = %00000010
RW = %00000001

    .org $8000

reset:
    ldac #%11111111 ; Set all pins on port B to output
    stac DDRB
    ldac #%00000111 ; Set top 3 pins on port A to output
    stac DDRA
    ldac #%00111000
    jsr lcd_ins
    ldac #%00001100 ; Display on; cursor on; blink off
    jsr lcd_ins
    ldac #%00000110 ; Increment cursor; Shift off
    jsr lcd_ins

    ldac #"H"
    jsr print_char
    ldac #"e"
    jsr print_char
    ldac #"l"
    jsr print_char
    ldac #"l"
    jsr print_char
    ldac #"o"
    jsr print_char

    ldac #","
    jsr print_char
    ldac #" "
    jsr print_char

    ldac #"w"
    jsr print_char
    ldac #"o"
    jsr print_char
    ldac #"r"
    jsr print_char
    ldac #"l"
    jsr print_char
    ldac #"d"
    jsr print_char
    ldac #"!"
    jsr print_char

loop:
    jmp loop

lcd_ins:
    stac PORTB
    ldac #0
    stac PORTA
    ldac #E
    stac PORTA
    ldac #0
    stac PORTA

    rsr

print_char:
    stac PORTB
    ldac #RS        ; Set Register Select
    stac PORTA
    ldac #(RS | E)  ; Send enable (E) bit instruction
    stac PORTA
    ldac #RS
    stac PORTA

    rsr

reset_vector:
    .org $fffc
    .word reset
