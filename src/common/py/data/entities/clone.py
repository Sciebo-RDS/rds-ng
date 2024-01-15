import dataclasses
import typing

EntityType = typing.TypeVar("EntityType")  # pylint: disable=invalid-name


def clone_entity(entity: typing.Generic[EntityType], **changes) -> EntityType:
    """
    Creates a copy (clone) of the given entity, applying optional field changes.

    Args:
        entity: The entity to clone.
        **changes: Any field changes to apply.

    Returns:
        The cloned entity.
    """
    return typing.cast(EntityType, dataclasses.replace(entity, **changes))
