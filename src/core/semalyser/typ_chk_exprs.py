import sys

import core.ast_nodes as ast
import core.token_ as tok

import core.semalyser.protocol as semproto

import utils.gen as ugen
import utils.sem_utils as semutils
import utils.sem_err_typ_strs as uestrs

TT = tok.TokenTypes
TYP_CHK_ERRS = uestrs.TypChkExprs


class TypChkExprsSemalyserMixin(semproto.SemalyserProtocol):
    def _litChk(self, exprNode: ast.LiteralNode) -> tuple[str, TT | None, int, int, int]:
        tokTyp = exprNode.token.typ
        tokPos = exprNode.token.pos
        tokLn = exprNode.token.ln
        tokPPos = exprNode.token.ppos

        # YOU SHOULDN'T BE EVALUATING THE EXPRESSIONS! YOU SHOULD BE CHECKING THEIR TYPES! GODDAMN IDIOT!
        # # Basic datatypes; I really have no idea how I'll extend this for other types
        # if typ == TT.INT:
        #     res = int(res)
        # elif typ == TT.FLOAT:
        #     res = float(res)
        # elif typ == TT.BOOL:
        #     res = {"true": True, "false": False}[res]
        # elif typ == TT.STR:
        #     # Just for clarity; this elif clause is actually not needed
        #     pass

        return TYP_CHK_ERRS.allGood, tokTyp, tokPos, tokLn, tokPPos

    def _chkIdent(
        self, exprNode: ast.IdentNode, scopeVars: semutils.ScopeEntry
    ) -> tuple[str, TT | None, int, int, int]:
        tokPos = exprNode.token.pos
        tokLn = exprNode.token.ln
        tokPPos = exprNode.token.ppos
        varTyp = scopeVars.getTyp(exprNode.token.val)

        # Undefined variable access; tell the user to go kill himself
        if varTyp is None:
            # TODO: Add error reporting for undefined variables, if needed
            return TYP_CHK_ERRS.ChkIdent.noSuchIdent, None, tokPos, tokLn, tokPPos

        return TYP_CHK_ERRS.allGood, varTyp, tokPos, tokLn, tokPPos

    def _chkUnary(
        self, exprNode: ast.UnaryOpNode, scope: str
    ) -> tuple[str, TT | None, int, int, int]:
        op = exprNode.op
        msg, rtTyp, tokPos, tokLn, tokPPos = self.typChkExprs(exprNode.rt, scope)

        # Operator is not an unary operator
        if op.typ not in self.unaryOps:
            return TYP_CHK_ERRS.ChkUnary.invUnaryOp, None, tokPos, tokLn, tokPPos

        # A problem with the right operand
        if rtTyp is None:
            return msg, None, tokPos, tokLn, tokPPos

        # Cannot do unary plus on the right operand
        if op.typ == TT.PLUS and rtTyp not in self.unaryPlusLegal:
            return TYP_CHK_ERRS.ChkUnary.illegUnaryPlusTyp, None, tokPos, tokLn, tokPPos

        # Cannot do unary minus on the right operand
        if op.typ == TT.MINUS and rtTyp not in self.unaryMinusLegal:
            return (
                TYP_CHK_ERRS.ChkUnary.illegUnaryMinusTyp,
                None,
                tokPos,
                tokLn,
                tokPPos,
            )

        return TYP_CHK_ERRS.allGood, rtTyp, tokPos, tokLn, tokPPos

    def _chkBin(self, exprNode: ast.BinOpNode, scope: str) -> tuple[str, TT | None, int, int, int]:
        op = exprNode.op
        opTyp = op.typ
        opTokPos = op.pos
        opTokLn = op.ln
        opTokPPos = op.ppos

        ltMsg, ltTyp, ltTokPos, ltTokLn, ltTokPPos = self.typChkExprs(exprNode.lt, scope)
        rtMsg, rtTyp, rtTokPos, rtTokLn, rtTokPPos = self.typChkExprs(exprNode.rt, scope)

        if op.typ not in self.binOps:
            return TYP_CHK_ERRS.ChkBin.invBinOp, None, opTokPos, opTokLn, opTokPPos

        # Problem with the left operand
        if ltTyp is None:
            return ltMsg, None, ltTokPos, ltTokLn, ltTokPPos
        # Problem with the right operand
        elif rtTyp is None:
            return rtMsg, None, rtTokPos, rtTokLn, rtTokPPos

        # Left and right operand types do not match; remember, an important feature in the
        # language is that there are no implicit type conversions
        if ltTyp != rtTyp:
            return (
                TYP_CHK_ERRS.ChkBin.operandTypMismatch,
                None,
                ltTokPos,
                ltTokLn,
                ltTokPPos,
            )

        ### ltTyp and rtTyp are the same from here onwards ###

        # Cannot perform binary plus on the operands
        if opTyp == TT.PLUS and ltTyp not in self.binPlusLegal:
            return (
                TYP_CHK_ERRS.ChkBin.illegBinPlusTyp,
                None,
                ltTokPos,
                ltTokLn,
                ltTokPPos,
            )

        # Cannot perform binary minus on the operands
        if opTyp == TT.MINUS and ltTyp not in self.binMinusLegal:
            return (
                TYP_CHK_ERRS.ChkBin.illegBinMinusTyp,
                None,
                ltTokPos,
                ltTokLn,
                ltTokPPos,
            )

        # Cannot perform binary multiply on the operands
        if opTyp == TT.ASTERISK and ltTyp not in self.binAsteriskLegal:
            return (
                TYP_CHK_ERRS.ChkBin.illegBinAsteriskTyp,
                None,
                ltTokPos,
                ltTokLn,
                ltTokPPos,
            )

        # Cannot perform binary divide on the operands
        if opTyp == TT.FSLASH and ltTyp not in self.binFSlashLegal:
            return (
                TYP_CHK_ERRS.ChkBin.illegBinFSlashTyp,
                None,
                ltTokPos,
                ltTokLn,
                ltTokPPos,
            )

        # Cannot perform binary dollar on the operands
        if opTyp == TT.DOLLAR and ltTyp not in self.binDollarLegal:
            return (
                TYP_CHK_ERRS.ChkBin.illegBinDollarTyp,
                None,
                ltTokPos,
                ltTokLn,
                ltTokPPos,
            )

        # Cannot do binary mod on the operands
        if opTyp == TT.PERCENT and ltTyp not in self.binPercentLegal:
            return (
                TYP_CHK_ERRS.ChkBin.illegBinPercentTyp,
                None,
                ltTokPos,
                ltTokLn,
                ltTokPPos,
            )

        # Cannot do binary caret on the operands
        if opTyp == TT.CARET and ltTyp not in self.binCaretLegal:
            return (
                TYP_CHK_ERRS.ChkBin.illegBinCaretTyp,
                None,
                ltTokPos,
                ltTokLn,
                ltTokPPos,
            )

        # If the operator is a comparison operator, the type is guaranteed to be a boolean if
        # there is no type mismatch between the operands
        if opTyp in self.binCompOps:
            return TYP_CHK_ERRS.allGood, TT.BOOL, ltTokPos, ltTokLn, ltTokPPos

        # Otherwise, if the operator is an arithmetic operator, it has the same type as the
        # operand
        # TODO: Check if this has any exceptions, like if for some cases this rule is false
        return TYP_CHK_ERRS.allGood, ltTyp, ltTokPos, ltTokLn, ltTokPPos

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
    ) -> tuple[str, TT | None, int, int, int]:
        """
        Evaluates the types of expressions. A recursive function that calls itself to evaluate
        sub-expressions.
        > param exprNode: The expression node to evaluate
        > param scope: The scope to evaluate the expression in
        > return: A tuple of an error message, the type of the evaluated expression, the position
                  of the token, the line number of the token and the "print position" of the token

        """
        scopeVars = self.symTable.get(scope)

        # No such scope found in the symbol table; this is an edge case that was over-looked by me.
        # Well, not exactly an edge-case, but it is needed for nutcases like me who will insert an
        # undefined scope.
        if scopeVars is None:
            ugen.fatal(f"No such scope in the symbol table: '{scope}'", None)
            sys.exit(-1)

        if type(exprNode) == ast.LiteralNode:
            return self._litChk(exprNode)

        elif type(exprNode) == ast.IdentNode:
            return self._chkIdent(exprNode, scopeVars)

        elif type(exprNode) == ast.UnaryOpNode:
            return self._chkUnary(exprNode, scope)

        elif type(exprNode) == ast.BinOpNode:
            return self._chkBin(exprNode, scope)

        elif type(exprNode) == ast.GrpNode:
            return self.typChkExprs(exprNode.node, scope)

        else:
            ugen.fatal(f"Invalid expression type: {type(exprNode)}", None)
            sys.exit(-1)
