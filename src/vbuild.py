import os
import sys

import platform as pf
import pathlib as pl
import subprocess as sp


class HahaHehe(Exception):
    pass


def prnVer() -> None:
    """
    Print the version of the build program.
    """
    print(f"vbuild v{__version__}")


def prnHelp() -> None:
    """
    Print the help string.
    """
    print("\n".join(PRN_HELP_STR))


def repErr(typ: str, msg: str) -> None:
    if typ.lower() in ("err", "crit", "fatal", "debug", "info"):
        print(f"{typ.upper()}: {msg}")
    else:
        raise HahaHehe(f"Dumbass! There's no error type called '{typ}'!")


def reportArgErr(typ: str, msg: str, idx: int | list[int], elem: str) -> None:
    if isinstance(idx, int):
        idxStr = str(idx + 1)
    elif isinstance(idx, list):
        idxStr = str(", ".join(str(i + 1) for i in idx))
    else:
        raise HahaHehe("STOOBID: The index(ices) were neither int nor a list of ints!")

    print(f"{typ.upper()}_ERR: {msg} at position {idxStr}: {elem}")


def parseArgs(
    validOpts: tuple[str, ...], validFlags: tuple[str, ...]
) -> tuple[
    dict[int, str], dict[str, list[str | int | list[int]]], dict[str, list[None | int | list[int]]]
]:

    args: dict[int, str]
    opts: dict[str, list[str | int | list[int]]]
    flags: dict[str, list[None | int | list[int]]]

    reqdVec = sys.argv[1:]
    lenReqdVec = len(reqdVec)
    args = {}
    opts = {}
    flags = {}
    idx = 0

    while idx < lenReqdVec:
        elem = reqdVec[idx]

        # ARGUMENTS
        # Arg dict format: {idx: arg, ...}
        if elem[0] != "-":
            # If an arg starting w/ '-' needs to be specified, the '-' char can be escaped using a
            # '\'
            if len(elem) >= 2 and elem[0] == "\\" and elem[1] == "-":
                toApp = elem[1:]
            else:
                toApp = elem

            args[idx] = toApp

        # FLAGS
        # Flag dict format: {flag: [None/error code, [list of indices where that flag occurs]]}.
        elif elem[1:] in validFlags:
            # The flag has already been passed in the same cmd
            if elem[1:] in flags:
                reportArgErr("flag", "Repeated flag", idx, elem)
                flags[elem[1:]][0] = ERR_REPEATED_FLAG
            else:
                flags[elem[1:]] = [None, []]

            # Add the current index to the list of indices for each flag in dict flags
            flags[elem[1:]][1].append(idx)

        # OPTIONS
        # Opt dict format: {opt: [val/error code, [list of indices where that opt occurs]]}.
        else:
            elemSplit = elem[1:].partition("=")

            # The parsed option isn't valid
            if elemSplit[0] not in validOpts:
                reportArgErr("opt", "Invalid option", idx, "-" + elemSplit[0])
                if elemSplit[0] not in opts:
                    opts[elemSplit[0]] = [ERR_INV_ELEM, []]
                else:
                    opts[elemSplit[0]][0] = ERR_INV_ELEM

            # The opt-val pair isn't valid, i.e. there is no '=' char separating the opt and the
            # val.
            elif elemSplit[1] != "=":
                reportArgErr(
                    "opt", "Option and value must be separated by '='", idx, "-" + elemSplit[0]
                )
                if elemSplit[0] not in opts:
                    opts[elemSplit[0]] = [ERR_OPT_NO_EQ, []]
                else:
                    opts[elemSplit[0]][0] = ERR_OPT_NO_EQ

            else:
                # The opt has already been passed in the same cmd.
                if elemSplit[0] in opts:
                    reportArgErr("opt", "Repeated option", idx, "-" + elemSplit[0])
                    opts[elemSplit[0]][0] = ERR_REPEATED_OPT
                else:
                    opts[elemSplit[0]] = [elemSplit[2], []]

            # Add the curr idx to the list of idxs for each opt in dict opts.
            opts[elemSplit[0]][1].append(idx)

        idx += 1

    return args, opts, flags


