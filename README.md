<div align="center">

# ✨ Lumina Interpreter ✨
*A lightweight, modular, and expressive custom programming language interpreter built from scratch in Python.*

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

---

## 🚀 Overview

**Lumina** is designed to explore the core pillars of programming language design—ranging from lexical analysis and abstract syntax tree (AST) parsing to tree-walk evaluation. Built with a clean, decoupled architecture, it emphasizes readability, extensibility, and minimal overhead.

---

## 🛠️ Project Architecture

The codebase follows a modular layout separating execution entry points, internal compiler components, and user examples:

```text
lumina/
├── cmd/
│   └── lumina/
│       └── main.py       # Entry point / CLI interface
├── internal/
│   ├── lexer.py          # Tokenizer (converts source code into tokens)
│   ├── parser.py         # Parser (constructs the Abstract Syntax Tree)
│   └── evaluator.py      # Evaluator (executes expressions and statements)
├── examples/
│   └── test.lum          # Sample Lumina script files
└── tests/                # Automated test suites
```
## ✨ Core Features
Modular Design: Strictly separated pipeline components (lexer, parser, evaluator) for high maintainability.

Robust Lexical Analysis: Accurately tokenizes keywords, identifiers, operators, and literals.

AST Construction: Builds precise Abstract Syntax Trees to represent language grammar.

Zero Dependencies: Written entirely in standard Python without external baggage.

##  🏁 Getting Started
Prerequisites
Make sure you have Python installed on your system:

Bash
python3 --version
Installation
Clone your repository:

Bash
git clone [https://github.com/callmepc99/lumina-interpreter.git](https://github.com/callmepc99/lumina-interpreter.git)
cd lumina
Run a sample script using the CLI entry point:

Bash
python3 cmd/lumina/main.py examples/test.lum
##  📝 Example Code (test.lum)
Lisp
// Sample Lumina script
let greeting = "Welcome to Lumina";
print(greeting);
## 🗺️ Roadmap
[ ] Add support for functions and control flow (if/else, while loops)

[ ] Implement a REPL (Read-Eval-Print Loop) interactive shell

[ ] Optimize error reporting with line and column tracking

## 👤 Author
Crafted with 💻 by Prithvi (@callmepc99)
