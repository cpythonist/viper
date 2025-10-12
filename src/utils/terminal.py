import sys

import platform as pf

if pf.system() == "Windows":
    from msvcrt import getch, kbhit

else:
    from termios import TCSADRAIN, tcgetattr, tcsetattr
    from select import select
    from tty import setraw
    from sys import stdin

    def getch() -> bytes:
        fd = stdin.fileno()
        oldSetts = tcgetattr(fd)

        try:
            setraw(fd)

            return stdin.read(1).encode()
        finally:
            tcsetattr(fd, TCSADRAIN, oldSetts)

    def kbhit() -> bool:
        return bool(select([stdin], [], [], 0)[0])


# def ansiOKOldOnlyWin32() -> bool:
#     """
#     Checks if the terminal supports ANSI sequences.
#     Thanks to Stack Overflow!
#     > return: True if the terminal supports ANSI sequences, False otherwise.
#     """
#     kernel32 = ct.windll.kernel32
#     kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
#
#     while ms.kbhit():
#         ms.getch()
#
#     sys.stdout.write("\x1b[6n\b\b\b\b")
#     sys.stdout.flush()
#     sys.stdin.flush()
#
#     if ms.kbhit():
#         if ord(ms.getch()) == 27 and ms.kbhit():
#             if ms.getch() == b"[":
#                 while ms.kbhit():
#                     ms.getch()
#                 return sys.stdout.isatty()
#
#     return False


def ansiOK() -> bool:
    """
    Checks if the terminal supports ANSI sequences.
    Thanks to Stack Overflow!
    > return: True if the terminal supports ANSI sequences, False otherwise.
    """
    while kbhit():
        getch()

    sys.stdout.write("\x1b[6n")
    sys.stdout.flush()

    sys.stdin.flush()
    if kbhit():
        if ord(getch()) == 27 and kbhit():
            if getch() == b"[":
                while kbhit():
                    getch()

                return sys.stdout.isatty()

    return False
