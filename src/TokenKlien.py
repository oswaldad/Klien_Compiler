from enum import Enum

class TokenType(Enum):
    operator    = 0
    punct       = 1
    number      = 2
    keyword     = 3
    identifier  = 4
    boolean     = 5
    eof         = 6

class Token:

    def __init__(self, tokenType, tokenValue = None):
        self.tokenType = tokenType
        self.tokenValue = tokenValue
    
    def isOperator(self):
        return self.tokenType == TokenType.operator

    def isPunct(self):
        return self.tokenType == TokenType.punct

    def isNumber(self):
        return self.tokenType == TokenType.number

    def isKeyword(self):
        return self.tokenType == TokenType.keyword

    def isIdentifier(self):
        return self.tokenType == TokenType.identifier

    def isBoolean(self):
        return self.tokenType == TokenType.boolean

    def isEof(self):
        return self.tokenType == TokenType.eof
    
    def value(self):
        return self.tokenValue

    def __repr__(self):
        if self.isOperator():
            return "Operator = " + self.tokenValue
        elif self.isPunct():
            return "Punctuation = " + self.tokenValue
        elif self.isNumber():
            return "Number = " + str(self.tokenValue)
        elif self.isKeyword():
            return "Keyword = " + self.tokenValue
        elif self.isIdentifier():
            return "Identifier = " + self.tokenValue
        elif self.isBoolean():
            return "Boolean = " + self.tokenValue
        else:
            return "End of File"