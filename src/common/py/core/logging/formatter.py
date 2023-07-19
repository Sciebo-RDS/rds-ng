import logging
import typing


class Formatter(logging.Formatter):
    """
    Customized log formatter.
    
    This formatter mainly colorizes log records for better readability.
    """
    _colors = {
        "time": 7,
        "scope": 28,
        "levels": {
            logging.DEBUG: 241,
            logging.INFO: 27,
            logging.WARNING: 214,
            logging.ERROR: 160,
        },
        "params": {
            "name": 93,
            "value": 126,
        },
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Colorizes the various portions of a log record.
        
        Returns:
            The formatted text.
        """
        scope = self._get_scope(record)
        params = [f"{self._color_wrap(k, self._colors['params']['name'], italic=True)}={self._color_wrap(str(v), self._colors['params']['value'], italic=True)}" for k, v in self._get_extra_params(record).items()]
        tokens = [
            self._color_wrap(self.formatTime(record, "%Y-%m-%d %H:%M:%S"), self._colors["time"]),
            " [",
            self._color_wrap(record.levelname, self._get_level_color(record.levelno), bold=True),
            "|" + self._color_wrap(scope, self._colors["scope"]) if scope != "" else "",
            "] ",
            record.msg,
            f" ({'; '.join(params)})" if len(params) > 0 else "",
        ]
        return "".join(tokens)
    
    def _color_wrap(self, text: str, fg_color: int = 0, bg_color: int | None = None, bold: bool = False, italic: bool = False) -> str:
        s: str = f"\x1b[38;5;{fg_color}m"
        if bold:
            s += "\x1b[1m"
        if italic:
            s += "\x1b[3m"
        if bg_color is not None:
            s += f"\x1b[48;5;{bg_color}m"
        return s + text + "\x1b[0m"
    
    def _get_level_color(self, level: int) -> int:
        return self._colors["levels"][level] if level in self._colors["levels"] else 0
    
    def _get_scope(self, record: logging.LogRecord) -> str:
        scope = ""
        if "scope" in record.__dict__ and record.scope is not None:
            scope = record.scope.lower()
        return scope

    def _get_extra_params(self, record: logging.LogRecord) -> typing.Dict[str, typing.Any]:
        params: typing.Dict[str, typing.Any] = {}
        if "extra_params" in record.__dict__ and record.extra_params is not None:
            params = record.extra_params
        return params
