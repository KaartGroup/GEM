#!/usr/bin/env python
from enum import Enum
from typing import Dict, List
import re


class MapCSSParseException(Exception):
    """
    An exception that indicates something went wrong during parsing.
    """

    def __init__(self, message):
        """
        >>> exception = MapCSSParseException("Test message")
        >>> str(exception)
        'Test message'
        """
        super().__init__(message)


class MapCSSComment:
    """
    MapCSS comment"
    """

    def __init__(self, comment: str):
        self.comment = comment


class MapCSSSelector(Enum):
    """
    MapCSS selectors
    """

    NODE = "node"
    WAY = "way"
    RELATION = "relation"
    AREA = "area"
    LINE = "line"
    CANVAS = "canvas"
    ZOOM = "|"
    STAR = "*"


class MapCSSClass:
    """
    MapCSS class
    """

    def __init__(self, clazz: str):
        self.clazz = clazz


class MapCSSTest:
    """
    MapCSS tests
    """

    def __init__(self, test):
        self.test = test


class MapCSSDeclaration:
    """
    MapCSS declaration
    """

    def __init__(self, declaration: str):
        """
        Initialize a declaration and set vocabulary and action
        >>> declaration = MapCSSDeclaration("opacity:0.5")
        >>> declaration.vocabulary
        'opacity'
        >>> declaration.action
        '0.5'
        >>> declaration.separator
        ':'
        >>> declaration = MapCSSDeclaration("set .minor_road")
        >>> declaration.vocabulary
        'set'
        >>> declaration.action
        '.minor_road'
        >>> declaration.separator
        ' '
        """
        self.separator = ":"
        split = declaration.split(sep=self.separator, maxsplit=1)
        if len(split) == 1:
            self.separator = " "
            split = declaration.split(self.separator, maxsplit=1)
        self.vocabulary = split[0]
        self.action = split[1]


class MapCSSRule:
    """
    MapCSS Rule class
    """

    def __init__(
        self, selectors: List[MapCSSSelector], declarations: List[MapCSSDeclaration]
    ):
        self.selectors = selectors


class MapCSS:
    """
    MapCSS class
    """

    def __init__(self, original: str):
        self.original = original
        self.rules = []
        self.meta = {}

    @staticmethod
    def parse_meta(mapcss_string: str) -> dict:
        meta = re.findall(r"meta.*?\{(.*?)\}", mapcss_string)
        if isinstance(meta, list):
            raise MapCSSParseException("Too many meta information blocks")
        meta = str(meta)
        possible_declarations = meta.split(";")
        declarations = []
        for i in possible_declarations:
            declarations.append(MapCSSDeclaration(i))
        return MapCSS

    @staticmethod
    def parse_mapcss(mapcss_string: str):
        meta = parse_meta(mapcss_string)

        parsed_mapcss = MapCSS(mapcss_string)
        parsed_mapcss.meta = meta
        parsed_mapcss.rules = rules
        return parsed_mapcss


if __name__ == "__main__":
    import doctest

    doctest.testmod()
