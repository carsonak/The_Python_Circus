#!/usr/bin/python3
"""Module for python_files_tracker."""

import ast
from collections.abc import Iterable, Iterator
from itertools import zip_longest
import os
from typing import Optional
from types import MappingProxyType

try:
    from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
except ModuleNotFoundError:
    from sys import path
    path.append("/home/line/Github_Repositories/The_Python_Circus")
    from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
    del path


class PyFileData:
    """Tracker for file data."""

    def __init__(self, contents: str = "", tree: ast.AST | None = None) -> None:
        self.contents = contents
        self.tree = tree

    @property
    def contents(self) -> str:
        """The contents of a file stored as a dtring."""
        return self.__contents

    @contents.setter
    def contents(self, val: str) -> None:
        """Initialise contents.

        Args:
            val: file contents as a string.

        Raises:
            TypeError: val is not a string.
        """
        if not isinstance(val, str):
            raise TypeError("value must be a string")

        self.__contents = val

    @property
    def tree(self) -> ast.AST | None:
        """Abstract syntax tree of a Python file."""
        return self.__tree

    @tree.setter
    def tree(self, val: ast.AST | None) -> None:
        """Initialise AST of a file.

        Args:
            val: the abstract syntax tree of a file.

        Raises:
            TypeError: val is not an instance of ast.AST or None.
        """
        if val and not isinstance(val, ast.AST):
            raise TypeError("value must be an instance of ast.AST or none")

        self.__tree = val


class PyFileTracker:
    """Tracker for python files."""

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
        self.__file_cache: dict[str, PyFileData] = {}
        self.py_files = py_files

        self.depth = max_descent
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.directory = directory

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
        if blacklist and not isinstance(blacklist, FileSystemBWlist):
            raise TypeError(
                "blacklist must be an instance of FileSystemBWlist or None")

        self.__blacklist = blacklist

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
        if whitelist and not isinstance(whitelist, FileSystemBWlist):
            raise TypeError(
                "whitelist must be an instance of FileSystemBWlist or None")

        self.__whitelist = whitelist

    @property
    def py_files(self) -> Iterable[str]:
        """An iterable of cached files."""
        return self.__file_cache.keys()

    @py_files.setter
    def py_files(self, py_files: Iterable[str]) -> None:
        """Initialise a cache with paths to python files.

        Initialises a mapping of filenames to data "contents" and "tree". Any
        items that are not of type str, not valid filepaths or don't have a
        .py extension, will be ignored.
        The filenames will not be affected by an update to directory.

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
                self.__file_cache[file] = PyFileData()

    @property
    def directory(self) -> str:
        """A python project directory."""
        return self.__workingdir

    @directory.setter
    def directory(self, directory: str) -> None:
        """Initialise py_files with files in directory.

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
            self.add_files([os.path.pathsep.join([root, file])
                            for file in files])

    def __getitem__(self, filename: str) -> PyFileData:
        """Return a mapping proxy of a file's current data.

        Args:
            filename: the name of the file to look up for.

        Returns:
            An instance of PyFileData.

        Raises:
            TypeError: filename is not a str type
            KeyError: filename does not exist in py_files.
        """
        if type(filename) is not str:
            raise TypeError("filename must be a str")

        return self.__file_cache[filename]

    def __setitem__(self, filename: str, data: PyFileData) -> None:
        """Update a file in py_files with data.

        Filename should be as it was added. For example if a directory search
        was performed, filename will be the path to the file starting from the
        project directory name. If filename was added to py_files directly, the
        name should be as it was added.

        Args:
            filename: path of the file to be updated.
            data: an instance of PyFileData

        Raises:
            TypeError: filename is not a string, data is not PyFileData
        """
        if type(filename) is not str:
            raise TypeError("filename must be a string")

        if not isinstance(data, PyFileData):
            raise TypeError("data must be an instance of PyFileData")

        self.__file_cache[filename] = data

    @staticmethod
    def walkdepth(start: str, max_depth: int = -1,
                  whitelist: Optional["FileSystemBWlist"] = None,
                  blacklist: Optional["FileSystemBWlist"] = None
                  ) -> Iterator[tuple[str, list[str], list[str]]]:
        """Genarate the directory tree of the given directory.

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

    def add_files(self, filenames: Iterable[str]) -> None:
        """Update py_files with new files.

        If a file name already exists in py_files, it's data will be cleared.
        Items in the iterable that are not strings, valid file paths or don't
        have a .py extension will be ignored.

        Args:
            filenames: an iterable of paths to files.

        Raises:
            TypeError: filenames is not an iterable of strings.
        """
        if not isinstance(filenames, Iterable) or type(filenames) is str:
            raise TypeError("filenames must be an Iterable of strings")

        for file in filenames:
            if (
                type(file) is str and
                os.path.isfile(file) and
                os.path.splitext(file)[1] == ".py"
            ):
                self.__file_cache[file] = PyFileData()

    def clear(self) -> None:
        """Clear the py_files cache."""
        self.__file_cache = {}

    def update(self, filename: str, data: PyFileData) -> None:
        if filename and type(filename) is not str:
            raise TypeError("filename must be a string")

        if not isinstance(data, PyFileData):
            raise TypeError("data must be an instance of PyFileData")

        self.__file_cache[filename] = data
