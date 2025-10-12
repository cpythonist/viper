#
# FILENAME: src\core\parser\parse_cfg.py
# DESCRIPTION: Contains logic to parse the configuration statements at the start of the program.
#

import core.ast_nodes as ast
import core.token_ as tok

import core.parser.protocol as pproto

import utils.parse_err_typ_strs as uetstr

TT = tok.TokenTypes
CFG_ESTRS = uetstr.ConfigETS
VALID_VALS = {"typing": ("sta", "dyn"), "delim": ("brac", "ws")}
DEF_CFG = ast.CfgNode({key: VALID_VALS[key][0] for key in VALID_VALS})
NO_OF_CFG = len(VALID_VALS)


class CfgParserMixin(pproto.ParserProtocol):
    def skipCfgWS(self, j: int) -> None:
        if j < NO_OF_CFG - 1:
            self.skipWSToks()

    def _parse1CfgStmt(self, param: str) -> tuple[str, str] | tuple[str, None]:
        """
        Parse one configuration statement.
        > param param: The configuration parameter name
        > return: A two-length tuple of either a string and a string, or a str and None.
                  (str and str) is returned when parsing was successful, else (str, None).
        """
        # Configuration keyword
        if not (self.chkTok(TT.KEYWD, param) and self.chkTokRange((900, 999), TT[param.upper()])):
            return CFG_ESTRS.noCfgKeywd, None
        self.nxtTok()

        # Value of the config param
        if self.token.val.lower() not in VALID_VALS[param]:
            return CFG_ESTRS.invCfgVal, None
        val = self.token.val
        self.nxtTok()

        # Finally, semicolon
        if not self.chkTok(TT.SEMICLN):
            return CFG_ESTRS.noCfgSemcln, None
        self.nxtTok()

        return param, val

    def parseCfg(self) -> ast.CfgNode | list[ast.ErrNode]:
        """
        Parse all the configuration statements.
        > return: The parsed configuration node or a list of ErrNode.`
        """
        config: dict[str, str]
        errs: list[ast.ErrNode]

        config = {}
        errs = []

        for j, nm in enumerate(VALID_VALS):
            lastCfgStmt = j == NO_OF_CFG - 1

            nmOrErr, val = self._parse1CfgStmt(nm)
            # val being None indicates an error during parsing; check self._parse1CfgStmt(...)
            if val is None:
                errs.append(ast.ErrNode(nmOrErr, self.token, DEF_CFG))
                if lastCfgStmt:
                    break
                self.skipTillResyncToks(
                    TT.KEYWD,
                    [i.name.lower() for i in TT if self.chkTokRange((900, 999), i)],
                )
                continue

            config[nmOrErr] = val

        return ast.CfgNode(config) if not errs else errs
