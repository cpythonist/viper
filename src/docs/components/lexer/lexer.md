
# THE LEXICAL ANALYSER

Turns raw source code into a stream of tokens. Designed for the Viper programming language. This is
the first step in the compilation process.  

Found at `src\core\lexer.py`.  

Hosts the class `Lexer`, which will become the lexical analyser object when instantiated.

## INPUT AND OUTPUT

The `__init__` method of the class `Lexer` requires one parameter to successfully initialise the
lexer object. The raw source code is to be provided to class `Lexer` as a single string.  

To obtain the stream of tokens, the public method `tokenise` is used. It returns a list of all
tokens in the source string provided.

Each token is an instance of the class `Token` defined in `src\core\token_.py`.

## TOKEN SPECIFICATION

### Keywords (`KEYWD`)

| KEYWORD TOKEN              | DESCRIPTION                                            |
|:---------------------------|:-------------------------------------------------------|
| **General keywords**       |                                                        |
| `DUMMY`                    | Placeholder token used internally                      |
| `INIT`                     | Initialisation token used internally                   |
| `INV`                      | Represents an invalid or unrecognised token            |
| `EOF`                      | End-of-file token representing end of input            |
| `SEMICLN`                  | Represent a semicolon (`;`)                            |
| `TILDE`*                   | Reserved token (unused)                                |
| `COMMA`*                   | Reserved token (unused)                                |
| `DOT`*                     | Reserved token (unused)                                |
| `KEYWD`                    | Internal token; represents a reserved keyword          |
| `IDENT`                    | Internal token; represents an identifier               |
| `TYP`                      | Internal token; represents a data type                 |
|                            |                                                        |
| **Configuration keywords** |                                                        |
| `TYPING`                   | Declares the typing mode                               |
| `DELIM`                    | Declares the delimiting style                          |
|                            |                                                        |
| **Type keywords**          |                                                        |
| `INT`                      | Declares an integer type                               |
| `FLOAT`                    | Declares a single-precision floating-point type        |
| `DOUBLE`*                  | Declares a double-precision floating-point type        |
| `BOOL`                     | Declares a boolean type                                |
| `STR`                      | Declares a string type                                 |
|                            |                                                        |
| **Other keywords**         |                                                        |
| `TRUE`                     | Boolean literal for true                               |
| `FALSE`                    | Boolean literal for false                              |
| `LET`                      | Declares a variable                                    |
| `FN`                       | Declares a function                                    |
| `RET`                      | Returns a value from a function                        |
| `IF`                       | Starts a conditional branch                            |
| `ELIF`                     | Defines an additional conditional branch               |
| `ELSE`                     | Defines the fallback branch in a conditional statement |
| `WHILE`                    | Starts a while loop                                    |
| `FOR`                      | Starts a for loop                                      |
| `BREAK`                    | Exits the innermost loop                               |
| `CONTI`                    | Jumps to next iteration of the innermost loop          |
| `LOAD`                     | Imports an external file                               |
| `PRN`                      | Prints output to standard output                       |
| `SCN`                      | Reads input from standard input                        |
| `CH`                       | Updates or reassigns a variable                        |

\* *Unused as of now*

---

### Operators

| OPERATOR TOKEN           | DESCRIPTION                                             |
|:-------------------------|:--------------------------------------------------------|
| **Arithmetic operators** |                                                         |
| `PLUS`                   | Represents the addition/unary plus operator (`+`)       |
| `MINUS`                  | Represents the subtraction/unary minus operator (`-`)   |
| `ASTERISK`               | Represents the binary multiplication operator (`*`)     |
| `FSLASH`                 | Represents the binary true division operator (`/`)      |
| `CARET`                  | Represents the binary exponentiation operator (`^`)     |
| `DOLLAR`                 | Represents the binary floor division operator (`$`)     |
| `PERCENT`                | Represents the binary modulus operator (`%`)            |
|                          |                                                         |
| **Comparison operators** |                                                         |
| `EQEQ`                   | Represents the equality operator (`==`)                 |
| `NEQ`                    | Represents the inequality operator (`!=`)               |
| `LT`                     | Represents the less than operator (`<`)                 |
| `GT`                     | Represents the greater than operator (`>`)              |
| `LTEQ`                   | Represents the less than or equal to operator (`<=`)    |
| `GTEQ`                   | Represents the greater than or equal to operator (`>=`) |
|                          |                                                         |
| **Logical operators**    |                                                         |
| `NOT`                    | Represents the logical NOT operator                     |
| `AND`                    | Represents the logical AND operator                     |
| `OR`                     | Represents the logical OR operator                      |
|                          |                                                         |
| **Assignment operator**  |                                                         |
| `EQ`                     | Represents the assignment operator (`=`)                |

