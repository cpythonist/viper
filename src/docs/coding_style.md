
# THE VIPER COMPILER CODING STYLE DOCUMENT

This document defines the coding conventions for this project. The programming language used is
Python-3.13.7.

## INDENTATION

Indentation is 4 spaces. No less, no more. And absolutely no tabs.

## LINE LENGTH

Limit lines to 100 characters when possible.

Exceptions include (but not limited to) long strings (e.g. error messages or command-line output)
where splitting lines would hurt readability or greppability (fun fact: Mr. Torvalds talks about
this in the Linux kernel coding style document).

## COMMENTS

Avoid over-commenting. Don't explain how your code works - that's what the code is for. Explain
*what* the code does, and why it does it.

Comment when something clever, non-obvious or ugly is going on.

## NAMING

- **Constants (literal and runtime):** ALLCAPS_SEP_BY_UNDERSCORES  
- **Variable and function identifiers:** lowerCamelCase  
- **Class identifiers:** UpperCamelCase  
- **Private attributes:** Prefix with a single underscore  
- **Filenames:** lower_snake_case  
- **Abbreviated module names:** flatcase

## IMPORTS

- **Standard library imports**: grouped first  
- **Third-party imports**: grouped next  
- **Custom modules**: grouped last  

Separate aliased modules/packages from modules/packages with original names with a newlines,
grouping the latter first.

## DOCSTRINGS

Docstrings must be written with triple quotes (even one-liners).  
**Format:**

```python
"""
Short description of the object.
> param parameter1: Description of parameter1
...
> return: Description of return value
NOTE: Any other data of value when using the object.
"""
```

## EXPRESSIONS AND OPERATORS

One space should surround all operators.  
No spaces surround `=` when supplying keyword arguments in a function call.
No space between a parameter/argument name/value and its parenthesis(es).

## WHITESPACE

Two blank lines between global-level attributes.  
One blank line between class methods and other attributes.  
One blank line between different logical units in a code block.  
No trailing whitespace unless required by a multi-line string.

## TYPE HINTS

Type hints are **compulsory**. No exclusions.

## FORMATTER

Use [the Black formatter](http://github.com/psf/black).
