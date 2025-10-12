
# THE PARSER

## Overview

This parser is a recursive-descent parser. This implementation is a LL(k) parser, i.e. it is
capable of looking ahead any number of tokens.  

The parser is divided into various modules and grouped into a package, `src\core\parser\`. The main
entry point of the parser is `src\core\parser\engine.py`. This file contains the class `Parser`,
which is used to instantise the parser object. This class uses mixins to aggregate functionality.
The mixins are obtained from the other modules in the package.  

The module `src\core\parser\protocol.py` defines protocols and type hints used for linting and
static type checking.

## INPUT AND OUTPUT

The parser needs the source string and the lexer object to be successfully instantised. The parser
itself uses the lexer to generate all the tokens. See [the lexer documentation](../lexer/lexer.md)
for more information.  

The method `parse()` of class `Parser` in `src\core\parser\engine.py` is the entry point of the
parser. The parser produces a abstract syntax tree, which is list of nodes. Each AST node is an
object from a class from the module `src\core\ast_nodes.py`. See
[the AST nodes documentation](#ast-nodes) for more information.

## SUPPORTED GRAMMAR

The parser supports only the Viper programming language. See [the BNF](../../assets/syntax.bnf).  

One significant change from other programming languages which use a semicolon to end statements is
that compound statements (statements enclosed by `{}`) need a semicolon at the end to be
considered valid. For example, consider this snippet:

```viper
{
    prn 1;
    let bool spam = false;
    if (spam != true) {
        prn "It's false! IT'S FALSE!";
    };
};
```

Notice the use of semicolons after the closing flower brace.

## ERROR HANDLING

In case a violation of the rules is identified, the parser creates an error node (defined in the
same module as other nodes) and appends it to an "error node array." The error node *is not*
added to the main AST.

## AST NODES

### `ASTNode`

This node is the base AST node. All other AST nodes are derived from this node.  

This node contains three defined (i.e. externally-defined) attributes:

```python
kind: str
token: core.token_.Token
parent: "ASTNode" | None
```

### `NotImplementedNode`

This node represents an unimplemented feature.

### `ErrNode`

This node represents an error encounted during parsing. This node defines two more attributes:

```python
typStr: str
nodes: list[core.ast_nodes.ASTNode]
```

### `IdentNode`

This node represents an identifier. This node defines two more attributes:

```python
typ: core.token.TokenTypes
nm: str
```

### `LiteralNode`

This node represents a literal in the source. This node defines two more attributes:

```python
typ: core.token.TokenTypes
val: str
```

### `UnaryOpNode`

This node represents unary operations. This node defines two more attributes:

```python
op: str
rt: LiteralNode | IdentNode | UnaryOpNode | BinOpNode | GrpNode | ErrNode
```

### `BinOpNode`

This node represents binary operations. This nodes defines three more attributes:

```python
lt: LiteralNode | IdentNode | UnaryOpNode | BinOpNode | GrpNode | ErrNode
op: str
rt: LiteralNode | IdentNode | UnaryOpNode | BinOpNode | GrpNode | ErrNode
```

### `GrpNode`

This node represents parenthesised expressions. This node defines one more attribute:

```python
node: LiteralNode | IdentNode | GrpNode | UnaryOpNode | BinOpNode | ErrNode
```

### `CfgNode`

This node represents the configuration statements at the beginning of the program. This node
defines one more attribute:

```python
config: dict[str, str]
```

### `StmtNode`

This node represents statements. This node defines one more attribute:

```python
nodes: list[ASTNode]
```

### `PrnNode`

This node represents a print statement. This node defines one more attribute:

```python
expr: GrpNode
```

### `IfNode`

This node represents an if conditional branch. This node defines two more attributes:

```python
cond: GrpNode
body: StmtNode
```

### `WhileNode`

This node represents a while loop. This node defines two more attributes:

```python
cond: GrpNode
body: StmtNode
```

### `LetNode`

This node represents an assignment statement. This node defines three more attributes:

```python
ident: IdentNode
typ: core.token_.TokenTypes
expr: GrpNode
```

### `BreakNode`

This node represents a loop break statement.

### `ContiNode`

This node represents a loop continue statement.

### `RetNode`

This node represents a function return statement. This node defines one more attribute:

```python
expr: GrpNode
```

### `FnNode`

This represents a function definition. This node defines four more attributes:

```python
typ: core.token_.TokenTypes
ident: IdentNode
params: dict[str, core.token_.TokenTypes]
body: StmtNode
```

### `ChNode`

This represents a "variable-change" node. This node defines two more attributes:

```python
ident: IdentNode
expr: GrpNode
```
