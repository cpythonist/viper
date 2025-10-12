import typing as ty

import core.err_disp as err
import core.token_ as tok
import core.ast_nodes as ast

TT = tok.TokenTypes


class ScopeEntry:
    def __init__(self, nm: str, allVars: dict[str, TT], parent: str | None, isFn: bool) -> None:
        self.nm = nm
        self.allVars = allVars
        self.parent = parent
        self.isFn = isFn

    # TODO: Check if you need to change this function's behaviour such that it reports an error
    # if the scope is not found, instead of letting the calling function handle it. Else, add a
    # parameter to specify whether to throw an error
    def getTyp(self, varNm: str) -> TT | None:
        return self.allVars.get(varNm)

    def setVar(self, varNm: str, typ: TT) -> tuple[str, TT] | None:
        # TODO: Check for the validity of the identifier, if needed, just in case
        if self.getTyp(varNm) is not None:
            return None
        self.allVars[varNm] = typ
        return (varNm, typ)

    def rmVar(self, varNm: str) -> TT | None:
        return self.allVars.pop(varNm, None)

    def __getitem__(self, key: str) -> TT | None:
        return self.allVars.get(key, None)

    def __setitem__(self, key: str, val: TT) -> None:
        self.allVars[key] = val

    def __contains__(self, key: str) -> TT | None:
        return self.allVars.get(key, None)

    def __repr__(self) -> str:
        return f"nm: '{self.nm}', allVars: {self.allVars}"


class SymTable:
    def __init__(self, symTable: dict[str, ScopeEntry]) -> None:
        self.get: ty.Callable[[str], ScopeEntry | None]

        self.data = symTable
        self.get = lambda scope: self.data.get(scope)
        self.getAll = lambda: tuple(self.data.keys())

    # TODO: Check if you need to change self.get(...)'s behaviour such that it reports an error
    # if the scope is not found, instead of letting the calling function handle it. Else, add a
    # parameter to specify whether to throw an error; you might need to discard the lambda and
    # write a full-fledged function

    def crtScope(
        self,
        scopeNm: str,
        initVals: dict[str, TT] = {},
        parent: str | None = None,
        isFn: bool = False,
    ) -> ScopeEntry | None:
        if self.get(scopeNm) is not None:
            return None
        self.data[scopeNm] = (newScope := ScopeEntry(scopeNm, initVals, parent, isFn))
        return newScope

    def setVar(self, scopeNm: str, varNm: str, typ: TT) -> tuple[str, TT] | None:
        scope = self.get(scopeNm)
        if scope is None:
            return None
        scope.setVar(varNm, typ)
        return (varNm, typ)

    def rmScope(self, scopeNm: str) -> None:
        if scopeNm in self.data:
            self.data.pop(scopeNm)

    def rmVar(self, scopeNm: str, varNm: str) -> TT | None:
        scope = self.get(scopeNm)
        if scope is None:
            return None
        return scope.rmVar(varNm)

    def __getitem__(self, key: str) -> ScopeEntry:
        return self.data[key]

    def __setitem__(self, key: str, val: ScopeEntry):
        self.data[key] = val

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def __repr__(self) -> str:
        return (
            "-----\n"
            + "SYMBOL TABLE\n"
            + "\n".join((str(v) for v in self.data.values()))
            + "\n-----"
        )


class SemErrEntry:
    def __init__(self, errStr: str, offendingNode: ast.ASTNode) -> None:
        self.errStr = errStr
        self.offendingNode = offendingNode


class SemErrs:
    def __init__(self) -> None:
        self.errs: list[SemErrEntry]

        self.errs = []

    def add(self, errStr: str, offendingNode: ast.ASTNode) -> None:
        """
        Add an element to the list of semantic errors.
        > param errStr: The error type string
        > param offendingNode: The offending node
        """
        if not isinstance(errStr, str) and not isinstance(offendingNode, ast.ASTNode):
            raise err.LogicalErr.ArrElemTypErr(
                "Invalid type in function sem_utils.SemErrs.add(...): 'errStr' or 'offendingNode'"
            )

        self.errs.append(SemErrEntry(errStr, offendingNode))