# NOTE: I know that storing the equivalent opts and flags in a dict is extremely stupid and leads
# to data duplication (is that what it's called?) But I can't find a better method to do it,
# especially comparing it w/ my other bright idea of storing them in a tuple.
def areEquivOptFlagRepd(
    opts: dict[str, list[str | int | list[int]]],
    flags: dict[str, list[None | int | list[int]]],
    equivOpts: dict[str, str],
    equivFlags: dict[str, str],
) -> bool:

    # If the flag is one that has occured first, before an equivalent occured in the cmd, it will
    # be in the list firstRepdFlag. Yeah, I know, it's a dumb name, but whatever.
    # Similarly for the options.
    firstRepdOpt: list[str]
    firstRepdFlag: list[str]

    repeated = False
    firstRepdOpt = []
    firstRepdFlag = []

    for opt in opts:
        # The opt was the first to occur (before the equivalent) in the cmd, and thus is already
        # present in firstRepdOpt. So, continue, because that repeated option would already have
        # been reported in parseArgs(...).
        if len(opts[opt][1]) > 1:
            repeated = True
        # Current opt has occured before its equivalent, and has occured atleast once in the cmd.
        if opt in firstRepdOpt:
            continue
        # The current opt does not have any equivalent opt.
        if opt not in equivOpts:
            continue
        # The current opt's equivalent opt is present in the opts dict.
        if equivOpts[opt] in opts:
            # If the current opt isn't in firstRepdOpt and it's equivalent opt is also not in
            # firstRepdOpt, add the current opt to firstRepdOpt (meaning it's first being
            # encountered now, and it's equivalent wasn't encountered before that).
            if opt not in firstRepdOpt and equivOpts[opt] not in firstRepdOpt:
                firstRepdOpt.append(opt)
                continue
            reportArgErr(
                "opt", f"Repeated equivalent option of -{equivOpts[opt]}", opts[opt][1], "-" + opt
            )
            repeated = True

    for flag in flags:
        # The flag was the first to occur (before the equivalent) in the cmd, and thus is already
        # present in firstRepdFlag. So, continue, because that repeated flag would already have
        # been reported in parseArgs(...).
        if len(flags[flag][1]) > 1:
            repeated = True
        # Curr flag has occured before its equivalent, and has occured atleast once in the cmd.
        if flag in firstRepdFlag:
            continue
        # Flag does not have any equivalent flag
        if flag not in equivFlags:
            continue
        # The curr flag's equivalent flag is present in the flags dict.
        if equivFlags[flag] in flags:
            # If the curr flag isn't in firstRepdFlag and its equivalent flag is also not in
            # firstRepdFlag, add the curr flag to firstRepdFlag (meaning it's first being
            # encountered now, and its equivalent wasn't encountered before that).
            if flag not in firstRepdFlag and equivFlags[flag] not in firstRepdFlag:
                firstRepdFlag.append(flag)
                continue
            reportArgErr(
                "flag",
                f"Repeated equivalent flag of -{equivFlags[flag]}",
                flags[flag][1],
                "-" + flag,
            )
            repeated = True

    return repeated


def main():
    args, opts, flags = parseArgs(VALID_OPTS, VALID_FLAGS)
    repeated = areEquivOptFlagRepd(opts, flags, EQUIV_OPTS, EQUIV_FLAGS)

    # Check if there are any integer values in the options and flags dictionary, which indicate
    # argument errors
    for i in tuple(opts.values()) + tuple(flags.values()):
        if isinstance(i[0], int):
            sys.exit(ERR_ARG_ERRS)

    # Repeated options/flags
    if repeated:
        sys.exit(ERR_ARG_ERRS)

    if "h" in flags or "-help" in flags:
        prnHelp()
        sys.exit(ALL_GOOD)

    if "v" in flags or "-version" in flags:
        prnVer()
        sys.exit(ALL_GOOD)

    # Check if the no of args is valid
    if len(args) == 0:
        repErr("fatal", f"Expected {NO_OF_VALID_ARGS} argument(s)")
        repErr("info", "Pass -h/--help for help")
        sys.exit(ERR_TOO_FEW_ARGS)
    if len(args) >= 2:
        repErr("fatal", f"Only {NO_OF_VALID_ARGS} argument(s) accepted")
        sys.exit(ERR_TOO_MANY_ARGS)

    fl = args[sorted(args)[0]]
    icon = None
    jobs = None
    quiet = False
    optimise = False
    outputDir = os.path.join(os.getcwd(), "build")
    docStrs = True
    asserts = True
    warnings = True
    extraFls = True

    # Fl nm
    if not os.path.isfile(fl):
        repErr("fatal", f'Cannot find source file: "{fl}"')
        sys.exit(ERR_SRC_FL_404)

    # Icon fl
    if (tmp := ("i" in opts)) or "-icon" in opts:
        icon = opts["i" if tmp else "-icon"][0]
        if not os.path.isfile(icon):
            repErr("fatal", f'Cannot find icon file: "{icon}"')

    # Number of jobs
    if (tmp := ("j" in opts)) or "-jobs" in opts:
        jobs = opts["j" if tmp else "-jobs"][0]
        try:
            int(jobs)
        except ValueError:
            repErr("fatal", f'Invalid number of jobs: "{jobs}"')
            sys.exit(ERR_ARG_ERRS)

    # Quiets
    if (tmp := ("q" in flags)) or "-quiet" in flags:
        quiet = True

    # C compiler optimisations
    if (tmp := ("od" in flags)) or "-optimise" in flags:
        optimise = True

    # O/p dir
    if (tmp := ("od" in opts)) or "-output-dir" in opts:
        outputDir = opts["od" if tmp else "-output-dir"][0]

    # Rm docstrs
    if (tmp := ("ndoc" in flags)) or "-no-docstrings" in flags:
        docStrs = False

    # No asserts
    if (tmp := ("nass" in flags)) or "-no-asserts" in flags:
        asserts = False

    # No warnings
    if (tmp := ("nwarn" in flags)) or "-no-warnings" in flags:
        warnings = False

    # Rm build fls
    if (tmp := ("nextrafl" in flags)) or "-no-extra-files" in flags:
        extraFls = False

    if pf.system() == "Windows":
        execNm = "python.exe"
        iconOpt = "--windows-icon-from-ico"
    elif pf.system() == "Linux":
        execNm = "python3"
        iconOpt = "--linux-icon"
    else:
        raise HahaHehe("Ahhhh. That is NOT something I recognise!")

    cmd = [
        execNm,
        "-OO",
        "-W",
        "error",
        "-m",
        "nuitka",
        "--python-flag=no_docstrings" if not docStrs else "",
        "--python-flag=-O" if not asserts else "",
        "--python-flag=no_warnings" if not warnings else "",
        "--standalone",
        "--follow-imports",
        f"--jobs={jobs}" if jobs is not None else "",
        "--noinclude-pytest-mode=nofollow" if optimise else "",
        "--lto=yes" if optimise else "",
        "--quiet" if quiet else "",
        "--remove-output" if not extraFls else "",
        "--no-pyi-file" if not extraFls else "",
        f"--output-dir={outputDir}",
        f"{iconOpt}={pl.Path(icon).resolve()}" if icon is not None else "",
        str(pl.Path(fl).resolve()),
    ]

    sp.run([i for i in cmd if i])

    # Run executable option --run provided
    if "-run" in flags:
        # sp.run([
        #     os.path.join(
        #         outputDir, os.path.splitext(fl)[0] + ".dist", os.path.splitext(fl)[0] + ".exe"
        #     )],
        #     shell=True
        # )
        raise NotImplementedError("Not implemented yet...")


