#!/usr/bin/python3
"""Module for python_files_tracker."""

import ast
from contextlib import suppress
import os
from typing import TypedDict

import regex


class FileBase(TypedDict):
    """Stores path to a file."""
    file: str | bytes | os.PathLike
    encoding: str
    file_type: str | None


class File(FileBase, total=False):
    """Container for a file's contents."""
    content: str | bytes
    tree: ast.AST


class FileData:
    """A container for Python scipt data."""

    def __init__(
        self, filepath: str | bytes | os.PathLike | None = None,
        content: str | bytes = "", tree: ast.AST | None = None,
    ):
        """Initialise a container for Python scipt data."""
        self.__file: File
        self.filename = filepath  # type: ignore
        self.content = content
        self.tree = tree

    @property
    def file(self) -> File:
        """A TypedDict with filename and and it's contents."""
        return self.__file

    @property
    def filename(self) -> str:
        """Path to the file."""
        return self.__filename

    @filename.setter
    def filename(self, path: str | bytes | os.PathLike) -> None:
        """Set filename."""
        self.__filename = str(os.fspath(path))
        if os.path.isfile(self.filename) is False:
            raise ValueError("path does not point to a file.")

        self.__file = File(
            file=self.__filename, encoding="utf-8",
            file_type=self.get_filetype(),
        )

    @property
    def content(self) -> str | bytes:
        """Contents of a python script."""
        return self.__content

    @content.setter
    def content(self, val: str | bytes) -> None:
        """Initialise content.

        Args:
            val: a str or bytes object representing the content of
                a python script.

        Raises:
            TypeError: val is not an instance of str or bytes.
        """
        if not isinstance(val, (str | bytes)):
            raise TypeError(f"object must be an instance of {str} or {bytes}")

        self.__content = val
        self.__file["content"] = self.__content

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
        self.__file["tree"] = val

    def __str__(self) -> str:
        """Return a string with details of this instance."""
        return (
            f"{self.__class__.__name__}("
            f"filepath={self.filename}, "
            f"content=<{type(self.content).__name__} object at "
            f"{hex(id(self.content))}>, "
            f"tree={self.tree})"
        )

    def get_filetype(self) -> str | None:
        """Determine file type from extnsion or from the shebang.

        Returns:
            tuple[is_file: bool, file_type: str]
        """
        file_type: str = os.path.splitext(self.__filename)[1]
        first_line: str = ""
        if not file_type:
            with suppress(PermissionError), open(self.__filename, "r") as f:
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

        return file_type
