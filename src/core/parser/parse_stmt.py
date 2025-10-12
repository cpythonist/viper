# Filename: src\\core\\parser\\parse_stmt.py
# Description:

import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
GEN_ESTRS = uetstr.GenETS


class StmtParserMixin(pproto.ParserProtocol):
    def parseStmt(self) -> ast.ASTNode:
        """
        Parse a statement in the source.
        > return: The parsed statement (I dunno what else to write here)
        """
        node: ast.ASTNode

        node = ast.StmtNode(self.token)
        curTok = self.token

        if curTok.typ == TT.KEYWD:
            if curTok.val == "let":
                node = self.parseLet()
            elif curTok.val == "if":
                node = self.parseIf()
            elif curTok.val == "while":
                node = self.parseWhile()
            elif curTok.val == "prn":
                node = self.parsePrn()
            elif curTok.val == "break":
                node = self.parseBreak()
            elif curTok.val == "conti":
                node = self.parseConti()
            elif curTok.val == "fn":
                node = self.parseFn()
            elif curTok.val == "ch":
                node = self.parseCh()
            elif curTok.val == "ret":
                node = self.parseRet()
            elif 1000 <= curTok.typ.value <= 1099:
                node = ast.ErrNode(GEN_ESTRS.unexptdTyp, curTok)
            elif 900 <= curTok.typ.value <= 999:
                node = ast.ErrNode(GEN_ESTRS.unexptdCfg, curTok)
            else:
                node = ast.ErrNode(GEN_ESTRS.notImpld, curTok)

        elif curTok.typ == TT.SEMICLN:
            pass

        elif curTok.typ == TT.LFLBRAC:
            node = self.parseCmpndStmt()

        else:
            node = self.parseExpr()

        if type(node) == ast.ErrNode:
            self.skipTillResyncToks()
        elif not self.chkTok(TT.SEMICLN):
            node = ast.ErrNode(GEN_ESTRS.noSemiCln, self.token, node)
            self.skipTillResyncToks()
        else:
            self.nxtTok()

        return node
