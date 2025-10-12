import core.ast_nodes as ast
import core.err_disp as err
import core.token_ as tok

import core.parser.engine as par
import core.parser.pruner as pruner

import core.semalyser.analyse_ch_node as anach
import core.semalyser.analyse_fn_node as anafn
import core.semalyser.analyse_grp_node as anagrp
import core.semalyser.analyse_if_node as anaif
import core.semalyser.analyse_let_node as analet
import core.semalyser.analyse_prn_node as anaprn
import core.semalyser.analyse_ret_node as anaret
import core.semalyser.analyse_stmt_node as anastmt
import core.semalyser.analyse_while_node as anawhile
import core.semalyser.typ_chk_exprs as typchkexprs

import utils.gen as ugen
import utils.sem_utils as semutils
import utils.sem_err_typ_strs as uetstrs

TT = tok.TokenTypes


class SemanticAnalyser(
    typchkexprs.TypChkExprsSemalyserMixin,
    anach.ChAnalyserMixin,
    anafn.FnAnalyserMixin,
    anagrp.GrpAnalyserMixin,
    anaif.IfAnalyserMixin,
    analet.LetAnalyserMixin,
    anaret.RetAnalyserMixin,
    anaprn.PrnAnalyserMixin,
    anastmt.StmtAnalyserMixin,
    anawhile.WhileAnalyserMixin,
):
    """
    Check the AST if it is semantically correct.
    > param parser: The parser object
    > param pruner: The pruner object
    > param tree: The pruned AST
    """

    def __init__(
        self, parser: par.Parser, pruner: pruner.ASTPruner, tree: list[ast.ASTNode]
    ) -> None:
        self.symTable = semutils.SymTable(
            {"module": semutils.ScopeEntry(nm="module", allVars={}, parent=None, isFn=False)}
        )

        self.parser = parser
        self.pruner = pruner
        self.tree = tree
        self.compile = True
        self.semErrs = semutils.SemErrs()
        self.semErrsAdd = self.semErrs.add
        self.availErrs = ugen.getInnerClses(err.SemanticErr, err.Err)

        # Operators
        self.unaryOps = self.parser.unaryOps
        self.binCompOps = self.parser.exprOps
        self.binAriOps = self.parser.factorOps + self.parser.termOps
        self.binOps = self.binAriOps + self.binCompOps

        # Legal types: unary operators
        self.unaryPlusLegal = (TT.INT, TT.FLOAT)
        self.unaryMinusLegal = (TT.INT, TT.FLOAT)

        # Legal types: binary operators
        self.binPlusLegal = (TT.INT, TT.FLOAT, TT.STR)
        self.binMinusLegal = (TT.INT, TT.FLOAT, TT.STR)
        self.binAsteriskLegal = (TT.INT, TT.FLOAT)
        self.binFSlashLegal = (TT.INT, TT.FLOAT)
        self.binDollarLegal = (TT.INT, TT.FLOAT)
        self.binPercentLegal = (TT.INT, TT.FLOAT)
        self.binCaretLegal = (TT.INT, TT.FLOAT)

        # Just to keep the scope names unique
        self.nodeNo = 1

    def error(self, errCls: type[err.Err], msg: str, token: tok.Token) -> None:
        """
        Display an error message.
        > param errCls: The error class
        > param msg: The error message
        > param token: The offending token
        """
        if errCls not in self.availErrs:
            raise err.LogicalErr.NoSuchErr(f"No such parser error class: '{errCls.__name__}'")
        errCls(msg, token.pos, token.ln, token.ppos)

    def _repUndefdVar(self, token: tok.Token) -> None:
        self.error(err.SemanticErr.undefdVar, f"Undefined variable: '{token.val}'", token)

    def _repTypMismatch(self, op: TT, tokPos: int, tokLn: int, tokPPos: int, *typs: TT) -> None:
        self.error(
            err.SemanticErr.typMismatch,
            f"Type mismatch for operator {op.name}: {', '.join(i.name for i in typs)}",
            tok.Token(TT.DUMMY, "", tokPos, tokLn, tokPPos),
        )

    def _repInvOp(self, op: TT, tokPos: int, tokLn: int, tokPPos: int, *typs: TT) -> None:
        self.error(
            err.SemanticErr.invOp,
            f"Cannot perform operation {op.name} on type(s) {', '.join(i.name for i in typs)}",
            tok.Token(TT.DUMMY, "", tokPos, tokLn, tokPPos),
        )

    def calcIndent(self, nodeLvl: int) -> str:
        return "    " * (nodeLvl // 2)

    def analyseNode(
        self, node: ast.ASTNode, scope: str, parentNode: ast.ASTNode | None
    ) -> tuple[ast.ASTNode, bool]:
        node.parent = parentNode
        nodeProb = False

        if type(node) == ast.StmtNode:
            tmp = self.analyseStmtNode(node, scope)
            if isinstance(tmp, str):
                nodeProb = True
                self.semErrsAdd(tmp, node)
            else:
                node = tmp

        elif type(node) == ast.LiteralNode:
            pass

        elif type(node) == ast.GrpNode:
            tmp = self.analyseGrpNode(node, scope)
            if isinstance(tmp, str):
                nodeProb = True
                self.semErrsAdd(tmp, node)

        elif type(node) == ast.PrnNode:
            tmp = self.analysePrnNode(node, scope)
            if isinstance(tmp, str):
                nodeProb = True
                self.semErrsAdd(tmp, node)

        elif type(node) == ast.LetNode:
            tmp = self.analyseLetNode(node, scope)
            if isinstance(tmp, str):
                nodeProb = True
                self.semErrsAdd(tmp, node)

        elif type(node) == ast.IfNode:
            tmp = self.analyseIfNode(node, scope)
            if isinstance(tmp, str):
                nodeProb = True
                self.semErrsAdd(tmp, node)

        elif type(node) == ast.WhileNode:
            tmp = self.analyseWhileNode(node, scope)
            if isinstance(tmp, str):
                nodeProb = True
                self.semErrsAdd(tmp, node)

        elif type(node) == ast.FnNode:
            self.analyseFnNode(node, scope)

        elif type(node) == ast.ChNode:
            tmp = self.analyseChNode(node, scope)
            if isinstance(tmp, str):
                nodeProb = True
                self.semErrsAdd(tmp, node)

        elif type(node) == ast.RetNode:
            tmp = self.analyseRetNode(node, scope, parentNode)
            if isinstance(tmp, str):
                nodeProb = True
                self.semErrsAdd(tmp, node)

        elif type(node) == ast.ErrNode:
            nodeProb = True
            self.semErrsAdd(uetstrs.ErrNodeETS.errNode, node)

        self.nodeNo += 1
        return (node, nodeProb)

    def analyseTree(
        self, tree: list[ast.ASTNode], scopeNm: str, parentNode: ast.ASTNode | None
    ) -> None:
        for node in tree:
            self.analyseNode(node, scopeNm, parentNode)
