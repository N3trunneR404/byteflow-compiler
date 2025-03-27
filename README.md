# ByteFlow Compiler

A compiler that translates C-like code into ByteFlow (a minimalist language similar to Brainfuck). This project demonstrates compiler construction principles including lexical analysis, parsing, and code generation.

## 🚀 Features

- Lexical analysis with token generation
- Recursive descent parsing
- Function compilation
- Global variable support
- Control flow statements (if, while, for, switch)
- Array support
- Direct ByteFlow code generation

## 📁 Project Structure

```
byteflow-compiler/
├── Compiler/
│   ├── __init__.py
│   ├── Compiler.py          # Main compiler implementation
│   ├── Exceptions.py        # Custom exception definitions
│   ├── FunctionCompiler.py  # Function compilation logic
│   ├── Functions.py         # Function handling utilities
│   ├── General.py          # General utility functions
│   ├── Globals.py          # Global variable management
│   ├── Lexical_analyzer.py # Tokenization logic
│   ├── LibraryFunctions.py # Built-in library functions
│   ├── Minify.py          # Code minification utilities
│   ├── Node.py            # AST node implementations
│   ├── Optimizer.py       # Code optimization
│   ├── Parser.py          # Token parsing implementation
│   └── Token.py           # Token class definition
├── examples/
│   ├── arrays.bf          # Array usage examples
│   ├── calc.bf            # Calculator implementation
│   └── games/
│       └── snake.bf       # Snake game implementation
├── Interpreter.py
├── .gitignore
├── .gitattributes
├── byteflow.py           # Main entry point
└── README.md             # Project documentation
```

### Added Files Description

- **`Exceptions.py`**: Defines custom exceptions for error handling
- **`Functions.py`**: Contains utilities for function handling and management
- **`General.py`**: Houses general-purpose utility functions used across the compiler
- **`Globals.py`**: Manages global variable declarations and scope
- **`LibraryFunctions.py`**: Implements built-in library functions
- **`Minify.py`**: Provides code minification capabilities

These additions enhance the compiler's functionality with better error handling, global variable management, library function support, and code optimization capabilities.

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/N3trunnelRR404/byteflow-compiler.git
cd byteflow-compiler
```

2. Ensure you have Python 3.11 or higher installed:
```bash
python --version
```

## 📖 Usage

### Basic Compilation
```bash
python byteflow.py input_file.bf
```

### Example Program
```c
// example.bf
int main() {
    int a = 5;
    int b = 10;
    print("Sum is: ");
    print(a + b);
    return 0;
}
```

### Run the Example
```bash
python byteflow.py examples/example.bf
```

## 🔍 Language Features

### Supported Types
- `int` - Integer values
- Arrays (multi-dimensional supported)

### Control Flow
- `if`/`else` statements
- `while` loops
- `for` loops
- `switch`/`case` statements
- `break` statements

### Functions
- Function definitions with parameters
- Return values
- Recursive function calls

### Input/Output
- `print` statement for output
- Basic input operations

## 🔧 Development

### Running Tests
```bash
python -m unittest discover tests
```

### Adding New Features
1. Implement the feature in appropriate module
2. Add test cases in `tests/` directory
3. Update documentation
4. Submit pull request

## 📝 Code Examples

### Array Operations
```c
int main() {
    int arr[5];
    int i;
    for(i = 0; i < 5; i++) {
        arr[i] = i * 2;
    }
    return 0;
}
```

### Function Definition
```c
int fibonacci(int n) {
    if(n <= 1) {
        return n;
    }
    return fibonacci(n-1) + fibonacci(n-2);
}
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⭐ Acknowledgments

- Inspired by the Brainfuck programming language
- Built with modern Python features
- Thanks to all contributors

## 🐛 Known Issues

- Limited optimization capabilities due to direct ByteFlow code generation
- No intermediate representation (IR) stage
- Limited support for floating-point operations

## 📬 Contact
Made by: Shubhankar, Vikas, Edukondulu
