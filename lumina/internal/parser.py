from internal.lexer import Lexer, TokenType

class Node: pass
class Program(Node):
    def __init__(self): self.statements = []
class LetStatement(Node):
    def __init__(self, name, value): self.name, self.value = name, value
class AssignStatement(Node):
    def __init__(self, name, value): self.name, self.value = name, value
class ReturnStatement(Node):
    def __init__(self, returnValue): self.returnValue = returnValue
class PrintStatement(Node):
    def __init__(self, expression): self.expression = expression
class Identifier(Node):
    def __init__(self, value): self.value = value
class IntegerLiteral(Node):
    def __init__(self, value): self.value = int(value)
class BooleanLiteral(Node):
    def __init__(self, value): self.value = value
class StringLiteral(Node):
    def __init__(self, value): self.value = value
class ArrayLiteral(Node):
    def __init__(self, elements): self.elements = elements
class IndexExpression(Node):
    def __init__(self, left, index): self.left, self.index = left, index
class PrefixExpression(Node):
    def __init__(self, operator, right): self.operator, self.right = operator, right
class InfixExpression(Node):
    def __init__(self, left, operator, right):
        self.left, self.operator, self.right = left, operator, right
class BlockStatement(Node):
    def __init__(self): self.statements = []
class IfExpression(Node):
    def __init__(self, condition, consequence, alternative=None):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative
class WhileExpression(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
class FunctionLiteral(Node):
    def __init__(self, parameters, body):
        self.parameters = parameters
        self.body = body
class CallExpression(Node):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = None
        self.peek_token = None
        self._advance_token()
        self._advance_token()

    def _advance_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> Program:
        program = Program()
        while self.current_token.type != TokenType.EOF:
            stmt = self._parse_statement()
            if stmt:
                program.statements.append(stmt)
            self._advance_token()
        return program

    def _parse_statement(self):
        if self.current_token.type == TokenType.LET:
            return self._parse_let_statement()
        if self.current_token.type == TokenType.RETURN:
            return self._parse_return_statement()
        if self.current_token.type == TokenType.PRINT:
            return self._parse_print_statement()
        if self.current_token.type == TokenType.IDENT and self.peek_token.type == TokenType.ASSIGN:
            return self._parse_assign_statement()
        return self._parse_expression()

    def _parse_let_statement(self):
        self._advance_token()
        name = Identifier(self.current_token.value)
        self._advance_token()
        self._advance_token()
        value = self._parse_expression()
        return LetStatement(name, value)

    def _parse_assign_statement(self):
        name = Identifier(self.current_token.value)
        self._advance_token()
        self._advance_token()
        value = self._parse_expression()
        return AssignStatement(name, value)

    def _parse_return_statement(self):
        self._advance_token()
        val = self._parse_expression()
        return ReturnStatement(val)

    def _parse_print_statement(self):
        self._advance_token()
        self._advance_token()
        expr = self._parse_expression()
        self._advance_token()
        return PrintStatement(expr)

    def _parse_expression(self):
        left = self._parse_term()
        ops = (TokenType.PLUS, TokenType.MINUS, TokenType.EQ, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE, TokenType.AND, TokenType.OR)
        while self.peek_token.type in ops:
            op = self.peek_token
            self._advance_token()
            self._advance_token()
            right = self._parse_term()
            left = InfixExpression(left, op.value, right)
        return left

    def _parse_term(self):
        left = self._parse_factor()
        while self.peek_token.type in (TokenType.ASTERISK, TokenType.SLASH):
            op = self.peek_token
            self._advance_token()
            self._advance_token()
            right = self._parse_factor()
            left = InfixExpression(left, op.value, right)
        return left

    def _parse_factor(self):
        token = self.current_token
        if token.type == TokenType.BANG:
            self._advance_token()
            return PrefixExpression("!", self._parse_factor())
        elif token.type == TokenType.INT:
            node = IntegerLiteral(token.value)
        elif token.type == TokenType.STRING:
            node = StringLiteral(token.value)
        elif token.type == TokenType.TRUE:
            node = BooleanLiteral(True)
        elif token.type == TokenType.FALSE:
            node = BooleanLiteral(False)
        elif token.type == TokenType.LBRACKET:
            node = self._parse_array_literal()
        elif token.type == TokenType.IDENT:
            node = Identifier(token.value)
            if self.peek_token.type == TokenType.LPAREN:
                node = self._parse_call_expression(node)
        elif token.type == TokenType.IF:
            return self._parse_if_expression()
        elif token.type == TokenType.WHILE:
            return self._parse_while_expression()
        elif token.type == TokenType.FN:
            return self._parse_function_literal()
        else:
            raise SyntaxError(f"Unexpected token: {token.type.name}")

        # Check for index access like arr[0]
        while self.peek_token.type == TokenType.LBRACKET:
            self._advance_token()
            self._advance_token()
            index = self._parse_expression()
            self._advance_token() # consume ]
            node = IndexExpression(node, index)

        return node

    def _parse_array_literal(self):
        elements = []
        if self.peek_token.type != TokenType.RBRACKET:
            self._advance_token()
            elements.append(self._parse_expression())
            while self.peek_token.type == TokenType.COMMA:
                self._advance_token()
                self._advance_token()
                elements.append(self._parse_expression())
        self._advance_token()
        return ArrayLiteral(elements)

    def _parse_function_literal(self):
        self._advance_token()
        self._advance_token()
        parameters = []
        if self.current_token.type != TokenType.RPAREN:
            parameters.append(Identifier(self.current_token.value))
            self._advance_token()
            while self.current_token.type == TokenType.COMMA:
                self._advance_token()
                parameters.append(Identifier(self.current_token.value))
                self._advance_token()
        self._advance_token()
        body = self._parse_block_statement()
        return FunctionLiteral(parameters, body)

    def _parse_call_expression(self, function):
        self._advance_token()
        arguments = []
        if self.peek_token.type != TokenType.RPAREN:
            self._advance_token()
            arguments.append(self._parse_expression())
            while self.peek_token.type == TokenType.COMMA:
                self._advance_token()
                self._advance_token()
                arguments.append(self._parse_expression())
        self._advance_token()
        return CallExpression(function, arguments)

    def _parse_if_expression(self):
        self._advance_token()
        self._advance_token()
        condition = self._parse_expression()
        self._advance_token()
        self._advance_token()
        consequence = self._parse_block_statement()
        alternative = None
        if self.peek_token.type == TokenType.ELSE:
            self._advance_token()
            self._advance_token()
            alternative = self._parse_block_statement()
        return IfExpression(condition, consequence, alternative)

    def _parse_while_expression(self):
        self._advance_token()
        self._advance_token()
        condition = self._parse_expression()
        self._advance_token()
        self._advance_token()
        body = self._parse_block_statement()
        return WhileExpression(condition, body)

    def _parse_block_statement(self):
        block = BlockStatement()
        self._advance_token()
        while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
            stmt = self._parse_statement()
            if stmt:
                block.statements.append(stmt)
            self._advance_token()
        return block
