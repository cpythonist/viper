
# ERROR CODES

This document lists and details the error codes returned to the calling program
and used within the program.

## RETURN CODE TO THE CALLING PROGRAM

**+0:** Success  
**+1:** Too few arguments  
**+2:** Too many arguments  
**+3:** Expected value for option  
**+4:** Unknown option/flag  
**+5:** Source file not found  
**+6:** Access is denied to source file  
**+7:** Source file does not contain text

## (INTERNAL) LEXER ERROR CODES

**+1000:** Unclosed string

## (INTERNAL) PARSER ERROR CODES

**+2000:** Match token error (unexpected token, i.e. could not match token)  
**+2001:** Unexpected token
