import typing


@typing.final
class Settings:
    @staticmethod
    def category(cat: str = ""):
        def decorator(cls):
            if cat != "":
                for key, value in cls.__dict__.items():
                    if not key.startswith("_") and isinstance(value, str):
                        setattr(cls, key, f"{cat}.{value}")
            
            return cls
        
        return decorator
