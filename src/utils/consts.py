import os
import sys

import logging as lg

import utils.loggers as ulog
import utils.terminal as uterm

EMP_JOIN = "".join
QUOTE_CHRS = {"'", '"'}
ESC_CHAR_MAP = {
    "\\": "\\\\",
    "'": "\\'",
    '"': '\\"',
    "\n": "\\n",
    "\r": "\\r",
    "\t": "\\t",
}

LOG_FATAL_VAL = 60
LOG_LVLS = {
    lg.DEBUG: "D",
    lg.INFO: "I",
    lg.WARNING: "W",
    lg.ERROR: "E",
    lg.CRITICAL: "C",
    LOG_FATAL_VAL: "F",
}

# Important directories
SRC_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(SRC_DIR, "logs")

# Colour codes
ANSI = uterm.ansiOK()
ANSI_BOLD = "\033[1m" if ANSI else ""
ANSI_BLINK = "\033[5m" if ANSI else ""
ANSI_BLUE = "\033[94m" if ANSI else ""
ANSI_CLS = "\033[H\033[J" if ANSI else ""
ANSI_CYAN = "\033[96m" if ANSI else ""
ANSI_GREEN = "\033[92m" if ANSI else ""
ANSI_HEADER = "\033[95m" if ANSI else ""
ANSI_RED = "\033[91m" if ANSI else ""
ANSI_RESET = "\033[0m" if ANSI else ""
ANSI_UNDERLINE = "\033[4m" if ANSI else ""
ANSI_YELLOW = "\033[93m" if ANSI else ""
ANSI_BOLD_RED = ANSI_BOLD + ANSI_RED
ANSI_BOLD_YELLOW = ANSI_BOLD + ANSI_YELLOW

# Error codes
ERR_SUCCESS = 0
ERR_TOO_FEW_ARGS = 1
ERR_TOO_MANY_ARGS = 2
ERR_EXP_VAL_OPT = 3
ERR_UNK_OPT_FLAG = 4
ERR_SRC_FL_NOT_FOUND = 5
ERR_PERM_DENIED_SRC_FL = 6
ERR_NO_TXT_SRC_FL = 7

# Loggers
ALL_LGRS = ulog.initLgrs()
if ALL_LGRS is None:
    print("Unable to initialise at least one of the loggers; the program cannot start")
    sys.exit(-1)
RED_B_CON_LGR = ALL_LGRS[0]
YELLOW_B_CON_LGR = ALL_LGRS[1]
B_CON_LGR = ALL_LGRS[2]
FL_LGR = ALL_LGRS[3]

ALPHA_RANGE = tuple(range(65, 91)) + tuple(range(97, 123))
NUM_RANGE = tuple(range(48, 58))
