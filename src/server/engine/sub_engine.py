import abc


class SubEngine(abc.ABC):
    """
    Defines the base for sub-engines.
    """

    def process(self) -> None:
        pass
