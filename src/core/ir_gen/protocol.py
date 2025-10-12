import typing as ty


class IRGenProtocol(ty.Protocol):
    instrArr: list[tuple[str, str, str, str]]
