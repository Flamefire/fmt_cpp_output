#!/usr/bin/env python3

from fmt_cpp_output import *
    
if __name__ == "__main__":
    for line in sys.stdin:
        print(formatTypes(cleanStd(colorFilenames(line))), end='', flush = True)


