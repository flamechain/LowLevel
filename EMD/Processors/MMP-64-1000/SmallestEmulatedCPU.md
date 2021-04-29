# Worlds Smallest Emulated CPU (Turing Complete) - 189 Characters

Limiations

- Needs to keep outside names (e.g. cant rename the RAM class variables)
- Public functions need understandable names
- Needs to be called identically to original

External Calling:

```py
cpu = CPU()
ram = RAM()
cpu.On(ram) # NOT cpu.On(ram.data), or cpu.O(ram)
```

## Explanation

Original with shrinking (no abstraction)

```py
class CPU:
    def __init__(self):
        self.PC=0

    def __Fetch(self, mem):
        value=None if self.PC>=len(mem)else mem[self.PC];self.PC+=1;return value

    def __Read(self, loc, mem):
        return mem[loc]

    def __Write(self, loc, val, mem):
        mem[loc]=val

    def Start(self, mem):
        while True:
            op1=self.__Fetch(mem.data)
            if op1 is None:
                return

            op2=self.__Fetch(mem.data)
            if op2 is None:
                return

            addr=self.__Fetch(mem.data)
            if addr is None:
                return

            res=self.__Read(op1,mem.data)-self.__Read(op2,mem.data);self.PC=addr if res<0 else self.PC;self.__Write(op1,res,mem.data)
```

When the CPU is called, it has a infinite loop that fetches the next 3 bytes. It does the logic:

```vb
op1 -= op2

if op1 & 0b10000000 ' Checks if sign bit is on
    goto op3
```

This is turing complete because you can control branching on a condition. Here is how to do a simple MOV instruction:

```txt
MOV EBX, EAX
```

```asm
EAX byte 7
EBX byte 3
Z   byte 0

SUBLEQ EBX, EBX, $+3
SUBLEQ Z, EAX, $+3
SUBLEQ EBX, Z, $+3
SUBLEQ Z, Z, $+3
```

This MOV instruction is now 4 instructions:

- First it makes EBX 0, the $+3 is just to jump to the next instruction if a branch somehow happens, and should always be this unless trying to branch.
- Next, Z becomes the oposite of EAX, because 0-EAX = -EAX.
- Finally, you subtract the oposite of EAX from EBX (now 0), so EBX = 0--7 = 0+7.
- The Z-Z is just to zero out Z for further use in helping instructions.

This is to prove that this is turing complete. You can MOV, ADD, SUB, JMP, and JL.

## Shrinking Methods

First you take out the unecessary whitespace.

```py
class CPU:
 def __init__(self):self.PC=0
 def __Fetch(self,mem):value=None if self.PC>=len(mem)else mem[self.PC];self.PC+=1;return value
 def __Read(self,loc,mem):return mem[loc]
 def __Write(self,loc,val,mem):mem[loc]=val
 def Start(self,mem):
  while True:
   op1=self.__Fetch(mem.data)
   if op1 is None:return
   op2=self.__Fetch(mem.data)
   if op2 is None:return
   addr=self.__Fetch(mem.data)
   if addr is None:return
   res=self.__Read(op1,mem.data)-self.__Read(op2,mem.data);self.PC=addr if res<0 else self.PC;self.__Write(op1,res,mem.data)
```

The next step is to strip out the unecessary functions including `__init__`, `__Read`, and `__Write` as they are only used once or twice. You can take out `__init__` by just placing the one class variable outside any functions.

```py
class CPU:
 PC=0
 def __Fetch(self,mem):value=None if self.PC>=len(mem)else mem[self.PC];self.PC+=1;return value
 def Start(self,mem):
  while True:
   op1=self.__Fetch(mem.data)
   if op1 is None:return
   op2=self.__Fetch(mem.data)
   if op2 is None:return
   addr=self.__Fetch(mem.data)
   if addr is None:return
   res=mem.data[op1]-mem.data[op2];self.PC=addr if res<0 else self.PC;mem.data[op1]=res
```

