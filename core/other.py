import ctypes
import msvcrt
import sys
import typing as ty

BOLD = "\033[1m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
UNDERLINE = "\033[4m"
YELLOW = "\033[93m"

def isDigit(char:str, starting:bool=False):
    return '0' <= char <= '9' if not starting else '1' <= char <= '9'

def isAlpha(char:str):
    return ord(char) in range(97, 123) or ord(char) in range(65, 91)

def isANSISupported():
    """
    Checks if the terminal supports ANSI sequences.
    If yes, return True, else False.

    Thanks to Stack Overflow for this code snippet!
    """
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    while msvcrt.kbhit():
        msvcrt.getch()
    sys.stdout.write("\x1b[6n\b\b\b\b")
    sys.stdout.flush()
    sys.stdin.flush()
    if msvcrt.kbhit():
        if ord(msvcrt.getch()) == 27 and msvcrt.kbhit():
            if msvcrt.getch() == b"[":
                while msvcrt.kbhit():
                    msvcrt.getch()
                return sys.stdout.isatty()
    return False

def isInt(string:str|int|float) -> bool:
    string = str(string)
    
    if string.startswith('0x'):
        string = string[2:]
    elif string.startswith('0'):
        string = string[1:]
    
    return all(char in '0123456789' for char in string)

def evaluate(val:ty.Any) -> bool:
    return bool(val)