__version__ = 0.1

ALL_GOOD = 0
ERR_TOO_FEW_ARGS = 1
ERR_TOO_MANY_ARGS = 2
ERR_SRC_FL_404 = 3
ERR_ARG_ERRS = 4

ERR_OPT_NO_EQ = 101
ERR_INV_ELEM = 102
ERR_REPEATED_FLAG = 103
ERR_REPEATED_OPT = 104

# TODO: Change the number of valid args as the prog grows
NO_OF_VALID_ARGS = 1
VALID_OPTS = ("i", "j", "od", "-icon", "-jobs", "-output-dir")
VALID_FLAGS = (
    "h",
    "v",
    "q",
    "op",
    "od",
    "ndoc",
    "nass",
    "nwarn",
    "nextrafl",
    "-help",
    "-version",
    "-quiet",
    "-optimise",
    "no-docstrings",
    "-no-asserts",
    "-no-warnings",
    "-no-extra-files",
    "-run",
)
# NOTE: Make sure you have only two equivalent options and flags for a specific function
EQUIV_OPTS = {"i": "-icon", "od": "-output-dir", "-icon": "i", "-output-dir": "od"}
EQUIV_FLAGS = {
    "h": "-help",
    "v": "-version",
    "q": "-quiet",
    "op": "-optimise",
    "ndoc": "-no-docstrings",
    "nass": "-no-asserts",
    "nwarn": "-no-warnings",
    "nextrafl": "-no-extra-files",
    "-help": "h",
    "-version": "v",
    "-quiet": "q",
    "-optimise": "op",
    "-no-docstrings": "ndoc",
    "-no-asserts": "nass",
    "-no-warnings": "nwarn",
    "-no-extra-files": "nextrafl",
}

PRN_HELP_STR = [
    "<comp> [flag ...] [opt=val ...] fl [...]",
    "",
    "ARGUMENTS",
    "fl",
    "    The main program (i.e. the program to be compiled)",
    "",
    "OPTIONS",
    "-i / --icon",
    "    The icon for the output executable",
    "-j / --jobs",
    "    The number of jobs to run in parallel",
    "-od / --output-dir",
    "    The directory to compile the program to",
    "",
    "FLAGS",
    "-h / --help",
    "    Display the help message",
    "-nass / --no-asserts",
    "    No assertions",
    "-ndoc / --no-docstrings",
    "    Remove docstrings",
    "-nextrafl / --no-extra-files",
    "    Remove the .pyi file and prog.build directory",
    "-nwarn / --no-warnings",
    "    Suppress warnings",
    "-op / --optimise",
    "    Optimise the C compiler output (--lto=yes and --noinclude-pytest-mode=nofollow)",
    "-q / --quiet",
    "    Silences Nuitka console output",
    "-v / --version",
    "    Display the version of the build program",
    "",
    "NOTE: Activate the Python virtual environment (if any) to use the correct interpreter",
]

main()
