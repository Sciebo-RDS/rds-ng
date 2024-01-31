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
