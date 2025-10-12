import sys

import inspect as ip
import typing as ty
import traceback as tb

import utils.consts as uconst


def getInnerClses(outerCls: object, parent: object | None = None) -> ty.List[type]:
    # NOTE: Note that outerCls and parent are changed here!
    if not isinstance(outerCls, type):
        outerCls = outerCls.__class__
    if not isinstance(parent, type):
        parent = parent.__class__

    if parent is None:
        toRet = [cls for cls in outerCls.__dict__.values() if ip.isclass(cls)]
    else:
        toRet = [
            cls for cls in outerCls.__dict__.values() if ip.isclass(cls) and issubclass(cls, parent)
        ]

    return toRet


def isUnifTyp(
    arr: list[ty.Any] | tuple[ty.Any, ...] | dict[ty.Any, ty.Any],
    exactMatch: bool = False,
    noEmpty: bool = False,
) -> tuple[bool, ty.Any]:
    """
    Check if all the elements in an array have the same type.
    > param arr: The array to check
    > param exactMatch: Whether to check for exact type matches or not
    > param noEmpty: If True, returns False if the array is empty
    > return: True if all the elements have the same type, False otherwise
    """
    if not isinstance(arr, (list, tuple, dict)):
        raise err.LogicalErr.ExptdDiffTyp(
            "Expected a list, tuple, or dict for param 'arr' in isUnifTyp(...)"
        )

    if not arr:
        return (False if noEmpty else True, None)

    first = arr[0]
    if not exactMatch:
        return (all(isinstance(i, type(first)) for i in arr), first)
    return (all(type(i) == type(first) for i in arr), first)


def debug(msg: str) -> None:
    uconst.B_CON_LGR.debug(msg)
    uconst.FL_LGR.debug(msg)


def info(msg: str) -> None:
    uconst.B_CON_LGR.info(msg)
    uconst.FL_LGR.info(msg)


def warn(msg: str) -> None:
    uconst.YELLOW_B_CON_LGR.warning(msg)
    uconst.FL_LGR.warning(msg)


def error(msgOrE: str | Exception) -> None:
    if isinstance(msgOrE, Exception):
        uconst.RED_B_CON_LGR.error(f"(DEBUG) {msgOrE.__class__.__name__}: {msgOrE}")
        uconst.FL_LGR.error(tb.format_exc())
    else:
        uconst.RED_B_CON_LGR.error(msgOrE)
        uconst.FL_LGR.error(msgOrE)


def crit(e: Exception, errCode: int | None) -> None:
    unrecoverable = "Unrecoverable Viper error\n"

    if isinstance(e, str):
        # TODO: Edit expr inside uconst.RED_B_CON_LGR.critical(...) call in release builds
        uconst.RED_B_CON_LGR.critical(unrecoverable + e)
        uconst.FL_LGR.critical(unrecoverable + e)
    elif isinstance(e, Exception):  # type: ignore
        # TODO: Edit expr inside uconst.RED_B_CON_LGR.critical(...) call in release builds
        uconst.RED_B_CON_LGR.critical(unrecoverable + f"(DEBUG) {e.__class__.__name__}: {e}")
        uconst.FL_LGR.critical(unrecoverable + tb.format_exc())

    if errCode is not None:
        sys.exit(errCode)


def fatal(e: str | Exception, errCode: int | None) -> None:
    unrecoverable = "Unrecoverable Viper error\n"

    if isinstance(e, str):
        # TODO: Edit expr inside uconst.RED_B_CON_LGR.fatal(...) call in release builds
        uconst.RED_B_CON_LGR.fatal(unrecoverable + e)
        uconst.FL_LGR.fatal(unrecoverable + e)
    elif isinstance(e, Exception):  # type: ignore
        # TODO: Edit expr inside uconst.RED_B_CON_LGR.fatal(...) call in release builds
        uconst.RED_B_CON_LGR.fatal(unrecoverable + f"(DEBUG) {e.__class__.__name__}: {e}")
        uconst.FL_LGR.fatal(unrecoverable + tb.format_exc())

    if errCode is not None:
        sys.exit(errCode)


def isAlpha(string: str) -> bool:
    """
    Check if the string is composed only of alphabets (like, actual English alphabets).

    > param string: The string to be checked
    > return: Boolean value stating if the string was composed only of the English alphabet
    """
    if not isinstance(string, str):
        raise TypeError(f"Expected type 'str'; got {type(string).__class__.__name__}")

    for i in string:
        if ord(i) not in uconst.ALPHA_RANGE:
            return False

    return True


def isNum(string: str) -> bool:
    """
    Check if the string is composed only of numbers (like, actual numbers).

    > param string: The string to be checked
    > return: Boolean value stating if the string was composed only of numbers
    """
    if not isinstance(string, str):
        raise TypeError(f"Expected type 'str'; got {type(string).__class__.__name__}")

    for i in string:
        if ord(i) not in uconst.NUM_RANGE:
            return False

    return True
