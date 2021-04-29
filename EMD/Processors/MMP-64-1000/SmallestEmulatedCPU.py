# TO USE:
#
# Make a RAM class and set the memory.
# Call the CPU.On() method, passing in the RAM (not the internal array) on a thread, because it doesn't stop until killed (like a normal CPU).
# You can emulate a HLT instruction by making an infite loop.
#
# Example program (All variables are actually pointers):
# A = 7
# B = 3
# Z = 0
#
# MOV B, A
# HLT
#
# Converts Into:
#
# A = 7
# B = 3
# Z = 0
# HLT1 = -1             ; Actually 255, but sign bit is on
# HLT2 = 0
#
# ; MOV B, A
# SUBLEQ B, B, $+3
# SUBLEQ Z, A, $+3
# SUBLEQ B, Z, $+3
# SUBLEQ Z, Z, $+3
# ; HLT
# SUBLEQ HLT1, HLT2, $  ; Jump back here, this does nothing because it subtracts 0, but the result is still negative
#

'''
Worlds Smallest Emulated Turing Complete CPU (189 Bytes)

Run this file and a simple program will be executed as described above.
'''

import threading
import time

# class CPU:
#  p=0
#  def f(self,m):p=self.p;v=m[p];self.p+=1if p<255else-p;return v
#  def On(self,m):
#   m=m.data;f=self.f
#   while 1:a=f(m);m[a]-=m[f(m)];l=f(m);self.p=l if m[a]<0else self.p

# class CPU:
#  def f(self,m,p):v=m[p[0]];p[0]+=1if p[0]<255else-p[0];return v
#  def On(self,m):
#   m=m.data;f=self.f;p=[0]
#   while 1:a=f(m,p);m[a]-=m[f(m,p)];l=f(m,p);m[a]<0and[p:=[l]]

# 211 Characters (16-bit)
class CPU16:
 def On(s,m):
  m=m.data;p=[0]
  def g():o=p[0];p[0]+=1if o<len(m)else-o;return m[o]
  def f():return g()<<8|g()
  while 1:a=f();r=m[a]-m[f()];l=f();m[a:a+1]=[(r&65280)>>8,r&255];m[a]<0and[p:=[l]]

# 149 Characters (8-bit)
class CPU:
 def On(s,m):
  m=m.data;p=[0]
  def f():o=p[0];p[0]+=1if o<255else-o;return m[o]
  while 1:a=f();m[a]-=m[f()];l=f();m[a]<0and[p:=[l]]

# All code apart from the CPU will be normal and easy to read

class RAM:
    def __init__(self):
        self.data = []
        for _ in range(0xFF):
            self.data.append(0)

cpu = CPU()
ram = RAM()

# Pointers
A = 0x10
B = 0x11
Z = 0x12
H1 = 0x13
H2 = 0x14

# Code
program = [
    # MOV B, A
    B, B, 3,    # 0
    Z, A, 6,    # 3
    B, Z, 9,    # 6
    Z, Z, 12,   # 9
    # HLT
    H1, H2, 12, # 12
]

ram.data[0:len(program)] = program

# Data
ram.data[A] = 7
ram.data[B] = 3
ram.data[Z] = 0
ram.data[H1] = -1
ram.data[H2] = 0

# Total program takes up 20 bytes including variables, 12% of memory.
# I might make a 16-bit version, but it would be much larger even after the same changes.

# Run
cpu_t = threading.Thread(target=cpu.On, args=[ram])
cpu_t.daemon = True # To kill it when program ends

print(ram.data[B]) # 'B' starts as 3 (or anything)

cpu_t.start()
time.sleep(0.1) # To allow for slow computers

print(ram.data[B]) # 'B' now has the contents of 'A' (7)
