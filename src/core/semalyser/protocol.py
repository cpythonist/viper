import typing as ty

import core.ast_nodes as ast
import core.token_ as tok

import utils.sem_utils as semutils

TT = tok.TokenTypes


class SemalyserProtocol(ty.Protocol):
    symTable: semutils.SymTable

    unaryOps: tuple[TT, ...]
    unaryOps: tuple[TT, ...]
    binCompOps: tuple[TT, ...]
    binAriOps: tuple[TT, ...]
    binOps: tuple[TT, ...]

    unaryPlusLegal: tuple[TT, ...]
    unaryMinusLegal: tuple[TT, ...]

    binPlusLegal: tuple[TT, ...]
    binMinusLegal: tuple[TT, ...]
    binAsteriskLegal: tuple[TT, ...]
    binFSlashLegal: tuple[TT, ...]
    binDollarLegal: tuple[TT, ...]
    binPercentLegal: tuple[TT, ...]
    binCaretLegal: tuple[TT, ...]

    semErrs: semutils.SemErrs
    semErrsAdd: ty.Callable[[str, ast.ASTNode], None]
    nodeNo: int

    def calcIndent(self, nodeLvl: int) -> str: ...
    def analyseNode(
        self, node: ast.ASTNode, scope: str, parentNode: ast.ASTNode | None
    ) -> tuple[ast.ASTNode, bool]: ...
    def analyseTree(
        self, tree: list[ast.ASTNode], scopeNm: str, parentNode: ast.ASTNode | None
    ) -> None: ...
    def typChkExprs(
        self,
        exprNode: (
            ast.LiteralNode
            | ast.IdentNode
            | ast.UnaryOpNode
            | ast.BinOpNode
            | ast.GrpNode
            | ast.ErrNode
        ),
        scope: str,
    ) -> tuple[str, TT | None, int, int, int]: ...
