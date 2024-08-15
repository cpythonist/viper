# Viper
The (incomplete) Viper parser.

The Viper language is an upcoming general-purpose, statically- and dynamically-typed, compiled programming language written in Python which aims to combine the simplicity of Python and speed of C/C++. It was largely inspired by Python. Other inspirations include C/C++ and JavaScript.

This version of the parser does not include abstract syntax tree generation. This prints the tokens and values of expressions (i.e. basically does half of the parsing process). The AST generator is currently not being worked on as the developer has moved to other interests. It will be some time before the developer will return to this project.
The name was derived from the fact that viper is kind of snake, so is python (as the language was mostly influenced by Python).

The language uses the `.vi` extension.

## Features
Some features of the Viper language include (some of them are not implemented yet):
1. Ability to choose between static-typing and dynamic typing for the project.
2. Extremely simple syntax, with easy-to-understand terms.
3. High speed of the compiled application.

The Viper programming language is planned to compile using the `llvmlite` Python module.

## Usage
A sample file called `main.vi` is present in the `tests\` directory. It can be used, or a new file can be created.
### Windows:
```
<PYTHON-DIR>\python.exe main.py <vi-FILE>
```
### Linux:
```
python3 main.py <vi-FILE>
```

## Contributors
- CPythonist:
  - [GitHub profile](http://github.com/cpythonist/)
  - [Personal website](http://cpythonist.github.io/)
