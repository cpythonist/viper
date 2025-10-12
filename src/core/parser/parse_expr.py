import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
EXPR_ESTRS = uetstr.ExprETS


class ExprParserMixin(pproto.ParserProtocol):
    def parseExpr(self) -> ast.GrpNode | ast.ErrNode:
        """
        Parse a general expression.
        > return: The parsed expression
        """
        node = self.parseArithExpr()
        if type(node) == ast.ErrNode:
            return node

        while self.token.typ in self.exprOps:
            opTok = self.token
            self.nxtTok()

            rt = self.parseArithExpr()
            if type(rt) == ast.ErrNode:
                return rt

            node = ast.BinOpNode(node, opTok, rt)

        # This is sure as hell a bad comment;
        # Check if the node obtained is an ErrNode, and if it's not and isn't a GrpNode, then
        # make it a GrpNode
        if not isinstance(node, ast.ErrNode) and not isinstance(node, ast.GrpNode):
            node = ast.GrpNode(node)

        return node

    def parseArithExpr(
        self,
    ) -> (
        ast.LiteralNode
        | ast.IdentNode
        | ast.GrpNode
        | ast.UnaryOpNode
        | ast.BinOpNode
        | ast.ErrNode
    ):
        """
        Parse an arithmetic expression.
        > return: The parsed term
        """
        node = self.parseTerm()
        if type(node) == ast.ErrNode:
            return node

        while self.token.typ in self.termOps:
            opTok = self.token
            self.nxtTok()

            rt = self.parseTerm()
            if type(rt) == ast.ErrNode:
                return rt

            node = ast.BinOpNode(node, opTok, rt)

        return node

    def parseTerm(
        self,
    ) -> (
        ast.LiteralNode
        | ast.IdentNode
        | ast.GrpNode
        | ast.UnaryOpNode
        | ast.BinOpNode
        | ast.ErrNode
    ):
        """
        Parse a factor.
        > return: The parsed factor
        """
        node = self.parseExpo()
        if type(node) == ast.ErrNode:
            return node

        while self.token.typ in self.factorOps:
            opTok = self.token
            self.nxtTok()

            rt = self.parseExpo()
            if type(rt) == ast.ErrNode:
                return rt

            node = ast.BinOpNode(node, opTok, rt)

        return node

    def parseExpo(
        self,
    ) -> (
        ast.LiteralNode
        | ast.IdentNode
        | ast.GrpNode
        | ast.UnaryOpNode
        | ast.BinOpNode
        | ast.ErrNode
    ):
        """
        Parse the exponentiation operator.
        > return: The parsed exponentiation component
        """
        node = self.parseUnary()

        if type(node) == ast.ErrNode:
            return node

        while self.token.typ == TT.CARET:
            opTok = self.token
            self.nxtTok()

            rt = self.parseUnary()
            if type(rt) == ast.ErrNode:
                return rt

            node = ast.BinOpNode(node, opTok, rt)

        return node

    def parseUnary(
        self,
    ) -> ast.LiteralNode | ast.IdentNode | ast.GrpNode | ast.UnaryOpNode | ast.ErrNode:
        """
        Parse a unary component of an expression.
        > return: The parsed component
        """
        opTok = None
        stTok = self.token

        if self.token.typ in self.unaryOps:
            opTok = self.token
            self.nxtTok()

        rt = self.parsePrimary()
        if type(rt) == ast.ErrNode:
            return rt

        if opTok is None:
            return rt

        node = ast.UnaryOpNode(opTok, rt, stTok)
        return node

    def parsePrimary(
        self,
    ) -> ast.LiteralNode | ast.IdentNode | ast.GrpNode | ast.ErrNode:
        """
        Parse a primary component of an expression (which itself is an expression).
        > return: The parsed component
        """
        curTok = self.token

        if curTok.typ in self.primValidTyps:
            node = ast.LiteralNode(curTok)
            self.nxtTok()
        elif curTok.typ == TT.IDENT:
            node = ast.IdentNode(curTok)
            self.nxtTok()
        elif curTok.typ == TT.LPAREN:
            self.nxtTok()
            node = self.parseExpr()
            if self.token.typ != TT.RPAREN:
                node = ast.ErrNode(EXPR_ESTRS.noCloRParen, self.token)
            else:
                self.nxtTok()
        else:
            node = ast.ErrNode(EXPR_ESTRS.exptdPrim, curTok)

        return node
