import unittest
from Scanner import *
from TokenKlien import Token, TokenType

class TestScanner(unittest.TestCase):

    def testAllTokens(self):
        testProgram = "3 identifier () : , < + - * / = if"
        answerList = [Token(TokenType.number, 3),Token(TokenType.identifier, "identifier"),
        Token(TokenType.punct, "("),Token(TokenType.punct, ")"),Token(TokenType.punct, ":"),Token(TokenType.punct, ","),Token(TokenType.operator, "<"),
        Token(TokenType.operator, "+"),Token(TokenType.operator, "-"),Token(TokenType.operator, "*"),Token(TokenType.operator, "/"),
        Token(TokenType.operator, "="),Token(TokenType.keyword, "if"),Token(TokenType.eof)]
        scanner = Scanner(testProgram)
        self.assertEqual(scanner.scan(testProgram), answerList)

    def testNumbers(self):
        testProgram = "01"
        scanner = Scanner(testProgram)
        with self.assertRaises(ValueError):
            scanner.scan(testProgram)

    def testNumTooLong(self):
        testProgram = "1000000000000000000000"
        scanner = Scanner(testProgram)
        with self.assertRaises(TypeError):
            scanner.scan(testProgram)
    
    def testNoLeadingNumInID(self):
        testProgram = "3number"
        scanner = Scanner(testProgram)
        with self.assertRaises(ValueError):
            scanner.scan(testProgram)

    def testIdentifierTooLong(self):
        testProgram = "IdentifierIsTooLongfkdsahfkdhsafkjghhfkjdhfdkjshfkjldshfkjhdsjkfhdslkahfdkjsalfdfdsafdfdshfgdjksgfjhkdgsfjhdsgfajkgdsjhfgdjshgfajdsgfajdsgafdsjlfkjdslkfjdslkajfdskjafdsafkalfjdkjsfjsdahflkdshaffdafds53gkjgjhgkhjgfhgfgjfchgjvhjhkbjkhfhkfhgjvhgfjhkbjkhbbghkvhgjjcgfdgfhvghvhgvkhvjkhbhjhjggfdgdfgfdgdfs"
        scanner = Scanner(testProgram)
        with self.assertRaises(TypeError):
            scanner.scan(testProgram)
            
    def testValidId(self):
        testProgram = "A_valid_Id_123"
        answer = [Token(TokenType.identifier, "A_valid_Id_123"),Token(TokenType.eof)]
        scanner = Scanner(testProgram)
        self.assertEqual(scanner.scan(testProgram), answer)

    def testComments(self):
        testProgram = "(*A_valid_Id_123*)"
        answer = [Token(TokenType.eof)]
        scanner = Scanner(testProgram)
        self.assertEqual(scanner.scan(testProgram), answer)

    def testNoWhiteSpace(self):
        testProgram = "3/5"
        answer = [Token(TokenType.number, 3), Token(TokenType.operator, "/"), Token(TokenType.number, 5), Token(TokenType.eof)]
        scanner = Scanner(testProgram)
        self.assertEqual(scanner.scan(testProgram), answer)





if __name__ == '__main__':
    unittest.main()