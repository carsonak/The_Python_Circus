#!/usr/bin/python3
"""Module for python_files_tracker."""

import ast
from collections.abc import Iterable
from contextlib import suppress
import os
import regex
from sys import stderr
from types import MappingProxyType
from typing import NamedTuple, TypedDict, Union

from file_handlers.files_dirs_search_list import FSSearchList
from file_handlers.walk_tree import walk_tree
from text.string import strip_path


class FileType(NamedTuple):
    """Indicates file type."""
    filename: str
    is_file: bool = False
    file_type: str | None = None


class FileBase(TypedDict):
    """Stores path to a file."""
    file: str | bytes | os.PathLike


class File(FileBase, total=False):
    """Container for a file's contents."""
    text: str
    byte_str: bytes
    tree: ast.AST


def get_filetype(file: str | bytes | os.PathLike) -> FileType:
    """Determine file type from extnsion or from the shebang.

    Args:
        file: a str or bytes object representing a path,
        or an object implementing the os.PathLike protocol.

    Returns:
        NamedTuple[filename: str, is_file: bool, file_type: str]

    Raises:
        TypeError: same errors that will be raised by os.fspath(file).
    """
    filename: str = str(os.fspath(file))
    is_file: bool = os.path.isfile(filename)
    if is_file is False:
        return FileType(filename, is_file)

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

    return FileType(filename, is_file, file_type)


class PyFileData:
    """A container for Python scipt data."""

    def __init__(
        self, filepath: str | bytes | os.PathLike | None = None,
        content: str | bytes = "", tree: ast.AST | None = None,
    ):
        """Initialise a container for Python scipt data."""
        self.__file: File = File(file="")
        self.filename = filepath  # type: ignore
        self.content = content
        self.tree = tree

    @property
    def file(self) -> File:
        """A TypedDict with filename and and it's contents."""
        return self.__file

    @property
    def filename(self) -> str | None:
        """Path to a file."""
        return self.__filename

    @filename.setter
    def filename(self, filepath: str | bytes | os.PathLike | None) -> None:
        """Initialise filename.

        Args:
            filepath: a str or bytes object representing a path,
                or an object implementing the os.PathLike protocol.

        Raises:
            TypeError: same errors that will be raised by os.fspath(filepath).
            ValueError: cannot ascertain if file is a python script
                filepath is not a path to a file
        """
        self.__filename: str | None = None
        if filepath is None:
            return

        self.__filename, is_file, file_type = get_filetype(filepath)
        if is_file is False:
            raise ValueError("filepath is not a path to a file")

        if (
            file_type is None or
            (file_type != ".py" and not file_type.startswith("python"))
        ):
            raise ValueError(
                "Cannot ascertain if file is a python script. "
                "Consider adding a .py extension or a shebang."
            )

        self.__file["file"] = self.__filename

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
        if isinstance(val, str):
            self.__file["text"] = val
        elif isinstance(val, bytes):
            self.__file["byte_str"] = val
        else:
            raise TypeError(f"object must be an instance of {str} or {bytes}")

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


