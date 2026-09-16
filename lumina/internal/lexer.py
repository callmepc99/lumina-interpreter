import enum

class TokenType(enum.Enum):
    LET = "LET"
    FN = "FN"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    RETURN = "RETURN"
    IDENT = "IDENT"
    INT = "INT"
    STRING = "STRING"
    TRUE = "TRUE"
    FALSE = "FALSE"
    PRINT = "PRINT"
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    ASTERISK = "*"
    SLASH = "/"
    EQ = "=="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    AND = "&&"
    OR = "||"
    BANG = "!"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    COMMA = ","
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

class Lexer:
    KEYWORDS = {
        "let": TokenType.LET,
        "fn": TokenType.FN,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "return": TokenType.RETURN,
        "print": TokenType.PRINT,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
    }

    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.col = 1
        self.current_char = self.source[self.pos] if self.source else None

    def advance(self):
        if self.current_char == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos += 1
        self.current_char = self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self):
        peek_pos = self.pos + 1
        return self.source[peek_pos] if peek_pos < len(self.source) else None

    def skip_whitespace_and_semicolons(self):
        while self.current_char is not None and (self.current_char.isspace() or self.current_char == ";"):
            self.advance()

    def number(self, start_line, start_col):
        num_str = ""
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token(TokenType.INT, num_str, start_line, start_col)

    def identifier(self, start_line, start_col):
        ident_str = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            ident_str += self.current_char
            self.advance()
        return Token(self.KEYWORDS.get(ident_str, TokenType.IDENT), ident_str, start_line, start_col)

    def string_literal(self, start_line, start_col):
        self.advance()
        str_val = ""
        while self.current_char is not None and self.current_char != "\"":
            str_val += self.current_char
            self.advance()
        self.advance()
        return Token(TokenType.STRING, str_val, start_line, start_col)

    def next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace() or self.current_char == ";":
                self.skip_whitespace_and_semicolons()
                continue
            start_line, start_col = self.line, self.col
            if self.current_char.isalpha() or self.current_char == "_":
                return self.identifier(start_line, start_col)
            if self.current_char.isdigit():
                return self.number(start_line, start_col)
            if self.current_char == "\"":
                return self.string_literal(start_line, start_col)
            if self.current_char == "=":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TokenType.EQ, "==", start_line, start_col)
                self.advance()
                return Token(TokenType.ASSIGN, "=", start_line, start_col)
            if self.current_char == "&":
                if self.peek() == "&":
                    self.advance()
                    self.advance()
                    return Token(TokenType.AND, "&&", start_line, start_col)
            if self.current_char == "|":
                if self.peek() == "|":
                    self.advance()
                    self.advance()
                    return Token(TokenType.OR, "||", start_line, start_col)
            if self.current_char == "!":
                self.advance()
                return Token(TokenType.BANG, "!", start_line, start_col)
            if self.current_char == "<":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TokenType.LTE, "<=", start_line, start_col)
                self.advance()
                return Token(TokenType.LT, "<", start_line, start_col)
            if self.current_char == ">":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TokenType.GTE, ">=", start_line, start_col)
                self.advance()
                return Token(TokenType.GT, ">", start_line, start_col)
            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+", start_line, start_col)
            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-", start_line, start_col)
            if self.current_char == "*":
                self.advance()
                return Token(TokenType.ASTERISK, "*", start_line, start_col)
            if self.current_char == "/":
                self.advance()
                return Token(TokenType.SLASH, "/", start_line, start_col)
            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(", start_line, start_col)
            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")", start_line, start_col)
            if self.current_char == "{":
                self.advance()
                return Token(TokenType.LBRACE, "{", start_line, start_col)
            if self.current_char == "}":
                self.advance()
                return Token(TokenType.RBRACE, "}", start_line, start_col)
            if self.current_char == "[":
                self.advance()
                return Token(TokenType.LBRACKET, "[", start_line, start_col)
            if self.current_char == "]":
                self.advance()
                return Token(TokenType.RBRACKET, "]", start_line, start_col)
            if self.current_char == ",":
                self.advance()
                return Token(TokenType.COMMA, ",", start_line, start_col)
            
            self.advance()
            return Token(TokenType.ILLEGAL, self.current_char, start_line, start_col)
        return Token(TokenType.EOF, "", self.line, self.col)
