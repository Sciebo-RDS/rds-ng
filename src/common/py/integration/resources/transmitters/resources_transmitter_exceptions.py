class ResourcesTransmitterError(RuntimeError):
    """
    Basic transmitter error.
    """

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
