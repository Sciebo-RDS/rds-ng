from enum import Flag, auto


class ComponentRole(Flag):
    SERVER = auto()
    CLIENT = auto()
