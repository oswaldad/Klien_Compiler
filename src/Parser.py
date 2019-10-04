from enum import Enum
from TokenKlien import Token, TokenType
from Scanner import *

class NonTerminal(Enum):
    PROGRAM                     = 0
    DEFINITIONS                 = 1
    DEF                         = 2
    FORMALS                     = 3
    NONEMPTYFORMALS             = 4
    NONEMPTYFORMALS_TAIL        = 5
    FORMAL                      = 6
    BODY                        = 7
    TYPE                        = 8
    EXPR                        = 9
    EXPR_TAIL                   = 10
    SIMPLE_EXPR                 = 11
    SIMPLE_EXPR_TAIL            = 12
    TERM                        = 13
    TERM_TAIL                   = 14
    FACTOR                      = 15
    FACTOR_TAIL                 = 16
    ACTUALS                     = 17
    NONEMPTYACTUALS             = 18
    NONEMPTYACT_TAIL            = 19
    LITERAL                     = 20
    PRINT_STATEMENT             = 21


parseTable = {
    (NonTerminal.PROGRAM, "function") : [NonTerminal.DEFINITIONS],
    (NonTerminal.PROGRAM, TokenType.eof) : [NonTerminal.DEFINITIONS],
    (NonTerminal.DEFINITIONS, "function") : [NonTerminal.DEF, NonTerminal.DEFINITIONS],
    (NonTerminal.DEFINITIONS, TokenType.eof) : [],
    (NonTerminal.DEF, "function") : [Token(TokenType.keyword, "function"), Token(TokenType.identifier, ""),
    Token(TokenType.punct, "("), NonTerminal.FORMALS, Token(TokenType.punct, ")"), Token(TokenType.punct, ":"),
    NonTerminal.TYPE, NonTerminal.BODY],
    (NonTerminal.FORMALS, ")") : [],
    (NonTerminal.FORMALS, TokenType.identifier) : [NonTerminal.NONEMPTYFORMALS],
    (NonTerminal.NONEMPTYFORMALS, TokenType.identifier) : [NonTerminal.FORMAL, NonTerminal.NONEMPTYFORMALS_TAIL],
    (NonTerminal.NONEMPTYFORMALS_TAIL, ",") : [Token(TokenType.punct, ","), NonTerminal.NONEMPTYFORMALS],
    (NonTerminal.NONEMPTYFORMALS_TAIL, ")") : [],
    (NonTerminal.FORMAL, TokenType.identifier) : [Token(TokenType.identifier, ""), Token(TokenType.punct, ":"), NonTerminal.TYPE],
    (NonTerminal.BODY, "-") : [NonTerminal.EXPR],
    (NonTerminal.BODY, "(") : [NonTerminal.EXPR],
    (NonTerminal.BODY, "if") : [NonTerminal.EXPR],
    (NonTerminal.BODY, "not") : [NonTerminal.EXPR],
    (NonTerminal.BODY, "print") : [NonTerminal.PRINT_STATEMENT , NonTerminal.BODY],
    (NonTerminal.BODY, TokenType.number) : [NonTerminal.EXPR],
    (NonTerminal.BODY, TokenType.boolean) : [NonTerminal.EXPR],
    (NonTerminal.BODY, TokenType.identifier) : [NonTerminal.EXPR],
    (NonTerminal.TYPE, "integer") : [Token(TokenType.keyword, "integer")],
    (NonTerminal.TYPE, "boolean") : [Token(TokenType.keyword, "boolean")],
    (NonTerminal.EXPR, "-") : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, "(") : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, "if") : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, "not") : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, TokenType.number) : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, TokenType.boolean) : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR, TokenType.identifier) : [NonTerminal.SIMPLE_EXPR, NonTerminal.EXPR_TAIL],
    (NonTerminal.EXPR_TAIL, "<") : [Token(TokenType.operator, "<"), NonTerminal.EXPR],
    (NonTerminal.EXPR_TAIL, "=") : [Token(TokenType.operator, "="), NonTerminal.EXPR],
    (NonTerminal.EXPR_TAIL, "+") : [],
    (NonTerminal.EXPR_TAIL, "-") : [],
    (NonTerminal.EXPR_TAIL, "*") : [],
    (NonTerminal.EXPR_TAIL, "/") : [],
    (NonTerminal.EXPR_TAIL, ",") : [],
    (NonTerminal.EXPR_TAIL, ")") : [],
    (NonTerminal.EXPR_TAIL, "and") : [],
    (NonTerminal.EXPR_TAIL, "function") : [],
    (NonTerminal.EXPR_TAIL, "then") : [],
    (NonTerminal.EXPR_TAIL, "else") : [],
    (NonTerminal.EXPR_TAIL, TokenType.eof) : [],
    (NonTerminal.SIMPLE_EXPR, "-") : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, "(") : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, "if") : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, "not") : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, TokenType.number) : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, TokenType.boolean) : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR, TokenType.identifier) : [NonTerminal.TERM, NonTerminal.SIMPLE_EXPR_TAIL],
    (NonTerminal.SIMPLE_EXPR_TAIL, "+") : [Token(TokenType.operator, "+"), NonTerminal.SIMPLE_EXPR],
    (NonTerminal.SIMPLE_EXPR_TAIL, "-") : [Token(TokenType.operator, "-"), NonTerminal.SIMPLE_EXPR],
    (NonTerminal.SIMPLE_EXPR_TAIL, "or") : [Token(TokenType.keyword, "or"), NonTerminal.SIMPLE_EXPR],
    (NonTerminal.SIMPLE_EXPR_TAIL, "<") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "=") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "*") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "/") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, ",") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, ")") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "and") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "function") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "then") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, "else") : [],
    (NonTerminal.SIMPLE_EXPR_TAIL, TokenType.eof) : [],
    (NonTerminal.TERM, "-") : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, "(") : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, "if") : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, "not") : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, TokenType.number) : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, TokenType.boolean) : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM, TokenType.identifier) : [NonTerminal.FACTOR, NonTerminal.TERM_TAIL],
    (NonTerminal.TERM_TAIL, "*") : [Token(TokenType.operator, "*"), NonTerminal.TERM],
    (NonTerminal.TERM_TAIL, "/") : [Token(TokenType.operator, "/"), NonTerminal.TERM],
    (NonTerminal.TERM_TAIL, "and") : [Token(TokenType.keyword, "and"), NonTerminal.TERM],
    (NonTerminal.TERM_TAIL, "<") : [],
    (NonTerminal.TERM_TAIL, "+") : [],
    (NonTerminal.TERM_TAIL, "-") : [],
    (NonTerminal.TERM_TAIL, ",") : [],
    (NonTerminal.TERM_TAIL, ")") : [],
    (NonTerminal.TERM_TAIL, "=") : [],
    (NonTerminal.TERM_TAIL, "or") : [],
    (NonTerminal.TERM_TAIL, "function") : [],
    (NonTerminal.TERM_TAIL, "then") : [],
    (NonTerminal.TERM_TAIL, "else") : [],
    (NonTerminal.TERM_TAIL, TokenType.eof) : [],
    (NonTerminal.FACTOR, "-") : [Token(TokenType.operator, "-"), NonTerminal.FACTOR],
    (NonTerminal.FACTOR, "not") : [Token(TokenType.keyword, "not"), NonTerminal.FACTOR],
    (NonTerminal.FACTOR, "(") : [Token(TokenType.punct, "("), NonTerminal.EXPR, Token(TokenType.punct, ")") ],
    (NonTerminal.FACTOR, "if") : [Token(TokenType.keyword, "if"), NonTerminal.EXPR, Token(TokenType.keyword, "then"), NonTerminal.EXPR, Token(TokenType.keyword, "else"), NonTerminal.EXPR],
    (NonTerminal.FACTOR, TokenType.number) : [NonTerminal.LITERAL],
    (NonTerminal.FACTOR, TokenType.boolean) : [NonTerminal.LITERAL],
    (NonTerminal.FACTOR, TokenType.identifier) : [Token(TokenType.identifier,""), NonTerminal.FACTOR_TAIL],
    (NonTerminal.FACTOR_TAIL, "(") : [Token(TokenType.punct, "("), NonTerminal.ACTUALS, Token(TokenType.punct, ")") ],
    (NonTerminal.FACTOR_TAIL, "<") : [],
    (NonTerminal.FACTOR_TAIL, "=") : [],
    (NonTerminal.FACTOR_TAIL, "+") : [],
    (NonTerminal.FACTOR_TAIL, "-") : [],
    (NonTerminal.FACTOR_TAIL, "*") : [],
    (NonTerminal.FACTOR_TAIL, "/") : [],
    (NonTerminal.FACTOR_TAIL, ",") : [],
    (NonTerminal.FACTOR_TAIL, ")") : [],
    (NonTerminal.FACTOR_TAIL, "and") : [],
    (NonTerminal.FACTOR_TAIL, "or") : [],
    (NonTerminal.FACTOR_TAIL, "function") : [],
    (NonTerminal.FACTOR_TAIL, "then") : [],
    (NonTerminal.FACTOR_TAIL, "else") : [],
    (NonTerminal.FACTOR_TAIL, TokenType.eof) : [],
    (NonTerminal.ACTUALS, "-") : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, "(") : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, "if") : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, "not") : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.number) : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.boolean) : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.ACTUALS, TokenType.identifier) : [NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACTUALS, "-") : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, "(") : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, "if") : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, "not") : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, TokenType.number) : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, TokenType.boolean) : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACTUALS, TokenType.identifier) : [NonTerminal.EXPR, NonTerminal.NONEMPTYACT_TAIL],
    (NonTerminal.NONEMPTYACT_TAIL, ",") : [Token(TokenType.punct, ","), NonTerminal.NONEMPTYACTUALS],
    (NonTerminal.NONEMPTYACT_TAIL, ")") : [],
    (NonTerminal.LITERAL, TokenType.number) : [Token(TokenType.number, 0)],
    (NonTerminal.LITERAL, TokenType.boolean) : [Token(TokenType.boolean, "true")],
    (NonTerminal.PRINT_STATEMENT, "print") : [Token(TokenType.identifier,"print"), Token(TokenType.punct, "("), NonTerminal.EXPR, Token(TokenType.punct, ")") ]
}







