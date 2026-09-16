from internal.parser import Program, LetStatement, AssignStatement, ReturnStatement, PrintStatement, Identifier, IntegerLiteral, BooleanLiteral, StringLiteral, ArrayLiteral, IndexExpression, PrefixExpression, InfixExpression, IfExpression, WhileExpression, BlockStatement, FunctionLiteral, CallExpression

class ReturnValue:
    def __init__(self, value): self.value = value

class Function:
    def __init__(self, parameters, body, env):
        self.parameters, self.body, self.env = parameters, body, env

class Environment:
    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer

    def get(self, name):
        val = self.store.get(name)
        if val is None and self.outer is not None:
            return self.outer.get(name)
        return val

    def set(self, name, val):
        self.store[name] = val
        return val

    def assign(self, name, val):
        if name in self.store:
            self.store[name] = val
            return val
        elif self.outer is not None:
            return self.outer.assign(name, val)
        else:
            raise NameError(f"Undefined variable \x27{name}\x27")

def eval_node(node, env):
    if isinstance(node, Program):
        result = None
        for stmt in node.statements:
            result = eval_node(stmt, env)
            if isinstance(result, ReturnValue):
                return result.value
        return result
    elif isinstance(node, BlockStatement):
        result = None
        for stmt in node.statements:
            result = eval_node(stmt, env)
            if isinstance(result, ReturnValue):
                return result
        return result
    elif isinstance(node, LetStatement):
        return env.set(node.name.value, eval_node(node.value, env))
    elif isinstance(node, AssignStatement):
        return env.assign(node.name.value, eval_node(node.value, env))
    elif isinstance(node, ReturnStatement):
        return ReturnValue(eval_node(node.returnValue, env))
    elif isinstance(node, PrintStatement):
        val = eval_node(node.expression, env)
        print(val)
        return val
    elif isinstance(node, IntegerLiteral): return node.value
    elif isinstance(node, BooleanLiteral): return node.value
    elif isinstance(node, StringLiteral): return node.value
    elif isinstance(node, ArrayLiteral):
        return [eval_node(el, env) for el in node.elements]
    elif isinstance(node, IndexExpression):
        left = eval_node(node.left, env)
        index = eval_node(node.index, env)
        return left[index]
    elif isinstance(node, Identifier): return env.get(node.value)
    elif isinstance(node, FunctionLiteral):
        return Function(node.parameters, node.body, env)
    elif isinstance(node, CallExpression):
        fn = eval_node(node.function, env)
        args = [eval_node(arg, env) for arg in node.arguments]
        extended_env = Environment(fn.env)
        for param, arg in zip(fn.parameters, args):
            extended_env.set(param.value, arg)
        evaluated = eval_node(fn.body, extended_env)
        return evaluated.value if isinstance(evaluated, ReturnValue) else evaluated
    elif isinstance(node, PrefixExpression):
        right = eval_node(node.right, env)
        if node.operator == "!": return not right
    elif isinstance(node, InfixExpression):
        l = eval_node(node.left, env)
        if node.operator == "&&": return bool(l) and bool(eval_node(node.right, env))
        if node.operator == "||": return bool(l) or bool(eval_node(node.right, env))
        r = eval_node(node.right, env)
        if node.operator == "+": return l + r
        if node.operator == "-": return l - r
        if node.operator == "*": return l * r
        if node.operator == "/": return l // r
        if node.operator == "==": return l == r
        if node.operator == "<": return l < r
        if node.operator == ">": return l > r
        if node.operator == "<=": return l <= r
        if node.operator == ">=": return l >= r
    elif isinstance(node, IfExpression):
        if eval_node(node.condition, env):
            return eval_node(node.consequence, Environment(env))
        elif node.alternative is not None:
            return eval_node(node.alternative, Environment(env))
    elif isinstance(node, WhileExpression):
        result = None
        while eval_node(node.condition, env):
            result = eval_node(node.body, Environment(env))
            if isinstance(result, ReturnValue): return result
        return result
    return None