class PyFileTracker:
    """A data tracker for Python scripts."""

    def __init__(
        self,
        pyfiles: Union[
            Iterable[str | bytes | os.PathLike], str, bytes, os.PathLike
        ] = (),
        directory: str | bytes | os.PathLike = "",
        max_descent: int = -1,
        blacklist: FSSearchList | None = None,
        whitelist: FSSearchList | None = None,
        pattern: str | None = None,
    ):
        """Initialise instance attributes for tracking files.

        Args:
            pyfiles: a path to a file or an Iterable of file paths.
            directory: a path to a python project directory.
            max_descent: an int indicating how many levels to descend while
                searching for files. A negative int means a full depth search,
                a positive number n means upto n levels deep, with 0 being the
                start directory.
            blacklist: a list of file/directory basenames to be excluded from a
                directory search.
            whitelist: a list of file/directory basenames to search for in a
                directory.
            pattern: a regex pattern to be used for searching directories.
        """
        self.pyfiles = pyfiles  # type: ignore
        self._pfmap: MappingProxyType[str, PyFileData] = MappingProxyType(
            self.__pyfiles)
        self.depth = max_descent
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.pattern = pattern
        self.directory = directory  # type: ignore

    @property
    def pyfiles(self) -> MappingProxyType[str, PyFileData]:
        """A mapping proxy of the files and their data."""
        return self._pfmap

    @pyfiles.setter
    def pyfiles(
            self,
            pyfiles: Union[
                Iterable[str | bytes | os.PathLike] |
                str | bytes | os.PathLike
            ],
    ) -> None:
        """Initialise pyfiles.

        Initialises a new mapping of filenames to instances of PyFileData.
        If an iterable is provided, any objects in it that raise a TypeError
        when called with os.fspath(), or that cannot be validated as Python
        scripts via their extensions or shebangs will be skipped and .

        Updates to self.directory will not remove any files already stored.

        Args:
            pyfiles: a path to a file or an Iterable of file paths.

        Raises:
            TypeError: pyfiles is neither an instance of os.PathLike,
                str or bytes nor an iterable of the same.
        """
        if isinstance(pyfiles, (str, bytes, os.PathLike)):
            temp: PyFileData = PyFileData(pyfiles)
            if temp.filename:
                temp.filename = strip_path(temp.filename)
                self.__pyfiles[temp.filename] = temp

            return

        if not isinstance(pyfiles, Iterable):
            raise TypeError(
                f"pyfiles must be an instance of {str}, {bytes} or "
                f"{os.PathLike} objects or an Iterable of the same."
            )

        self.__pyfiles: dict[str, PyFileData] = {}
        for file in pyfiles:
            if type(file) is str:
                try:
                    temp = PyFileData(file)
                except (TypeError, ValueError) as err:
                    print(f"Skipping {file}: Reason: {err}", file=stderr)
                    continue

                if temp.filename:
                    self.__pyfiles[temp.filename] = temp

    @property
    def directory(self) -> str:
        """Path to a directory with Python scripts."""
        return self.__workingdir

    @directory.setter
    def directory(self, directory: str | bytes | os.PathLike) -> None:
        """Initialise pyfiles with files in directory.

        The given directory will be searched for Python scripts with depth,
        whitelist and blacklist applied to the search. All Python scripts
        found will be added to pyfiles as a relative path from directory.
        The pyfiles will only be updated and not cleared.

        Args:
            directory: path to a directory with Python scripts.

        Raises:
            Any errors raised by os.fspath(directory).
        """
        # TODO(Andrew) check that encoding for bytes->str is utf-8
        directory = str(os.fspath(directory))
        self.__workingdir = strip_path(directory)
        for root, _dirs, files in walk_tree(
            self.__workingdir, self.pattern, self.whitelist,
            self.blacklist, self.depth,
        ):
            self.add_files([os.sep.join((root, file)) for file in files])

    @property
    def depth(self) -> int:
        """Max number of sub-directory levels to descend."""
        return self.__depth

    @depth.setter
    def depth(self, depth: int) -> None:
        """Initialise depth.

        Args:
            depth: an int indicating how many levels to descend while
                searching for files. A negative number implies a full depth
                search, a positive number n means upto n levels deep, with 0
                being the starting directory.

        Raises:
            TypeError: depth is not an int
        """
        if type(depth) is not int:
            raise TypeError("depth must be an integer")

        self.__depth = depth

    @property
    def blacklist(self) -> FSSearchList | None:
        """A blacklist of file/directory basenames."""
        return self.__blacklist

    @blacklist.setter
    def blacklist(self, blacklist: FSSearchList | None) -> None:
        """Initialise blacklist.

        Args:
            blacklist: a list of file/directory basenames to be excluded from
            a search.

        Raises:
            TypeError: blacklist is not None or an instance of FSSearchList
        """
        if (
            blacklist is not None and
            not isinstance(blacklist, FSSearchList)
        ):
            raise TypeError(
                "blacklist must be an instance of "
                f"{FSSearchList} or {None}"
            )

        self.__blacklist = blacklist

    @property
    def whitelist(self) -> FSSearchList | None:
        """A whitelist of file/directory basenames."""
        return self.__whitelist

    @whitelist.setter
    def whitelist(self, whitelist: FSSearchList | None) -> None:
        """Initialise whitelist.

        Args:
            whitelist: a list of file or directory basenames to search for.

        Raises:
            TypeError: whitelist is not None or an instance of FSSearchList
        """
        if (
            whitelist is not None and
            not isinstance(whitelist, FSSearchList)
        ):
            raise TypeError(
                "whitelist must be an instance of "
                f"{FSSearchList} or {None}"
            )

        self.__whitelist = whitelist

    def __repr__(self) -> str:
        """Return official string representation of this instance."""
        return (f"{self.__class__.__name__}({self.pyfiles}, "
                f"{self.directory}, {self.depth}, {self.blacklist}, "
                f"{self.whitelist})")

    def __getitem__(self, filename: str) -> PyFileData:
        """Get file data for filename.

        filename should be as it was added. For example if a directory search
        was performed, filename will be the path to the file starting from the
        project directory name. If filename was added to pyfiles directly, the
        name should be as it was added.

        Args:
            filename: name of the file to look up.

        Returns:
            An instance of PyFileData.

        Raises:
            TypeError: filename is not a str type
            KeyError: filename does not exist in pyfiles.
        """
        if type(filename) is not str:
            raise TypeError("filename must be a str")

        return self.__pyfiles[strip_path(filename)]

    def __setitem__(self, filename: str, data: PyFileData) -> None:
        """Update a file in pyfiles with data.

        Filename should be as it was added. For example if a directory search
        was performed, filename will be the path to the file starting from the
        project directory name. If filename was added to pyfiles directly, the
        name should be as it was added.

        Args:
            filename: path of the file to be updated.
            data: an instance of PyFileData.

        Raises:
            TypeError: filename is not a str, data is not a PyFileData object.
        """
        if type(filename) is not str:
            raise TypeError("filename must be a string")

        if not isinstance(data, PyFileData):
            raise TypeError(f"data must be an instance of {PyFileData}")

        self.__pyfiles[strip_path(filename)] = data

    def add_files(
        self,
        filepaths: Iterable[str | bytes | os.PathLike],
    ) -> None:
        """Update pyfiles with files in filepaths.

        Items in the iterable that cannot be verified as python scripts via
        their extensions or shebangs will be silently ignored.

        Args:
            filepaths: an Iterable of paths to files.

        Raises:
            TypeError: filepaths is not an Iterable.
        """
        if (
            isinstance(filepaths, (str, bytes, os.PathLike)) or
            not isinstance(filepaths, Iterable)
        ):
            raise TypeError("filepaths must be an Iterable of file paths")

        temp: PyFileData
        for file in filepaths:
            try:
                temp = PyFileData(file)
            except (ValueError):
                continue

            if temp.filename:
                self.__pyfiles.setdefault(
                    strip_path(temp.filename), PyFileData()
                )

    def clear(self) -> None:
        """Clear all items in pyfiles."""
        self.__pyfiles = {}

    def update(self, filename: str, data: PyFileData) -> None:
        """Update a file in pyfiles with data.

        Filename should be as it was added. For example if a directory search
        was performed, filename will be the path to the file starting from the
        project directory name. If filename was added to pyfiles directly, the
        name should be as it was added.

        Args:
            filename: path of the file to be updated.
            data: an instance of PyFileData

        Raises:
            TypeError: filename is not a string, data is not PyFileData
        """
        if type(filename) is not str:
            raise TypeError(f"filename must be an instance of {str}")

        if not isinstance(data, PyFileData):
            raise TypeError("data must be an instance of PyFileData")

        self.__pyfiles[strip_path(filename)] = data
