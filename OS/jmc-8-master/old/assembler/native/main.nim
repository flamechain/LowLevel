import sequtils, strutils, os, parseopt2
import "../../common/jmc"
import "../common/assembler"

const usage = """
JMC-8 Assembler v1.0 by Jonathan Henrisken <jh@jhenriksen.net>

Usage:
    jmcasm [FILENAME] <OPTIONS>

    -h or --help    .. prints this dialog

    --o:[file]
    --out:[file]    .. specifies output file

    --v
    --verbose       .. runs the assembler in verbose output mode

    --f:[opt]
    --format:[opt]
        Where [opt] is one of:
            "binary":       '.bin' file -- default
            "logisim":      Logisim formatted image file
            "logisim16":    Logisim formatted image file, 16-bit words
"""

type
    OutputFormat {.pure.} = enum
        Binary, Logisim, Logisim16

proc error(message: string): void =
    echo "Error: " & message
    quit(1)

proc printUsage(): void =
    echo usage
    quit()

proc output(format: OutputFormat, result: seq[uint8], file: string): void =
    let filename = splitFile(file)[1] & (case format
        of OutputFormat.Binary: ".bin"
        of OutputFormat.Logisim, OutputFormat.Logisim16: ".logisim")

    case format
    of OutputFormat.Binary:
        writefile(filename, result.mapIt(it.char).join())
    of OutputFormat.Logisim:
        writeFile(filename, "v2.0 raw\n" & result.mapIt(toHex(it.int, 2) & "\n").join())
    of OutputFormat.Logisim16:
        var result16 = newSeq[uint16]()
        for i in 0..(result.len div 2)-1:
            result16 &= uint16((result[i * 2 + 1].int shl 8) or result[i * 2 + 0].int)
        writeFile(filename, "v2.0 raw\n" & result16.mapIt(toHex(it.int, 4) & "\n").join())
var
    outputFormat = OutputFormat.Binary
    inputFile: string = nil
    outputFile: string = nil
    verbose: bool = false

for kind, key, value in getopt():
    case kind
    of cmdArgument:
        if inputFile == nil:
            inputFile = key
        else:
            error("More than one input file specified")
    of cmdLongOption, cmdShortOption:
        case key
        of "help", "h":
            printUsage()
        of "out", "o":
            outputFile = value
        of "verbose", "v":
            verbose = true
        of "format", "f":
            try: outputFormat = parseEnum[OutputFormat](value)
            except: error("Unknown output format")
        else:
            echo "Error: Unrecognized option " & key
            printUsage()
    else:
        assert(false)

if inputFile == nil:
    error("No input file specified")

let result = assemble(inputFile, readFile(inputFile))
output(outputFormat, result, file=(if outputfile != nil: outputFile else: "out"))