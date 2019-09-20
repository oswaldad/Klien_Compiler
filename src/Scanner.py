from enum import Enum
from TokenKlien import Token, TokenType

class State(Enum):
    start       = 0
    operator    = 1
    punct       = 2
    zero        = 3
    number      = 4
    identifier  = 5
    comment     = 6

class Scanner:
    """
    Read tokens from input program
    """

    def __init__(self, programStr):
        self.programStr = programStr
        self.pos = 0
      #  self.tokens = self.scan(self.programStr)
        self.tokens = []


    def scan(self, programStr):
        keywords = {"integer" : "Keyword", "boolean" : "Keyword", "if" : "Keyword", "then" : "Keyword", "else" : "Keyword", "not" : "Keyword", "and" : "Keyword", "or" : "Keyword", "function" : "Keyword", "main" : "Identifier", "print" : "Identifier", "true" : "Boolean", "false" : "Boolean"}
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lineCounter = 1
        punct = "(),:"
        operators = "+-*/<="
        accum = ""
        state = State.start
        tokens = []
        strPos = 0
        while strPos < len(programStr):
            if state == State.start:
                if programStr[strPos].isspace():
                    if programStr[strPos] == "\n":
                        lineCounter += 1
                    pass
                elif programStr[strPos] in operators:
                    tokens.append(Token(TokenType.operator,programStr[strPos]))
                elif programStr[strPos] in "),:":
                    tokens.append(Token(TokenType.punct,programStr[strPos]))
                elif programStr[strPos] in "0":
                    accum = programStr[strPos]
                    state = State.zero
                elif programStr[strPos] in "123456789":
                    accum = programStr[strPos]
                    state = State.number
                elif programStr[strPos] in alphabet:
                    accum = programStr[strPos]
                    state = State.identifier
                elif programStr[strPos] == "(":
                    if strPos < len(programStr) -1 and programStr[strPos+1] == "*":
                        state = State.comment
                        strPos += 1
                    else:
                        tokens.append(Token(TokenType.punct,programStr[strPos]))
                else: #Character not exceptable in the language
                    errorMessage = 'Error line {} : Invalid character in program {}'
                    raise ValueError(errorMessage.format(lineCounter, programStr[strPos]))
                strPos += 1

            elif state == State.zero:
                if programStr[strPos].isspace():
                    if programStr[strPos] == "\n":
                        lineCounter += 1
                    tokens.append(Token(TokenType.number, int(accum)))
                elif programStr[strPos] in (operators + punct):
                    tokens.append(Token(TokenType.number, int(accum)))
                    strPos -= 1
                elif programStr[strPos].isdigit():
                    errorMessage = 'Error line {} : Numbers cannot have a leading 0: 0{}'
                    raise ValueError(errorMessage.format(lineCounter, programStr[strPos]))
                else:
                    errorMessage = 'Error line {} : Invalid character after 0: 0{}'
                    raise ValueError(errorMessage.format(lineCounter, programStr[strPos]))
                accum = ""
                state = State.start
                strPos += 1

            elif state == State.number:
                if programStr[strPos].isdigit():
                    accum += programStr[strPos]
                    strPos += 1
                elif programStr[strPos].isspace():
                    if programStr[strPos] == "\n":
                        lineCounter += 1
                    if int(accum) <= 2147483647:
                        tokens.append(Token(TokenType.number, int(accum)))
                        accum = ""
                        state = State.start
                        strPos += 1
                    else:
                        errorMessage = 'Error line {} : Number cannot be over 2^31 - 1 {}'
                        raise TypeError(errorMessage.format(lineCounter, accum))
                elif programStr[strPos] in (operators + punct):
                    if int(accum) <= 2147483647:
                        tokens.append(Token(TokenType.number, int(accum)))
                        accum = ""
                        state = State.start
                    else:
                        errorMessage = 'Error line {} : Number cannot be over 2^31 - 1 {}'
                        raise TypeError(errorMessage.format(lineCounter, accum))
                else:
                    errorMessage = 'Error line {} : Invalid character in number  {}*{}*'
                    raise ValueError(errorMessage.format(lineCounter, accum, programStr[strPos]))

            elif state == State.identifier:
                if programStr[strPos] in (alphabet + "_1234567890"):
                    accum += programStr[strPos]
                    strPos += 1
                elif programStr[strPos].isspace():
                    if programStr[strPos] == "\n":
                        lineCounter += 1
                    if len(accum) <= 256:
                        if accum in keywords:
                            type = keywords[accum]
                            if type == "Keyword":
                                tokens.append(Token(TokenType.keyword, accum))
                            elif type == "Boolean":
                                tokens.append(Token(TokenType.boolean, accum))
                            else:
                                tokens.append(Token(TokenType.identifier, accum))
                        else:
                            tokens.append(Token(TokenType.identifier, accum))
                    else:
                        errorMessage = 'Error line {} : String cannot be over 256 characters {}'
                        raise TypeError(errorMessage.format(lineCounter, accum))
                    accum = ""
                    strPos += 1
                    state = State.start
                elif programStr[strPos] in (operators + punct):
                    if len(accum) <= 256:
                        if accum in keywords:
                            type = keywords[accum]
                            if type == "Keyword":
                                tokens.append(Token(TokenType.keyword, accum))
                            elif type == "Boolean":
                                tokens.append(Token(TokenType.boolean, accum))
                            else:
                                tokens.append(Token(TokenType.identifier, accum))
                        else:
                            #TBD add identifier to keywords dictionary
                            tokens.append(Token(TokenType.identifier, accum))
                    else:
                        errorMessage = 'Error line {} : String cannot be over 256 characters {}'
                        raise TypeError(errorMessage.format(lineCounter, accum))
                    accum = ""
                    state = State.start
                
                else:
                    errorMessage = 'Error line {} : Invalid character in string  {}*{}*'
                    raise ValueError(errorMessage.format(lineCounter, accum, programStr[strPos]))

            elif state == State.comment:
                if programStr[strPos] == "\n":
                    lineCounter += 1
                if programStr[strPos] == "*":
                    if strPos < len(programStr) -1 and programStr[strPos+1] == ")":
                        strPos += 1
                        state = State.start
                strPos += 1
            else:
                    errorMessage = 'Invalid state {}'
                    raise TypeError(errorMessage.format(state))
        #Handles accum at the end of the file
        if accum != "":
            if state == State.zero:
                tokens.append(Token(TokenType.number, int(accum)))
            elif state == State.number:
                if int(accum) <= 2147483647:
                    tokens.append(Token(TokenType.number, int(accum)))
                else:
                    errorMessage = 'Error line {} : Number cannot be over 2^31 - 1 {}'
                    raise TypeError(errorMessage.format(lineCounter, accum))
            elif state == State.identifier:
                if len(accum) <= 256:
                    if accum in keywords:
                        type = keywords[accum]
                        if type == "Keyword":
                            tokens.append(Token(TokenType.keyword, accum))
                        elif type == "Boolean":
                            tokens.append(Token(TokenType.boolean, accum))
                        else:
                            tokens.append(Token(TokenType.identifier, accum))
                    else:
                        #TBD add identifier to keywords dictionary
                        tokens.append(Token(TokenType.identifier, accum))
                else:
                    errorMessage = 'Error line {} : String cannot be over 256 characters {}'
                    raise TypeError(errorMessage.format(lineCounter, accum))
            else: 
                errorMessage = 'Invalid state {} with this accum {}'
                raise TypeError(errorMessage.format(state, accum))

        if state == State.comment:
                errorMessage = 'Comment was never close {}'
                raise TypeError(errorMessage.format(state))

        tokens.append(Token(TokenType.eof))
        return tokens

    def next(self):
        nextToken = self.tokens[self.pos]
        self.pos += 1
        return nextToken
    
    def peek(self):
        return self.tokens[self.pos]
    
def print_one(klienProgram):
    file = open(klienProgram, 'r')
    program = file.read()
    demoScanner = Scanner(program)

    tokens = demoScanner.scan(program)
    for token in tokens:
        print(token)

"""
#used for testing

if __name__ == '__main__':
    try:
        print_one()
    except TypeError as err:
        print(err)
    except ValueError as err:
        print(err)
"""
    
