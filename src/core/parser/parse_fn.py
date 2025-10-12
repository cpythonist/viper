import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
FN_ESTRS = uetstr.FnETS


class FnParserMixin(pproto.ParserProtocol):
    def parseFn(self) -> ast.FnNode | ast.ErrNode:
        fnTyp: TT
        paramTyp: TT

        params: dict[str, TT]

        if not self.chkTok(TT.KEYWD, "fn"):
            return ast.ErrNode(FN_ESTRS.noFn, self.token)
        fnTok = self.token
        self.nxtTok()

        if not (self.chkTok(TT.KEYWD) and 1000 <= TT[self.token.val.upper()].value <= 1099):  # type: ignore
            return ast.ErrNode(FN_ESTRS.exptdTyp, self.token)
        fnTyp = TT[self.token.val.upper()]  # type: ignore
        self.nxtTok()

        if not self.chkTok(TT.IDENT):
            return ast.ErrNode(FN_ESTRS.noIdent, self.token)
        ident = ast.IdentNode(self.token)
        self.nxtTok()

        if not self.chkTok(TT.LPAREN):
            return ast.ErrNode(FN_ESTRS.noLParen, self.token)
        self.nxtTok()

        params = {}
        while not self.chkTok(TT.RPAREN):
            if not self.chkTok(TT.KEYWD) or not (1000 <= TT[self.token.val.upper()].value <= 1099):  # type: ignore
                return ast.ErrNode(FN_ESTRS.noParamTyp, self.token)
            paramTyp = TT[self.token.val.upper()]  # type: ignore
            self.nxtTok()

            if not self.chkTok(TT.IDENT):
                return ast.ErrNode(FN_ESTRS.noParamIdent, self.token)
            paramIdent = self.token.val
            self.nxtTok()

            params[paramIdent] = paramTyp

            if self.token.typ == TT.COMMA:
                self.nxtTok()

        if not self.chkTok(TT.RPAREN):
            return ast.ErrNode(FN_ESTRS.noRParen, self.token)
        self.nxtTok()

        body = self.parseCmpndStmt()
        return ast.FnNode(fnTyp, ident, params, body, fnTok)
