def encrypt(text,s):
    result = ""
    for i in range(len(text)):
        char = text[i]

        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result

string = "one must see the two suns before the troll can rise"
're.findall("..", string.replace(' ', ''))'

import re

# for j in range(-20, 20):
#     for i in string:
#         print(chr(ord(i)+j), end='')
#     print()

for i in range(-14, 12):
    print(encrypt(string,i))
