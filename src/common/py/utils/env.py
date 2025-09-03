import os
import typing


def get_env_value(key: str, target_type: type) -> typing.Any:
    """
    Gets an environment variable from the system, converting it to a specific type.
    
    Args:
        key: The environment variable key.
        target_type: The target type.

    Returns:
        The converted value.
    """
    if key in os.environ:
        value = os.environ.get(key)
        if target_type == bool:
            if isinstance(value, str):
                value = value.casefold()
                return (
                        value == "1"
                        or value == "yes".casefold()
                        or value == "true".casefold()
                )
            if isinstance(value, int):
                return value >= 1
        
        return target_type(value)
    
    raise KeyError(f"The environment variable {key} doesn't exist")
