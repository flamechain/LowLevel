# Package

version       = "0.1.0"
author        = "Jonathan Henriksen"
description   = "JMC-8 Emulator"
license       = "MIT"

# Dependencies

requires "nim >= 0.16.0"

task buildnative, "Builds the emulator":
    exec "nim c native/main.nim"

task buildjs, "Builds the emulator in Javascript":
    exec "nim c js/main.nim"

task run, "Runs the emulator":
    exec "nim c --run native/main.nim"

task test, "Runs unit tests":
    exec "nim --run c common/test.nim"