import logging
import typing


class Formatter(logging.Formatter):
    """ Handles unified formatting of log messages. """
    # TODO: Optimize -> Prepare formats for all levels, store formatters
    
    def format(self, record: logging.LogRecord) -> str:
        fg_color: int = self._get_level_color(record.levelno)
        fmt: str = f"{self._color_wrap('$asctime', 7)} {self._color_wrap('[$levelname', fg_color, bold=True)}{self._get_scope(record)}{self._color_wrap(']', fg_color, bold=True)} $message"
        args: str = self._get_extra_params(record)
        if args != "":
            fmt += f" ({args})"
        return logging.Formatter(fmt, style="$", datefmt="%Y-%m-%d %H:%M:%S").format(record)
    
    def _get_level_color(self, level: int):
        colors: typing.Mapping[int, int] = {
            logging.DEBUG: 61,
            logging.INFO: 27,
            logging.WARNING: 214,
            logging.ERROR: 160,
        }
        return colors[level] if level in colors else 0
    
    def _color_wrap(self, text: str, fg_color: int = 0, bg_color: int|None = None, bold: bool = False) -> str:
        s: str = f"\x1b[38;5;{fg_color}m"
        if bold:
            s += "\x1b[1m"
        if bg_color is not None:
            s += f"\x1b[48;5;{bg_color}m"
        s += text + "\x1b[0m"
        return s
    
    def _get_scope(self, record: logging.LogRecord) -> str:
        scope: str = ""
        if "scope" in record.__dict__ and record.scope is not None:
            scope = "|" + self._color_wrap(record.scope.lower(), 34, bold=True)
        return scope

    def _get_extra_params(self, record: logging.LogRecord) -> str:
        s: str = ""
        if "extra_params" in record.__dict__ and record.extra_params is not None:
            args: typing.List[str] = []
            for k, v in record.extra_params.items():
                args.append(f"{self._color_wrap(k, 88)}={self._color_wrap(str(v), 208)}")
            s = "; ".join(args)
        return s
