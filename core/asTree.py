import sys
import typing as ty

import basicTypes as bt
import commons as comm
import err
import other as ot
import tok

# Please note that TT, TTn, TT are defined here!
TTn = tok.Token
TT = tok.TokenTypes
ANSI = comm.ANSI


class ASTNode:
    def __init__(self) -> None:
        self.val = ''
    
    def __error(self, errType:ty.Type[err.Error], *args:ty.Any, **kwargs:ty.Any):
        sys.stdout.write(f"{ot.RED if ANSI else ''}??{ot.RESET if ANSI else ''} " + str(errType(*args, **kwargs)) + '\n')
        sys.stdout.flush()
    
    def __str__(self) -> str:
        return str(self.val)


class ExprNode(ASTNode):
    def __init__(self, exprVal:bt.BaseForAll) -> None:
        super().__init__()
        self.exprVal = exprVal


class TermNode(ASTNode):
    def __init__(self, termVal:bt.BaseForAll) -> None:
        super().__init__()
        self.termVal = termVal


class ParamNode(ASTNode):
    def __init__(self, params:dict[bt.VIdent, TT]|None) -> None:
        super().__init__()
        self.params = params


class StatementNode(ASTNode):
    def __init__(self, statement:ty.Self, nextStatement:ty.Self|None=None) -> None:
        super().__init__()
        self.statement     = statement
        self.nextStatement = nextStatement
    
    def __repr__(self) -> str:
        return f"StatementNode({self.statement}, {self.nextStatement})"


class BinOpNode(ASTNode):
    def __init__(self, left:ty.Any, op:bt.VOperator, right:ty.Any) -> None:
        super().__init__()
        self.err   = False
        self.left  = left
        self.op    = op
        self.right = right
        self.val   = op.val(left, right)
    
    def __repr__(self) -> str:
        return f"BinOp({self.left}, {self.op}, {self.right})"


class UnaryOpNode(ASTNode):
    def __init__(self, op:bt.VOperator, operand:ty.Any) -> None:
        super().__init__()
        self.op = op
        self.operand = operand
        self.val = self.op.val(operand)
    
    def __repr__(self) -> str:
        return f"UnaryNode({self.op}, {self.operand})"


class NumNode(ASTNode):
    def __init__(self, val:bt.VInt|bt.VFloat) -> None:
        super().__init__()
        self.val = val
    
    def __repr__(self) -> str:
        return f"NumNode({self.val})"


class BoolNode(ASTNode):
    def __init__(self, val:bt.VBool) -> None:
        super().__init__()
        self.val = val
    
    def __repr__(self) -> str:
        return f"BoolNode({self.val})"


class StringNode(ASTNode):
    def __init__(self, val:bt.VString) -> None:
        super().__init__()
        self.val = val
    
    def __repr__(self) -> str:
        return f"StringNode({self.val})"


# Might not be needed
# class IntNode(ASTNode):
#     def __init__(self) -> None:
#         super().__init__()


class IdentNode(ASTNode):
    def __init__(self, val:tuple[bt.VIdent]) -> None:
        super().__init__()
        self.val = val
    
    def __repr__(self) -> str:
        return f"IdentNode({self.val})"


class LetNode(ASTNode):
    def __init__(self, ident:bt.VIdent, val:bt.BaseForAll) -> None:
        super().__init__()
        self.ident = ident
        self.val   = val
    
    def __repr__(self) -> str:
        return f"AssignNode({self.ident}, {self.val})"


# class IfNode(ASTNode):
#     def __init__(self, condition:bool, thenBranch, elseBranch=None) -> None:
#         self.condition = condition
#         self.thenBranch = thenBranch
#         # self.elifBranches = elifBranches
#         self.elseBranch = elseBranch
    
#     def __repr__(self) -> str:
#         return f"IfNode({self.condition}, then={self.thenBranch}, else={self.elseBranch})"


# class WhileNode(ASTNode):
#     def __init__(self, condition, thenBranch) -> None:
#         self.condition = condition
#         self.thenBranch = thenBranch
    
#     def __repr__(self) -> str:
#         return f"WhileNode({self.condition}, then={self.thenBranch})"


# class ForNode(ASTNode):
#     def __init__(self, iterable, thenBranch) -> None:
#         self.iterable = iterable
#         self.thenBranch = thenBranch
    
#     def __repr__(self) -> str:
#         return f"IfNode({self.iterable}, then={self.thenBranch})"


class FunNode(ASTNode):
    def __init__(self, func:bt.VIdent, parameters:ParamNode) -> None:
        super().__init__()
        self.func = func
        self.parameters = parameters
    
    def __repr__(self) -> str:
        return f"FunNode({self.func}, {self.parameters})"
