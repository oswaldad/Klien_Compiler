#!/usr/bin/env python3

from Scanner import *
from sys import argv

klienProgram = argv[1]

try:
    print_one(klienProgram)
except TypeError as err:
    print(err)
except ValueError as err:
    print(err)