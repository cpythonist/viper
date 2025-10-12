#
# The Viper source code
#
# Filename: src\\main.py
# Description: The main program
#
# Return codes to the main calling program:
# -1: Unknown error
#  0: Success
# +1: Cannot perform required imports
#

# TODO: sys.setrecursionlimit(...) call add panna marandudatha
# This PC can go beyond int(1e8), but I think the program might consume more memory than desirable.
# So, bump up the recursion limit to 1e6 or 2e6.

MAIN_ERR_UNKNOWN = -1
MAIN_ALL_GOOD = 0
MAIN_ERR_CANT_IMPORT = 1
MAIN_ERR_FL_404 = 2
MAIN_ERR_PERM = 3
MAIN_ERR_INV_ARG = 4
MAIN_ERR_NOT_TXT = 5


try:
    import sys

    import logging as lg

    import core.lexer as lex
    import core.parser.engine as par
    import core.semalyser.engine as sem
    import core.token_ as tok

    import utils.consts as uconst
    import utils.gen as ugen

    # TODO: Remove in the release build
    import utils.dev_and_debug as udev

    import core.parser.pruner as prune

    TT = tok.TokenTypes
    VER = "1.0"

    # NOTE: Change this when you're adding more arguments!
    NO_OF_VALID_ARGS = 1
    # NOTE: Change this to probably logging.INFO in the release build!
    FL_LOG_LVL = lg.DEBUG

except KeyboardInterrupt:
    print(f"Interrupted by your dumbass")
    sys.exit(MAIN_ALL_GOOD)

except ImportError as e:
    print(f"\033[1m\033[91mF\033[0m: Could not import required modules/packages;\n{str(e)}")
    sys.exit(MAIN_ERR_CANT_IMPORT)

except Exception as e:
    # TODO: Remove in final build (the import statement, not the print statement, you idiot)
    import traceback

    traceback.print_exc()
    print(
        f"FATAL: Could not initialise the program; encountered a/an {e.__class__.__name__} ({str(e)})"
    )
    sys.exit(MAIN_ERR_UNKNOWN)


def prnHelp() -> None:
    """
    Print the help message for the program.
    """
    print("""Work in progress, buddy...""")


def parseArgs() -> tuple[list[str], dict[str, str], list[str]]:
    """
    Parse the arguments passed to the program.
    > return: A tuple of a list of strings, a dictionary of string keys and string values, and a
              list of strings, for arguments, options and flags
    """
    args: list[str]
    opts: dict[str, str]
    flags: list[str]

    args = []
    opts = {}
    flags = []
    exitAfter = False
    modSysArgv = sys.argv[1:]
    lenModSysArgv = len(modSysArgv)
    parseOpts = True
    idx = 0
    err = uconst.ERR_SUCCESS

    while idx < lenModSysArgv:
        elem = modSysArgv[idx]

        # -- marks the end of parsing options
        if elem == "--":
            parseOpts = False
            idx += 1
            continue

        if parseOpts and elem[0] == "-":
            if elem == "-h" or elem == "--help":
                if lenModSysArgv > 1:
                    ugen.info(
                        "Other data passed to the program is ignored as the help option is passed"
                    )
                prnHelp()
                exitAfter = True
            elif elem == "-v" or elem == "--version":
                print(VER)
                exitAfter = True
            else:
                print(f"{uconst.ANSI_BOLD_RED}ERR:{uconst.ANSI_RESET} Unknown option/flag: {elem}")
                err = uconst.ERR_UNK_OPT_FLAG
        else:
            args.append(elem)

        idx += 1

    if len(args) < NO_OF_VALID_ARGS:
        print(f"{uconst.ANSI_BOLD_RED}ERR:{uconst.ANSI_RESET} Too few arguments")
        prnHelp()
        sys.exit(uconst.ERR_TOO_FEW_ARGS)
    if len(args) > NO_OF_VALID_ARGS:
        print(f"{uconst.ANSI_BOLD_RED}ERR:{uconst.ANSI_RESET} Too many arguments")
        prnHelp()
        sys.exit(uconst.ERR_TOO_MANY_ARGS)

    if err or exitAfter:
        sys.exit(err)

    return args, opts, flags


def main() -> None:
    """
    Main function.
    """
    # sys.set_int_max_str_digits(1000000000)

    args, opts, flags = parseArgs()

    srcFl = args[0]
    try:
        with open(srcFl, buffering=1) as f:
            src = f.read()
    except FileNotFoundError:
        ugen.error(f'File not found: "{srcFl}"')
        sys.exit(MAIN_ERR_FL_404)
    except PermissionError:
        ugen.error(f'Access is denied: "{srcFl}"')
        sys.exit(MAIN_ERR_PERM)
    except OSError:
        ugen.error(f'Invalid argument: "{srcFl}"')
        sys.exit(MAIN_ERR_INV_ARG)
    except UnicodeDecodeError:
        ugen.error(f'Does not appear to contain text: "{srcFl}"')
        sys.exit(MAIN_ERR_NOT_TXT)

    lexer = lex.Lexer()
    parser = par.Parser(src, lexer)
    tree = parser.parse()
    pruner = prune.ASTPruner(tree)
    pruner.prune()

    semChker = sem.SemanticAnalyser(parser, pruner, pruner.tree)
    semChker.analyseTree(pruner.tree, "module", None)

    print("PARSE_ERRS")
    for i in parser.parseErrs.errs:
        print(i.errStr, i.offendingTok)
    print("------")

    print("SEM_ERRS")
    for i in semChker.semErrs.errs:
        print(i.errStr, i.offendingNode)

    print(semChker.symTable)

    # udev.pprn(pruner.tree)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ugen.error("Interrupted by your dumbass")
    except Exception as e:
        ugen.fatal(e, -1)
