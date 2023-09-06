import typing

ItemType = typing.TypeVar("ItemType")  # pylint: disable=invalid-name


class ItemsCatalog(typing.Generic[ItemType]):
    """
    Generic catalog to keep track of "registered" items (where the definition of "item" is completely context dependant).

    This is a globally accessible list of these items, associated with their respective names.
    """
    _items: typing.Dict[str, ItemType] = {}
    
    @staticmethod
    def define():
        """
        A decorator to define a new item catalog.
        
        Notes:
            This decorator must always be used for new item catalogs; otherwise, data corruption might occur.
        """
        def decorator(cls):
            setattr(cls, "_items", {})
            return cls
        
        return decorator
    
    @classmethod
    def register_item(cls, name: str, item: ItemType) -> None:
        """
        Registers a new item.

        Args:
            name: The item name.
            item: The item.
        """
        if name in cls._items:
            if cls._items[name] != item:
                raise RuntimeError(f"An item with the name '{name}' has already been registered to a different item")
        else:
            cls._items[name] = item
    
    @classmethod
    def find_item(cls, name: str) -> ItemType | None:
        """
        Finds the item associated with the given ``name``.

        Args:
            name: The item name.

        Returns:
            The associated item, if any.
        """
        return cls._items[name] if name in cls._items else None

    @classmethod
    def items(cls) -> typing.Tuple[str, ItemType]:
        """
        Generator to iterate over all registered items.
        
        Returns:
            Tuple consisting of the item name and the item itself.
        """
        for name, item in cls._items.items():
            yield name, item