---

### Brackets

| BRACKET TOKEN     | DESCRIPTION                               |
|:------------------|:------------------------------------------|
| `LPAREN`          | Represents the left parenthesis (`(`)     |
| `RPAREN`          | Represents the right parenthesis (`)`)    |
| `LFLBRAC`         | Represents the left flower bracket (`{`)  |
| `RFLBRAC`         | Represents the right flower bracket (`}`) |
| `LSQBRAC`         | Represents the left square bracket (`[`)  |
| `RSQBRAC`         | Represents the right square bracket (`]`) |

---

### Whitespace

| WHITESPACE TOKEN | DESCRIPTION                                   |
|:-----------------|:----------------------------------------------|
| `SPACE`          | Represents a space character (` `)            |
| `TAB`            | Represents a tab character (`\t`)             |
| `CARR_RET`       | Represents a carriage return character (`\r`) |
| `NL`             | Represents a newline character (`\n`)         |

**NOTE:** These tokens are not used as of now, but will be used in the future when adding
functionality for whitespace delimiting.

---

### Other

These were used in an older version of the lexer, but has been kept around *just in case* they are
needed again.

| TOKEN     | DESCRIPTION |
|:----------|:------------|
| `PRIMARY` | -           |
| `UNARY`   | -           |
| `EXPO`    | -           |
| `FACTOR`  | -           |
| `TERM`    | -           |
| `EXPR`    | -           |

## IMPLEMENTATION DETAILS

This lexer is a hand-written lexical analyser. Whitespace characters and newlines are ignored
currently, although they will later be used when functionality to delimit using whitespace is
added. The lexer ignores comments. Comments start with a hash (`#`).

## ERROR HANDLING

When the lexer encounters an unrecognised symbol, it generates an error token. Error tokens are
`Token` objects whose `typ` attribute is `core.token_.TokenTypes.INV`. The error details can be
found in the other attributes.

## EXAMPLES

Sample program: [CLICK ME! CLICK ME!](./sample_prog.vi)  
Output: [NO, NO! CLICK ME! CLICK ME! I'M BETTER](./sample_prog_lexer_op.txt)

Please ignore the ANSI codes at the start (and end, if any) of the output. They appear during
checks done to determine if the console is ANSI-compliant (supports standard ANSI escape codes for
colour), which is not perfect yet.

## INTEGRATION

This lexer exposes a single public method:

```python
tokenise(src: str) -> list[core.token_.Token]
```

This method performs lexical analysis on the source string (`src`). Method `tokenise()` returns a
list of `core.token_.Token` objects, which contain the following fields for data storage:

| FIELD  | DESCRIPTION                                                  |
|:-------|:-------------------------------------------------------------|
| `typ`  | Type of the token (`core.token_.TokenTypes`)                 |
| `val`  | Value of the token (type `str`)                              |
| `pos`  | Absolute position of the token in the source string          |
| `ln`   | Line number of the token                                     |
| `ppos` | Position of the token in the current line ("print position") |

## EXTENSIBILTY AND MAINTENANCE

### Add new tokens

Define the token type name in `src\core\token_.py` inside the enum class `TokenTypes` with a unique
token constant value. Then, inside method `_getNxtTok()` in class `Lexer`, in `src\core\lexer.py`,
add logic to return the required token.

## BUGS AND TODO

Todo comments are scattered all over the code, above places where something needs to be implemented
or changed. They will be done as and when required.  

Comment ignoring appears a little fragile at the moment, although it does not appear to fail often.
