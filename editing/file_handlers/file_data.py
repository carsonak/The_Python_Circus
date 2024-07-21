#!/usr/bin/python3
"""Module for python_files_tracker."""

import ast
from contextlib import suppress
from enum import Enum
import os
from types import MappingProxyType

import regex


class Interpretor(Enum):
    """Interpretor and their extensions."""
    AWK = frozenset({".awk"})
    BASH = frozenset({".bash", ".bashrc"})
    PYTHON = frozenset({".py", ".pyi", ".pyc"})
    RUBY = frozenset({".rb"})
    SH = frozenset({".sh"})
    MAKE = frozenset({""})


EXTENSIONS: MappingProxyType[str, Interpretor] = MappingProxyType({
    ext: inter for inter in Interpretor for ext in inter.value
})


class FileData:
    """A container for Python script data."""

    def __init__(
        self, file_path: str | bytes | os.PathLike,
        content: str | bytes | None = None, tree: ast.AST | None = None,
    ) -> None:
        """Initialise a container for Python script data.

        Args:
            file_path: path to a file.
            content: contents of the file as a string or byte array.
            tree: abstract syntax trees for python scripts.
        """
        self.filepath = file_path  # type: ignore
        self.content = content
        self.tree = tree

    @property
    def filepath(self) -> str:
        """Path to the file."""
        return self.__filepath

    @filepath.setter
    def filepath(self, path: str | bytes | os.PathLike) -> None:
        """Set filepath."""
        self.__filepath = str(os.fspath(path))
        if os.path.isfile(self.filepath) is False:
            raise ValueError("filepath does not point to a file.")

        self.__fileinterpretor = get_file_interpretor(self.__filepath)

    @property
    def file_interpretor(self) -> Interpretor | None:
        """The type of the file."""
        return self.__fileinterpretor

    @property
    def content(self) -> str | bytes | None:
        """Contents of a python script."""
        return self.__content

    @content.setter
    def content(self, val: str | bytes | None) -> None:
        """Initialise content.

        Args:
            val: a str or bytes object representing the content of
                a python script.

        Raises:
            TypeError: val is not an instance of str or bytes.
        """
        self.__content = None
        if val is None:
            return

        if not isinstance(val, (str, bytes)):
            raise TypeError(
                f"object must be an instance of {str}, {bytes} or None")

        self.__content = val

    @property
    def tree(self) -> ast.AST | None:
        """Abstract Syntax Tree of a Python script or None."""
        return self.__tree

    @tree.setter
    def tree(self, val: ast.AST | None) -> None:
        """Initialise tree.

        Args:
            val: the abstract syntax tree of a Python script or None.

        Raises:
            TypeError: val is not an instance of ast.AST or None.
        """
        self.__tree = None
        if val is None:
            return

        if not isinstance(val, ast.AST):
            raise TypeError(
                f"object must be an instance of {ast.AST} or {None}")

        self.__tree = val

    def __str__(self) -> str:
        """Return a string with details of this instance."""
        return (
            f"{self.__class__.__name__}("
            f"filepath={self.filepath}, "
            f"content=<{type(self.content).__name__} object at "
            f"{hex(id(self.content))}>, "
            f"tree={self.tree})"
        )


def get_file_interpretor(
        file_path: str | bytes | os.PathLike) -> Interpretor | None:
    """Determine file's interpretor from the file's extension or shebang.

    Args:
        filepath:

    Returns:
        An option from the Enum Interpretor or None.
    """
    filename: str = str(os.fspath(file_path))
    file_type: str = os.path.splitext(filename)[1]
    first_line: str = ""
    if not file_type:
        with suppress(PermissionError), open(filename, "r") as f:
            first_line = f.readline().strip()

    shebang_match: regex.Match | None = regex.match(
        r"""
        ^\#!
        (?P<dir_path> (?> \/+ (?: (?<!-) [\w.-]+ \/+ )* ) )
        (?P<exe> (?> (?<!-) [\w.-]+ ) )
        (?P<opts> (?> \ +(?:-[\w-]+(?:\ +|=)? ) ) )*$
        """,
        first_line,
        regex.VERBOSE,
    )
    if shebang_match is None:
        shebang_match = regex.match(
            r"""
            ^\#!
            (?P<dir_path> (?> \/+ (?: (?<!-) [\w.-]+ \/+ )* ) )
            env\ +
            (?P<opts> (?> (?:-[\w-]+=?)\ * ) )*
            (?P<exe> (?> (?<!-) [\w.-]+ ) )
            """,
            first_line,
            regex.VERBOSE
        )

    if shebang_match is not None:
        file_type = shebang_match.group("exe").strip()

    if file_type.startswith("."):
        for ext, inter in EXTENSIONS.items():
            if file_type == ext:
                return inter
    else:
        for inter in Interpretor:
            if file_type.startswith(inter.name.lower()):
                return inter

    return None
