
# THE VIPER LANGUAGE SPECIFICATIONS

Please note that some of the language features mentioned here have not been implemented yet.

## COMPOUND STATEMENTS

Compound statements are enclosed by flower braces.

```viper
{
    statements
};
```

## VARIABLE DECLARATION AND ASSIGNMENT

Assignment is done through the `let` statement. Constants are defined using the `const` keyword.

```viper
let type ident = value;
```

## VARIABLE MODIFICATION OR UPDATION

Variable modification or updation is achieved using the `ch` keyword.

```viper
ch identifier = value;
```

## IF CONDITIONAL BRANCH

The `if` statement, `elif` clause and `else` clause all accept only a compound statement as their
body.  
`elif` and `else` clauses are optional.

```viper
if expression {
    statements
}; elif expression {
    statements
}; else {
    statements
};
```

## WHILE LOOP

The `while` keyword is used to define a while loop.

```viper
while expression {
    statements
};
```

## FOR LOOP

Construct is yet to be decided.

## LOOP BREAK

A loop can be terminated by using the `break` keyword.

```viper
while ... {
    statements
    break;
};
```

## LOOP CONTINUE

A jump to the next loop iteration can be achieved using the `conti` keyword.

```viper
while ... {
    statements
    conti;
};
```

## FUNCTION DECLARATION

Function declaration is done using the `fn` keyword.

```viper
fn type identifier(type parameter, ...)
{
    statements
};
```

## FUNCTION CALL

```viper
<fn-name>(arg, ...);
```

## RETURN STATEMENT

The `ret` keyword is used to return a value from a function.

```viper
fn bool ...
{
    statements
    ret true;
};
```

## END OF STATEMENT

A semicolon indicates the end of a statement.

```viper
statement;
```
