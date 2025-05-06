import typing


def human_readable_file_size(size: int, suffix="B") -> str:
    """
    Converts a file size to a human-readable string.
    
    Args:
        size: The file size to convert.
        suffix: Default suffix.

    Returns:
        The human-readable file size.
    """
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(size) < 1024.0:
            return f"{size:3.2f} {unit}{suffix}"
        size /= 1024.0
    
    return f"{size:.2f} Y{suffix}"


def format_elapsed_time(elapsed: float) -> str:
    """
    Converts a number of seconds into a readable string.
    
    Args:
        elapsed: The elapsed time in seconds.

    Returns:
        The string representation.
    """
    m, s = divmod(elapsed, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 60)
    
    tokens: typing.List[str] = []
    
    def add_token(val: float, name: str) -> None:
        if val >= 1.0:
            tokens.append(f"{val:.0f}{name}")
            
    add_token(d, "d")
    add_token(h, "h")
    add_token(m, "m")
    add_token(s, "s")
    
    return " ".join(tokens)


def ensure_starts_with(s: str, start: str) -> str:
    """
    Ensures that a string starts with a given string.
    
    Args:
        s: The string.
        start: The start to ensure.

    Returns:
        The new string.
    """
    if not s.startswith(start):
        s = start + s
    return s
