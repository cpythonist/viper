import os

import logging as lg
import typing as ty

import utils.consts as uconst


class CustomLogger(lg.getLoggerClass()):
    """
    Custom logger extending the logging.Logger class to add separate functionality to the FATAL log
    level.
    """

    def __init__(self, name: str, level: int | str = lg.NOTSET) -> None:
        super().__init__(name, level)
        lg.addLevelName(uconst.LOG_FATAL_VAL, "FATAL")

    def info(self, msg: str, sl: int = 3, *args: ty.Any, **kwargs: ty.Any) -> None:
        if self.isEnabledFor(lg.INFO):
            self._log(lg.INFO, msg, args, **kwargs, stacklevel=sl)

    def debug(self, msg: str, sl: int = 3, *args: ty.Any, **kwargs: ty.Any) -> None:
        if self.isEnabledFor(lg.DEBUG):
            self._log(lg.DEBUG, msg, args, **kwargs, stacklevel=sl)

    def warning(self, msg: str, sl: int = 3, *args: ty.Any, **kwargs: ty.Any) -> None:
        if self.isEnabledFor(lg.WARNING):
            self._log(lg.WARNING, msg, args, **kwargs, stacklevel=sl)

    def error(self, msg: str, sl: int = 3, *args: ty.Any, **kwargs: ty.Any) -> None:
        if self.isEnabledFor(lg.ERROR):
            self._log(lg.ERROR, msg, args, **kwargs, stacklevel=sl)

    def critical(self, msg: str, sl: int = 3, *args: ty.Any, **kwargs: ty.Any) -> None:
        if self.isEnabledFor(lg.CRITICAL):
            self._log(lg.CRITICAL, msg, args, **kwargs, stacklevel=sl)

    def fatal(self, msg: str, sl: int = 3, *args: ty.Any, **kwargs: ty.Any) -> None:
        if self.isEnabledFor(uconst.LOG_FATAL_VAL):
            self._log(uconst.LOG_FATAL_VAL, msg, args, **kwargs, stacklevel=sl)


class ConLogFormatter(lg.Formatter):
    """
    To apply custom formatting to the console messages.
    """

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: ty.Literal["%"] | ty.Literal["{"] | ty.Literal["$"] = "%",
        validate: bool = True,
        *,
        defaults: ty.Mapping[str, ty.Any] | None = None,
    ) -> None:
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record: lg.LogRecord) -> str:
        record.msg = record.getMessage().strip("\n")
        record.levelname2 = uconst.LOG_LVLS[record.levelno]
        return super().format(record)


def initLgrs() -> tuple[lg.Logger, lg.Logger, lg.Logger, lg.Logger] | None:
    """
    Initialise and set up the loggers.
    > return: A tuple of the initialised loggers
    """
    try:
        os.makedirs(uconst.LOG_DIR, exist_ok=True)
    except PermissionError:
        return None
    lg.setLoggerClass(CustomLogger)
    lg.captureWarnings(True)

    redBoldConLgrStr = f"{uconst.ANSI_BOLD_RED}%(levelname2)s:{uconst.ANSI_RESET} %(message)s"
    yellowBoldConLgrStr = f"{uconst.ANSI_BOLD_YELLOW}%(levelname2)s:{uconst.ANSI_RESET} %(message)s"
    boldConLgrStr = f"{uconst.ANSI_BOLD}%(levelname2)s:{uconst.ANSI_RESET} %(message)s"
    flLgrStr = (
        "[%(asctime)s.%(msecs)03d]\n"
        "%(levelname)s:%(module)s:%(funcName)s\n"
        "%(message)s\n"
        "----------"
    )
    flLgrDtStr = "%z/%d-%m-%Y/%H:%M:%S"

    # Create the loggers
    lgr = lg.getLogger(__name__)
    redBoldConLgr = lgr.getChild("CON_RED_BOLD")
    yellowBoldConLgr = lgr.getChild("CON_YELLOW_BOLD")
    boldConLgr = lgr.getChild("CON_BOLD")
    flLgr = lgr.getChild("FL")

    # Formatters
    redBoldConLgrFormatter = ConLogFormatter(fmt=redBoldConLgrStr)
    yellowBoldConLgrFormatter = ConLogFormatter(fmt=yellowBoldConLgrStr)
    boldConLgrFormatter = ConLogFormatter(fmt=boldConLgrStr)
    flLgrFormatter = lg.Formatter(fmt=flLgrStr, datefmt=flLgrDtStr)

    # Handlers
    redBoldConHdler = lg.StreamHandler()
    yellowBoldConHdler = lg.StreamHandler()
    boldConHdler = lg.StreamHandler()
    flHdler = lg.FileHandler(os.path.join(uconst.LOG_DIR, "viper.log"), "a", encoding="utf-8")

    # Apply the formatters
    redBoldConHdler.setFormatter(redBoldConLgrFormatter)
    yellowBoldConHdler.setFormatter(yellowBoldConLgrFormatter)
    boldConHdler.setFormatter(boldConLgrFormatter)
    flHdler.setFormatter(flLgrFormatter)

    # TODO: May need to change levels in release build
    # Set the level of each logger, will ya?
    redBoldConLgr.setLevel(lg.DEBUG)
    yellowBoldConLgr.setLevel(lg.DEBUG)
    boldConLgr.setLevel(lg.DEBUG)
    flLgr.setLevel(lg.WARN)

    # Add the handlers to the loggers, please, m'boy
    redBoldConLgr.addHandler(redBoldConHdler)
    yellowBoldConLgr.addHandler(yellowBoldConHdler)
    boldConLgr.addHandler(boldConHdler)
    flLgr.addHandler(flHdler)

    return redBoldConLgr, yellowBoldConLgr, boldConLgr, flLgr