def top(stack):
    return stack[-1]

def pop(stack):
    stack.pop()

def pushRule(rule, stack):
    for element in reversed(rule):
        stack.append(element)


class Parser:

    def __init__(self, scanner):
      self.scanner = scanner

    def parse(self):
        stack = []
        pushRule( [ NonTerminal.PROGRAM, Token(TokenType.eof) ], stack)
        while stack:
        #    print("Stack = " + str(stack))
       #     print("NextToken = " + str(self.scanner.peek()))
            tos = top(stack) 
            if isinstance(tos, Token):
                token = self.scanner.next()
                # Checking if values are the same. Used punctuations, operators, and keywords
                if tos.getTokenType() == TokenType.punct or tos.getTokenType() == TokenType.operator or tos.getTokenType() == TokenType.keyword:
                    if tos.value() == token.value():
                        pop(stack)
                    else:
                        errorMessage = 'Error: Expected  {}  but received {}'
                        raise TypeError(errorMessage.format(tos.value(), token.value()))
                # Checking if an identifier is print. Used in the print-statement rule.
                elif token.value() == "print":
                    if tos.value() == token.value():
                        pop(stack)
                    else:
                        errorMessage = 'Error: Expected  {}  but received {}'
                        raise TypeError(errorMessage.format(tos.value(), token.value()))
                # Checking if tokenTypes are the same. Used for Numbers, EOF, Booleans, and identifiers that are not print.
                elif tos.getTokenType() == token.getTokenType():
                    pop(stack)
                else:
                    errorMessage = 'Error: Expected  {}  but received {}'
                    raise TypeError(errorMessage.format(tos.getTokenType(), token.getTokenType()))

            elif isinstance(tos, NonTerminal):
                token = self.scanner.peek()
                if token.getTokenType() == TokenType.punct or token.getTokenType() == TokenType.operator or token.getTokenType() == TokenType.keyword:
                    rule = parseTable.get((tos, token.value()))
                elif token.value() == "print":
                    rule = parseTable.get((tos, "print"))
                else:
                    rule = parseTable.get((tos,token.getTokenType()))

                if rule is not None:
                    pop(stack)
                    pushRule(rule, stack)
                else:
                    errorMessage = 'Error: {} cannot be expanded on by {}'
                    raise TypeError(errorMessage.format(tos, token))
            else:
                errorMessage = 'invalid item on stack: {}'
                raise TypeError(errorMessage.format(tos))

        # Checking if there is more tokens after the program was completed.
        if not token.isEof():
            errorMessage = 'Error: unexpected token at end: {}'
            raise TypeError(errorMessage.format(token))

        return True

def testParser(klienProgram):
    file = open(klienProgram, 'r')
    program = file.read()
    demoScanner = Scanner(program)
    demoScanner.scan(program)
    parser = Parser(demoScanner)
    return parser.parse()

if __name__ == '__main__':
    try:
        testParser('klein-programs/farey.kln')
    except TypeError as err:
        print(err)
        
    except ValueError as err:
        print(err)
        
