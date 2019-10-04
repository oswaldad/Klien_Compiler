#!/usr/bin/env python3

from Parser import *
from sys import argv

kleinProgram = argv[1]
file = open(kleinProgram, 'r')
program = file.read()

try:
    scanner = Scanner(program)
    scanner.scan(program)
    parser = Parser(scanner)
    parser.parse()
    print("Valid Program")
except TypeError as err:
    print(err)
        
except ValueError as err:
    print(err)




