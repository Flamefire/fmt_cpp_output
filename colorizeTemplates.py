#!/usr/bin/env python3

from fmt_cpp_output import *
    
if __name__ == "__main__":
    if sys.__stdin__.isatty():
        for line in sys.argv[1:]:
            print(formatTypes(cleanStd(colorFilenames(line))), end='', flush = True)
        print("")
    else:
        for line in sys.stdin:
            print(formatTypes(cleanStd(colorFilenames(line))), end='', flush = True)


