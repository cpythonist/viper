import typing as ty


def pformat(
    arr: list[ty.Any] | tuple[ty.Any, ...] | dict[ty.Any, ty.Any],
    prevIndent: int = 0,
    indent: int = 4,
    lastElem: bool = True,
) -> list[str]:
    """
    A custom pretty print function.
    Stupidly long var names.
    """
    toRet: list[str]

    arrLen = len(arr)
    prevIndentSpaces = " " * prevIndent
    indentSpaces = " " * indent
    toRet = []
    toRetApp = toRet.append
    toRetExt = toRet.extend

    if isinstance(arr, list):
        braces = "[", "]"
    elif isinstance(arr, tuple):
        braces = "(", ")"
    elif isinstance(arr, dict):
        braces = "{", "}"
    else:
        braces = "$", "$"

    toRetApp(prevIndentSpaces + braces[0] + "\n")
    for idx, i in enumerate(arr):
        if hasattr(i, "__iter__"):
            toRetExt(pformat(i, prevIndent + indent, indent, idx == arrLen - 1))
            continue
        toRetApp(
            prevIndentSpaces + indentSpaces + str(i) + ("," if idx < arrLen - 1 else "") + "\n"
        )
    toRetApp(prevIndentSpaces + braces[1] + ("," if not lastElem else "") + "\n")

    return toRet


def pprn(
    arr: list[ty.Any] | tuple[ty.Any, ...] | dict[ty.Any, ty.Any],
    prevIndent: int = 0,
    indent: int = 4,
    lastElem: bool = True,
) -> None:
    print("".join(pformat(arr, prevIndent, indent, lastElem)))
