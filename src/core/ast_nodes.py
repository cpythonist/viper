import core.token_ as tok

TT = tok.TokenTypes


class ASTNode:
    parent: "ASTNode | None"

    kind = "base"
    token = tok.Token(TT.DUMMY, "", -1, 0, 0)
    parent = None


class NotImplementedNode(ASTNode):
    def __init__(self, token: tok.Token) -> None:
        self.token = token
        self.kind = "not-impld"

    def __repr__(self) -> str:
        return f"[NOT_IMPL ({self.token.typ.name} {self.token.val} {self.token.pos} {self.token.ln} {self.token.ppos})]"


class ErrNode(ASTNode):
    def __init__(self, typStr: str, token: tok.Token, *nodes: ASTNode) -> None:
        self.typStr = typStr
        self.token = token
        self.nodes = list(nodes)
        self.kind = "err"

    def __repr__(self) -> str:
        return f"ERR ({self.typStr}) ({self.token.typ.name} {repr(self.token.val)} {self.token.pos} {self.token.ln} {self.token.ppos}) {self.nodes}"


class IdentNode(ASTNode):
    def __init__(self, token: tok.Token) -> None:
        self.token = token
        self.typ = token.typ
        self.nm = token.val
        self.kind = "ident"

    def __repr__(self) -> str:
        return f"(IDENT {self.nm} ({self.token.pos} {self.token.ln} {self.token.ppos}))"


class LiteralNode(ASTNode):
    def __init__(self, token: tok.Token) -> None:
        self.token = token
        self.typ = token.typ
        self.val = token.val
        self.kind = "lit"

    def __repr__(self) -> str:
        return f"(LIT {self.val} ({self.token.pos} {self.token.ln} {self.token.ppos}))"


class UnaryOpNode(ASTNode):
    def __init__(
        self,
        op: tok.Token,
        rt: "LiteralNode | IdentNode | UnaryOpNode | BinOpNode | GrpNode | ErrNode",
        token: tok.Token,
    ) -> None:
        self.op = op
        self.rt = rt
        self.token = token
        self.kind = "unary-op"

    def __repr__(self) -> str:
        return f"({self.op.val}{self.rt} ({self.token.pos} {self.token.ln} {self.token.ppos}))"


class BinOpNode(ASTNode):
    def __init__(
        self,
        lt: "LiteralNode | IdentNode | GrpNode | UnaryOpNode | BinOpNode | ErrNode",
        op: tok.Token,
        rt: "LiteralNode | IdentNode | GrpNode | UnaryOpNode | BinOpNode | ErrNode",
    ) -> None:

        self.lt = lt
        self.op = op
        self.rt = rt
        self.kind = "bin-op"

    def __repr__(self) -> str:
        return f"({self.lt} {self.op.val} {self.rt})"


class GrpNode(ASTNode):
    def __init__(
        self,
        node: "LiteralNode | IdentNode | GrpNode | UnaryOpNode | BinOpNode | ErrNode",
    ) -> None:
        self.node = node
        self.kind = "grp"

    def __repr__(self) -> str:
        return f"{self.node}"


class CfgNode(ASTNode):
    def __init__(self, config: dict[str, str]) -> None:
        self.config = config
        self.kind = "cfg"

        for key in config:
            setattr(self, key, config[key])

    def __repr__(self) -> str:
        return f"CFG typing: {self.config}"


class StmtNode(ASTNode):
    def __init__(self, token: tok.Token, *nodes: ASTNode) -> None:
        self.token = token
        self.nodes = list(nodes)
        self.kind = "stmt"

    def __repr__(self) -> str:
        return f"STMT {self.nodes}"


class PrnNode(ASTNode):
    def __init__(self, expr: GrpNode, token: tok.Token) -> None:
        self.expr = expr
        self.token = token
        self.kind = "prn"

    def __repr__(self) -> str:
        return f"PRN {self.expr}"


class IfNode(ASTNode):
    def __init__(self, cond: GrpNode, body: StmtNode, token: tok.Token) -> None:
        self.cond = cond
        self.body = body
        self.token = token
        self.kind = "if"

    def __repr__(self) -> str:
        return f"IF {self.cond} {self.body.nodes}"


class WhileNode(ASTNode):
    def __init__(self, cond: GrpNode, body: StmtNode, token: tok.Token) -> None:
        self.cond = cond
        self.body = body
        self.token = token
        self.kind = "while"

    def __repr__(self) -> str:
        return f"WHILE {self.cond}; {self.body.nodes}"


class LetNode(ASTNode):
    def __init__(self, ident: IdentNode, typ: TT, expr: GrpNode, token: tok.Token) -> None:
        self.ident = ident
        self.typ = typ
        self.expr = expr
        self.token = token
        self.kind = "let"

    def __repr__(self) -> str:
        return f"LET {self.typ.name} {self.ident} {self.expr}"


class BreakNode(ASTNode):
    def __init__(self, token: tok.Token) -> None:
        self.token = token
        self.kind = "break"

    def __repr__(self) -> str:
        return f"BREAK ({self.token.pos} {self.token.ln} {self.token.ppos})"


class ContiNode(ASTNode):
    def __init__(self, token: tok.Token) -> None:
        self.token = token
        self.kind = "conti"

    def __repr__(self) -> str:
        return f"CONTI ({self.token.pos} {self.token.ln} {self.token.ppos})"


class RetNode(ASTNode):
    def __init__(self, expr: GrpNode, token: tok.Token) -> None:
        self.expr = expr
        self.token = token
        self.kind = "ret"

    def __repr__(self) -> str:
        return f"RET ({self.expr}) ({self.token.typ.name} '{self.token.val}' {self.token.pos} {self.token.ln} {self.token.ppos})"


class FnNode(ASTNode):
    def __init__(
        self,
        typ: TT,
        ident: IdentNode,
        params: dict[str, TT],
        body: StmtNode,
        token: tok.Token,
    ) -> None:
        self.typ = typ
        self.ident = ident
        self.params = params
        self.body = body
        self.token = token
        self.kind = "fn"

    def __repr__(self) -> str:
        return f"FN {self.typ.name} {self.ident.nm} @({self.token.typ.name} '{self.token.val}' {self.token.pos} {self.token.ln} {self.token.ppos}) {self.body}"


class ChNode(ASTNode):
    def __init__(self, ident: IdentNode, expr: GrpNode, token: tok.Token) -> None:
        self.ident = ident
        self.expr = expr
        self.token = token
        self.kind = "ch"

    def __repr__(self) -> str:
        return f"CH {self.ident} {self.expr}"
