import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from internal.lexer import Lexer
from internal.parser import Parser
from internal.evaluator import eval_node, Environment

def start_repl():
    print("✨ Welcome to the Lumina Programming Language REPL! ✨")
    print("Type expressions or statements. Type exit() or press Ctrl+C to quit.\n")
    env = Environment()
    buffer = []
    
    while True:
        try:
            prompt = "... " if buffer else "lumina> "
            sys.stdout.write(prompt)
            sys.stdout.flush()
            
            line = sys.stdin.readline()
            if not line:
                break
            line = line.rstrip("\r\n")
            
            if not buffer and line.strip() == "exit()":
                break
                
            # If buffer has items and user hits enter on an empty line, execute!
            if buffer and line.strip() == "":
                full_code = "\n".join(buffer)
                buffer = []
                try:
                    lexer = Lexer(full_code)
                    parser = Parser(lexer)
                    program = parser.parse_program()
                    evaluated = eval_node(program, env)
                    if evaluated is not None:
                        print(evaluated)
                except Exception as e:
                    print(f"Error: {e}")
                continue
                
            if not buffer and not line.strip():
                continue
                
            buffer.append(line)
            full_code = "\n".join(buffer)
            
            # Auto-execute if braces are balanced and last line closes a block
            open_braces = full_code.count("{")
            close_braces = full_code.count("}")
            
            if open_braces > 0 and open_braces == close_braces:
                buffer = []
                try:
                    lexer = Lexer(full_code)
                    parser = Parser(lexer)
                    program = parser.parse_program()
                    evaluated = eval_node(program, env)
                    if evaluated is not None:
                        print(evaluated)
                except Exception as e:
                    print(f"Error: {e}")
                
        except KeyboardInterrupt:
            print("\nExiting Lumina REPL...")
            break
        except Exception as e:
            print(f"Error: {e}")
            buffer = []

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        with open(file_path, "r") as f:
            code_content = f.read()
        lexer = Lexer(code_content)
        parser = Parser(lexer)
        program = parser.parse_program()
        eval_node(program, Environment())
    else:
        start_repl()
