from typing import Protocol


class Verifier(Protocol):
    """
    Defines the general interface for data verifiers.
    """

    def verify_create(self) -> None:
        """
        Verifies a new entity. In case of invalid data, an error is thrown.

        Raises:
            VerificationException: In case of any errors in the entity data.
        """
        ...

    def verify_update(self) -> None:
        """
        Verifies an updated entity. In case of invalid data, an error is thrown.

        Raises:
            VerificationException: In case of any errors in the entity data.
        """
        ...

    def verify_delete(self) -> None:
        """
        Verifies the deletion of an entity. In case of invalid data, an error is thrown.

        Raises:
            VerificationException: In case of any errors in the entity data.
        """
        ...
