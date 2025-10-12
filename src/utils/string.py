import utils.consts as uconst


# These functions are defined because I don't trust str.isalnum(), str.isdigit(), etc. because they
# return True for non-ASCII characters too, which I REALLY don't want to happen
def isAlpha(txt: str) -> bool:
    return "a" <= txt <= "z" or "A" <= txt <= "Z"


def isDigit(txt: str) -> bool:
    return "0" <= txt <= "9"


def isAlNum(txt: str) -> bool:
    return isAlpha(txt) or isDigit(txt)


def vRepr(txt: str) -> str:
    """
    Escapes special characters in the given string. Basically Python's repr(...), but only with
    characters Viper recognises.
    > param txt: The string to escape
    > return: The escaped string
    """
    for i, char in enumerate(txt):
        if char in uconst.ESC_CHAR_MAP:
            txt = uconst.EMP_JOIN((txt[:i], uconst.ESC_CHAR_MAP[char], txt[i + 1 :]))
    return txt
