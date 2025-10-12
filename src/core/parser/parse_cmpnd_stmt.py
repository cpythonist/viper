import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
CMPND_STMT_ESTRS = uetstr.CmpndStmtETS


class CmpndStmtParserMixin(pproto.ParserProtocol):
    def parseCmpndStmt(self) -> ast.StmtNode | ast.ErrNode:
        """
        Parse a compound statement (i.e. a code block).
        > return: Statement node of the parsed compound statement
        """
        stmts: list[
            ast.LetNode
            | ast.IfNode
            | ast.WhileNode
            | ast.BreakNode
            | ast.ContiNode
            | ast.PrnNode
            | ast.FnNode
            | ast.StmtNode
            | ast.NotImplementedNode
            | ast.ErrNode
        ]

        stmts = []
        stmtsApp = stmts.append
        startTok = self.token

        if self.token.typ != TT.LFLBRAC:
            return ast.ErrNode(CMPND_STMT_ESTRS.noLFlBrac, self.token, *stmts)
        self.nxtTok()

        while self.token.typ != TT.RFLBRAC and self.token.typ != TT.EOF:
            stmtsApp(self.parseStmt())

        if self.token.typ != TT.RFLBRAC:
            return ast.ErrNode(CMPND_STMT_ESTRS.noRFlBrac, self.token, *stmts)
        self.nxtTok()

        return ast.StmtNode(startTok, *stmts)
