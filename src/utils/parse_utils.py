import core.err_disp as err
import core.token_ as tok


class ParseErrEntry:
    def __init__(self, errStr: str, offendingTok: tok.Token) -> None:
        self.errStr = errStr
        self.offendingTok = offendingTok


class ParseErrs:
    def __init__(self) -> None:
        self.errs: list[ParseErrEntry]

        self.errs = []

    def add(self, errStr: str, offendingTok: tok.Token) -> None:
        if not isinstance(errStr, str) and not isinstance(offendingTok, tok.Token):
            raise err.LogicalErr.ArrElemTypErr(
                "Invalid type in function parse_utils.ParseErrs.add(...): 'errStr' or 'offendingTok'"
            )

        self.errs.append(ParseErrEntry(errStr, offendingTok))
