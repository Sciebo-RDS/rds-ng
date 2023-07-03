import abc
import typing


class Aspects(abc.ABC):
    def create_object(self, create_type: type, target_type: type, *args, **kwargs) -> typing.Any:
        obj = create_type(*args, **kwargs)
        if not isinstance(obj, target_type):
            raise RuntimeError(f"Tried to create a {target_type}, but got type {type(obj)}")
        
        return obj
