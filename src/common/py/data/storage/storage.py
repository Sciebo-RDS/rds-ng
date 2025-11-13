import abc
import typing

EntityType = typing.TypeVar("EntityType")  # pylint: disable=invalid-name
EntityKeyType = typing.TypeVar("EntityKeyType")  # pylint: disable=invalid-name


class Storage(typing.Generic[EntityType, EntityKeyType], abc.ABC):
    """
    Defines a general storage interface for basic CRUD operations.
    """

    @abc.abstractmethod
    def next_id(self) -> EntityKeyType:
        """
        Gets the next ID to use for a new entity.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def add(self, entity: EntityType) -> None:
        """
        Adds a new entity or updates an existing one.

        Raises:
              StorageException: If the entity couldn't be added.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, entity: EntityType) -> None:
        """
        Removes an entity.

        Raises:
              StorageException: If the entity couldn't be removed.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, key: EntityKeyType) -> EntityType | None:
        """
        Retrieves the entity identified by the given key.

        Returns:
            The found entity, or ``None`` if no entity with the given key exists.

        Raises:
            StorageException: If the entity couldn't be fetched (not due to a missing key).
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def list(self) -> typing.List[EntityType]:
        """
        Retrieves all stored entities.

        Returns:
            A list of all entitites.

        Raises:
            StorageException: If the entities couldn't be listed.
        """
        raise NotImplementedError()
