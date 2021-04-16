char = "000000010"
total = 0
counter = 100000000

for i in range(9):
    num = ord(char[i]) - 48
    num *= counter
    total += num
    counter //= 10

print(total)
print(chr(''))