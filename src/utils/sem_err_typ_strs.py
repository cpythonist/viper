allGood = ""


class TypChkExprs:
    allGood = ""

    class ChkIdent:
        noSuchIdent = "no-such-ident"

    class ChkUnary:
        invUnaryOp = "inv-unary-op"
        illegUnaryPlusTyp = "illeg-unary-plus-typ"
        illegUnaryMinusTyp = "illeg-unary-minus-typ"

    class ChkBin:
        invBinOp = "inv-bin-op"
        operandTypMismatch = "operand-typ-mismatch"
        illegBinPlusTyp = "illeg-bin-plus-typ"
        illegBinMinusTyp = "illeg-bin-minus-typ"
        illegBinAsteriskTyp = "illeg-bin-asterisk-typ"
        illegBinFSlashTyp = "illeg-bin-fslash-typ"
        illegBinDollarTyp = "illeg-bin-dollar-typ"
        illegBinPercentTyp = "illeg-bin-percent-typ"
        illegBinCaretTyp = "illeg-bin-caret-typ"


class LetStmtETS:
    typMismatch = "typ-mismatch"


class ChStmtETS:
    noSuchVar = "no-such-ident"
    typMismatch = "typ-mismatch"


class WhileStmtETS:
    bodyErr = "while-body-err"


class RetStmtETS:
    typMismatch = "typ-mismatch"
    notInsideFn = "not-inside-fn"


class ErrNodeETS:
    errNode = "err-node"
