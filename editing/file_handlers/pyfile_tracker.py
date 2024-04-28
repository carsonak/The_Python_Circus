#!/usr/bin/python3
"""Module for python_files_tracker."""

import ast
from collections.abc import Iterable, Iterator
from itertools import zip_longest
from typing import Optional
import os

from editing.file_handlers.filesystem_bw_list import FileSystemBWlist


class PyFileTracker:
    """Tracker for python files being processed."""

    def __init__(self, py_files: Iterable[str] = (), directory: str = "",
                 max_descent: int = -1,
                 blacklist: Optional["FileSystemBWlist"] = None,
                 whitelist: Optional["FileSystemBWlist"] = None) -> None:
        """Initialise instance attributes for tracking files.

        Args:
            py_files: an iterable of file pathnames.
            directory: a pathname to a python project directory.
            max_descent: an int indicating how many levels to descend while
                searching for files. A negative int means a full depth search,
                a positive number n means upto n levels deep, with 0 being the
                start directory.
            blacklist: a list of file/directory basenames to be excluded from a
                directory search.
            whitelist: a list of file/directory basenames to search for in a
                directory.
        """
        self.__file_cache: dict[str, dict[str, ast.AST | str | None]] = {}
        self.depth = max_descent
        self.py_files = py_files
        self.directory = directory
        self.blacklist = blacklist
        self.whitelist = whitelist

    @property
    def depth(self) -> int:
        """Max number of sub-directory levels to descend."""
        return self.__depth

    @depth.setter
    def depth(self, depth: int) -> None:
        """Initialise depth.

        Args:
            depth: an int indicating how many levels to descend while
                searching for files. A negative int means a full depth search,
                a positive number n means upto n levels deep, with 0 being the
                start directory.

        Raises:
            TypeError: depth is not an int
        """
        if type(depth) is not int:
            raise TypeError("depth must be an integer")

        self.__depth = depth

    @property
    def blacklist(self) -> Optional["FileSystemBWlist"]:
        """A blacklist of file/directory basenames."""
        return self.__blacklist

    @blacklist.setter
    def blacklist(self, blacklist: Optional["FileSystemBWlist"]) -> None:
        """Initialise blacklist.

        Args:
            blacklist: a list of file/directory basenames to be excluded from
            a search.

        Raises:
            TypeError: blacklist is not None or an instance of FileSystemBWlist
        """
        if isinstance(blacklist, FileSystemBWlist) or blacklist is None:
            self.__blacklist = blacklist
        else:
            raise TypeError(
                "blacklist must be an instance of FileSystemBWlist or None")

    @property
    def whitelist(self) -> Optional["FileSystemBWlist"]:
        """A whitelist of file/directory basenames."""
        return self.__whitelist

    @whitelist.setter
    def whitelist(self, whitelist: Optional["FileSystemBWlist"]) -> None:
        """Initialise whitelist.

        Args:
            whitelist: a list of file or directory basenames to search for.

        Raises:
            TypeError: whitelist is not None or an instance of FileSystemBWlist
        """
        if isinstance(whitelist, FileSystemBWlist) or whitelist is None:
            self.__whitelist = whitelist
        else:
            raise TypeError(
                "whitelist must be an instance of FileSystemBWlist or None")

    @property
    def py_files(self) -> Iterable:
        """An iterable of files and their contents."""
        return self.__file_cache.items()

    @py_files.setter
    def py_files(self, py_files: Iterable[str]) -> None:
        """Initialise a cache with paths to python files.

        Initialises a dictionary of python file paths and their modified
        abstract syntax tree. Any file names that don't exist, don't have a
        .py extension or an object in the iterable that is not type string,
        will be ignored.
        The files stored will not be cleared if directory is changed.

        Args:
            py_files: An iterable of file pathnames.

        Raises:
            TypeError: py_files is not an iterable or is just a string.
        """
        if not isinstance(py_files, Iterable) or type(py_files) is str:
            raise TypeError("py_files must be an Iterable of strings.")

        self.__file_cache = {}
        for file in py_files:
            if (
                type(file) is str and
                os.path.isfile(file) and
                os.path.splitext(file)[1] == ".py"
            ):
                self.__file_cache[file] = {"contents": None, "tree": None}

    @property
    def directory(self) -> str:
        """Current working directory being processed."""
        return self.__workingdir

    @directory.setter
    def directory(self, directory: str) -> None:
        """Initialise the working directory and it's python files.

        The given directory will be searched for python files with depth,
        whitelist and blacklist applied to the search. The resulting files
        will be added to py_files. The py_files cache will not be cleared if
        directory is changed.

        Args:
            directory: This the pathname of a python project directory.

        Raises:
            TypeError: directory is not a string.
        """
        if type(directory) is not str:
            raise TypeError("directory must be an instance of str")

        self.__workingdir = directory
        for root, dirs, files in self.walkdepth(directory, self.depth,
                                                self.whitelist,
                                                self.blacklist):
            self.add_files(files)

    def __getitem__(self, filename: str) -> dict[str, None | str | ast.AST]:
        """Return"""
        if type(filename) is not str:
            raise TypeError("filename must be a str")

        return ReadOnlyDict(self.__file_cache[filename])

    @staticmethod
    def walkdepth(start: str, max_depth: int = -1,
                  whitelist: Optional["FileSystemBWlist"] = None,
                  blacklist: Optional["FileSystemBWlist"] = None
                  ) -> Iterator[tuple[str, list[str], list[str]]]:
        """Traverse the sub-directories of the given directory.

        This is a directory tree generator that behaves similar to os.walk()
        except it can prune directories according to a depth, filter out files
        and directories according to a blacklist or search only for specific
        files and directories according to a whitelist.

        Args:
            start: a path to a directory.
            max_depth: an int indicating how many levels to descend while
                searching for files. A negative int means a full depth search,
                a positive int n means upto n levels deep, with 0 being the
                start directory.
            whitelist: an optional List of file or directory basenames to
                search for. If a whitelist exists for files or directories the
                corresponding blacklist will be ignored.
            blacklist: an optional List of file or director basenames to be
                excluded from the search. If a whitelist exists for files or
                directories the corresponding blacklist will be ignored.

        Yields:
            A tuple of three items:
                dirpath, dirnames, filenames
            dirpath is the path to the directory. dirnames is a list of the
            names of the subdirectories in dirpath (including symlinks to
            directories, and excluding '.' and '..'). filenames is a list of
            the names of the non-directory files in dirpath.
            The names in the lists are just names, with no path components.

        Raises:
            TypeError: one of the parameters is not the correct type.
        """
        if type(start) is not str:
            raise TypeError("start must be a string")

        if type(max_depth) is not int:
            raise TypeError("max_depth must be an int")

        if whitelist and type(whitelist) is not FileSystemBWlist:
            raise TypeError(
                "whitelist must be an instance of FileSystemBWlist or None")

        if blacklist and type(blacklist) is not FileSystemBWlist:
            raise TypeError(
                "blacklist must be an instance of FileSystemBWlist or None")

        base_depth: int = start.count(os.path.sep)
        for root, dirnames, filenames in os.walk(start):
            for dir, file in zip_longest(dirnames[:], filenames[:]):
                if dir:
                    if whitelist and whitelist.directories:
                        if not whitelist.in_dirs(dir):
                            dirnames.remove(dir)
                    elif blacklist and blacklist.in_dirs(dir):
                        dirnames.remove(dir)

                if file:
                    if whitelist and whitelist.files:
                        if not whitelist.in_files(file):
                            filenames.remove(file)
                    elif blacklist and blacklist.in_files(file):
                        filenames.remove(file)

            current_depth: int = root.count(os.path.sep) - base_depth
            if 0 <= max_depth <= current_depth:
                del dirnames[:]

            yield root, dirnames, filenames

    def add_files(self, items: Iterable[str]) -> None:
        """Update py_files with new files."""
        if not isinstance(items, Iterable) or type(items) is str:
            raise TypeError("items must be an Iterable of strings")

        for file in items:
            if (
                type(file) is str and
                os.path.isfile(file) and
                os.path.splitext(file)[1] == ".py"
            ):
                self.__file_cache[file] = {"contents": None, "tree": None}

    def clear(self) -> None:
        """Clear the py_files cache."""
        self.__file_cache = {}

    def update(self, filename: str,
               contents: str | None = None,
               tree: ast.AST | None = None
               ) -> "ReadOnlyDict[str, None | str | ast.AST]":
        if filename and type(filename) is not str:
            raise TypeError("filename must be a string")

        if contents and type(contents) is not str:
            raise TypeError("contents must be a string")

        if tree and not isinstance(tree, ast.AST):
            raise TypeError("tree must be an instance of ast.AST")

        self.__file_cache[filename] = {"contents": contents, "tree": tree}
        return ReadOnlyDict(self.__file_cache[filename])



class ReadOnlyDict(dict):
    """A readonly dictionary."""

    def __setitem__(self, key, value) -> None:
        """Not Modifiable."""
        raise TypeError("cannot modify ReadOnlyDict")

    def __delitem__(self, key) -> None:
        """Not Modifiable."""
        raise TypeError("cannot modify ReadOnlyDict")

    def clear(self) -> None:
        """Not Modifiable."""
        raise TypeError("cannot modify ReadOnlyDict")

    def popitem(self) -> tuple:
        """Not Modifiable."""
        raise TypeError("cannot modify ReadOnlyDict")

    def pop(self, k, d=None):
        """Not Modifiable."""
        raise TypeError("cannot modify ReadOnlyDict")

    def setdefault(self, key, defualt=None) -> None:
        """Not Modifiable."""
        raise TypeError("cannot modify ReadOnlyDict")

    def update(self, E, **kwargs) -> None:
        """Not modifiable."""
        raise TypeError("cannot modify ReadOnlyDict")


if __name__ == "__main__":
    rd = ReadOnlyDict(key="item", sum="all")
    print(rd)
    rd.update(sum="nun", more="items")
    print(rd)
    rd.clear()