The next step is to optimize the program by wrapping the program counter instead of returning, making all of the `if x is None:return` statements useless, and saving a lot of lines and characters.

```py
class CPU:
 PC=0
 def __Fetch(self,mem):
  value=mem[self.PC]
  if self.PC>=len(mem):self.PC=0
  else:self.PC+=1
  return value
 def Start(self,mem):
  while True:
   op1=self.__Fetch(mem.data)
   op2=self.__Fetch(mem.data)
   addr=self.__Fetch(mem.data)
   res=mem.data[op1]-mem.data[op2];self.PC=addr if res<0 else self.PC;mem.data[op1]=res
```

Then quickly replace the unecessary whitespace again by using semicolons and replacing `__Fetch` with a one liner using a refactored one-line if-else statement.

```py
class CPU:
 PC=0
 def __Fetch(self,mem):value=mem[self.PC];self.PC+=1if self.PC<len(mem)else-self.PC;return value
 def Start(self,mem):
  while True:op1=self.__Fetch(mem.data);op2=self.__Fetch(mem.data);addr=self.__Fetch(mem.data);res=mem.data[op1]-mem.data[op2];self.PC=addr if res<0 else self.PC;mem.data[op1]=res
```

This can turn the while loop into a one-liner. The `__Fetch` works by incrementing if in range of memory, or subtracting itself (going 0) otherwise (wrapping back to the first address). We also use a trick where you can put keywords directly after numbers (`self.PC+=1if...`).

There are only a few major changes, then its up to subtle changes and minification and abstraction. First we rework the while loop to shrink the number of times we are creating variables that are only used once.

```py
class CPU:
 PC=0
 def __Fetch(self,mem):value=mem[self.PC];self.PC+=1if self.PC<len(mem)else-self.PC;return value
 def Start(self,mem):
  while True:op1=self.__Fetch(mem.data);mem.data[op1]-=mem.data[self.__Fetch(mem.data)];addr=self.__Fetch(mem.data);self.PC=addr if mem.data[op1]<0else self.PC
```

We rework it by subtracting directly from the location of op1, then looking back at the location for the branch instead of storing the result inside a variable.

Thats the last of the big changes, so now its time to minify. Heres a minified version with a key:

```py
# PC -> p
# op1 -> a
# addr -> l (for location)
# __Fetch -> f (no longer private)
# Start -> On (still makes sense, but shorter)
# mem -> m
# value -> v

class CPU:
 p=0
 def f(self,m):v=m[self.p];self.p+=1if self.p<len(m)else-self.p;return v
 def On(self,m):
  while 1:a=self.f(m.data);m.data[a]-=m.data[self.f(m.data)];l=self.f(m.data);self.p=l if m.data[a]<0else self.p
```

The `True` keyword was also replaced by a 1.

Next its time to replace some commonly used variables with shortcuts. For example, adding a `f=self.f` statement will save characters in the end. We can also do this with the memory, and the program counter in the `f()` function, where we are only reading.

```py
class CPU:
 p=0
 def f(self,m):p=self.p;v=m[p];self.p+=1if p<len(m)else-p;return v
 def On(self,m):
  m=m.data;f=self.f
  while 1:a=f(m);m[a]-=m[f(m)];l=f(m);self.p=l if m[a]<0else self.p
```

We cant do this with self.p though because we are changing the value, not reading.

The final change is to replace `len(m)` with 255, because since we only have 1 byte addressing, we are probably fine to assume that there is full memory.

```py
class CPU:
 p=0
 def f(self,m):p=self.p;v=m[p];self.p+=1if p<255else-p;return v
 def On(self,m):
  m=m.data;f=self.f
  while 1:a=f(m);m[a]-=m[f(m)];l=f(m);self.p=l if m[a]<0else self.p
```

Now we have a 189 character turing complete CPU, with major optimizations. This version is 5.5 times smaller than the original, and has better functionality.
