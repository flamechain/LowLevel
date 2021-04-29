# Package

version       = "0.1.0"
author        = "Jonathan Henriksen"
description   = "JMC-8 assembler"
license       = "MIT"

# Dependencies

requires "nim >= 0.16.0"

task buildnative, "Builds the assembler":
    exec "nim c --out:./jmcasm.exe native/main.nim"

task buildjs, "Builds the assembler in Javascript":
    exec "nim js -d:nodejs js/main.nim"

task test, "Runs unit tests":
    exec "nim --run c common/test.nim"