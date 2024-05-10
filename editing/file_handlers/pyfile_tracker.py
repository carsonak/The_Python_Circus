#!/usr/bin/python3
"""Module for python_files_tracker."""

import ast
from collections.abc import Iterable, Iterator
from itertools import zip_longest
import os

try:
    from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
except ModuleNotFoundError:
    from sys import path
    from os.path import dirname, realpath
    path.append(dirname(dirname(dirname(realpath(__file__)))))
    from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
    del path, realpath, dirname


class PyFileData:
    """A container for Python scipt data."""

    def __init__(self, contents: str = "", tree: ast.AST | None = None):
        """Initialise a container for Python scipt data."""
        self.contents = contents
        self.tree = tree

    @property
    def contents(self) -> str:
        """Text content of a python script."""
        return self.__contents

    @contents.setter
    def contents(self, val: str) -> None:
        """Initialise contents.

        Args:
            val: a string representing the raw text of a python script.

        Raises:
            TypeError: val is not a string.
        """
        if not isinstance(val, str):
            raise TypeError("object must be an instance of a string")

        self.__contents = val

    @property
    def tree(self) -> ast.AST | None:
        """Abstract Syntax Tree of a Python script."""
        return self.__tree

    @tree.setter
    def tree(self, val: ast.AST | None) -> None:
        """Initialise tree.

        Args:
            val: the abstract syntax tree of a Python script.

        Raises:
            TypeError: val is not an instance of ast.AST or None.
        """
        if val and not isinstance(val, ast.AST):
            raise TypeError("object must be an instance of ast.AST or none")

        self.__tree = val

    def __repr__(self) -> str:
        """Return an official string representation of this instance."""
        return f"{self.__class__.__name__}({self.contents}, {self.tree})"


class PyFileTracker:
    """A data tracker for Python scripts."""

    def __init__(self, py_files: Iterable[str] = (), directory: str = "",
                 max_descent: int = -1,
                 blacklist: FileSystemBWlist | None = None,
                 whitelist: FileSystemBWlist | None = None):
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
    def blacklist(self) -> FileSystemBWlist | None:
        """A blacklist of file/directory basenames."""
        return self.__blacklist

    @blacklist.setter
    def blacklist(self, blacklist: FileSystemBWlist | None) -> None:
        """Initialise blacklist.

        Args:
            blacklist: a list of file/directory basenames to be excluded from
            a search.

        Raises:
            TypeError: blacklist is not None or an instance of FileSystemBWlist
        """
        if blacklist is not None and not isinstance(blacklist,
                                                    FileSystemBWlist):
            raise TypeError(
                "blacklist must be an instance of FileSystemBWlist or None")

        self.__blacklist = blacklist

    @property
    def whitelist(self) -> FileSystemBWlist | None:
        """A whitelist of file/directory basenames."""
        return self.__whitelist

    @whitelist.setter
    def whitelist(self, whitelist: FileSystemBWlist | None) -> None:
        """Initialise whitelist.

        Args:
            whitelist: a list of file or directory basenames to search for.

        Raises:
            TypeError: whitelist is not None or an instance of FileSystemBWlist
        """
        if whitelist is not None and not isinstance(whitelist,
                                                    FileSystemBWlist):
            raise TypeError("whitelist must be an instance of "
                            "FileSystemBWlist or None")

        self.__whitelist = whitelist

    @property
    def py_files(self) -> Iterable[str]:
        """An iterable of cached file names."""
        return self.__file_cache.keys()

    @py_files.setter
    def py_files(self, py_files: Iterable[str]) -> None:
        """Initialise py_files.

        Initialises a new mapping of filenames to their data "contents" and
        "tree". Any items in the iterable that are: not type str, not valid
        filepaths or don't have a py extension, will be ignored.
        The filenames will not be affected by an update to directory.

        Args:
            py_files: An iterable of file pathnames.

        Raises:
            TypeError: py_files is not an iterable or is a string.
        """
        if not isinstance(py_files, Iterable) or type(py_files) is str:
            raise TypeError("py_files must be an Iterable of strings.")

        self.__file_cache: dict[str, PyFileData] = {}
        for file in py_files:
            if (
                type(file) is str and
                os.path.isfile(file) and
                os.path.splitext(file)[1] == ".py"
            ):
                file = file.rstrip(os.sep)
                self.__file_cache[
                    file[2:] if file.startswith(f".{os.sep}") else file
                    ] = PyFileData()

    @property
    def directory(self) -> str:
        """Pathname of a directory with Python scripts."""
        return self.__workingdir

    @directory.setter
    def directory(self, directory: str) -> None:
        """Initialise py_files with files in directory.

        The given directory will be searched for Python scripts with depth,
        whitelist and blacklist applied to the search. All Python scripts
        found will be added to py_files as a relative path from directory.
        The py_files will only be updated and not cleared.

        Args:
            directory: pathname of a directory with Python scripts.

        Raises:
            TypeError: directory is not a string.
        """
        if type(directory) is not str:
            raise TypeError("directory must be an instance of str")

        directory = directory.rstrip(os.sep)
        if directory.startswith(f".{os.sep}") and len(directory) > 2:
            directory = directory[2:]

        self.__workingdir = directory
        for root, _dirs, files in self.walkdepth(
                self.__workingdir, self.depth, self.whitelist, self.blacklist):
            self.add_files([os.sep.join((root, file)) for file in files])

    def __repr__(self) -> str:
        """Return official string representation of this instance."""
        return (f"{self.__class__.__name__}({self.py_files}, "
                f"{self.directory}, {self.depth}, {self.blacklist}, "
                f"{self.whitelist})")

    def __getitem__(self, filename: str) -> PyFileData:
        """Get file data for filename.

        Filename should be as it was added. For example if a directory search
        was performed, filename will be the path to the file starting from the
        project directory name. If filename was added to py_files directly, the
        name should be as it was added.

        Args:
            filename: name of the file to look up.

        Returns:
            An instance of PyFileData.

        Raises:
            TypeError: filename is not a str type
            KeyError: filename does not exist in py_files.
        """
        if type(filename) is not str:
            raise TypeError("filename must be a str")

        filename = filename.rstrip(os.sep)
        return self.__file_cache[
            filename[2:] if filename.startswith(f".{os.sep}") else filename]

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
                  whitelist: FileSystemBWlist | None = None,
                  blacklist: FileSystemBWlist | None = None
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
            A tuple of three items: dirpath, dirnames, filenames.
            `dirpath` is the path to the directory. `dirnames` is a list of the
            names of the subdirectories in dirpath (including symlinks to
            directories, and excluding '.' and '..'). `filenames` is a list of
            the names of the non-directory files in dirpath.
            The names in the lists are just names, with no path components.

        Raises:
            TypeError: start is not a string.
                maxdepth is not an int.
                whitelist is not None or an instance of FileSystemBWlist.
                blacklist is not None or an instance of FileSystemBWlist.
        """
        if type(start) is not str:
            raise TypeError("start must be a string")

        if type(max_depth) is not int:
            raise TypeError("max_depth must be an int")

        if whitelist is not None and not isinstance(whitelist,
                                                    FileSystemBWlist):
            raise TypeError("whitelist must be None or "
                            "an instance of FileSystemBWlist")

        if blacklist is not None and not isinstance(blacklist,
                                                    FileSystemBWlist):
            raise TypeError("blacklist must be None or "
                            "an instance of FileSystemBWlist")

        start = start.rstrip(os.sep)
        if start.startswith(f".{os.sep}") and len(start) > 2:
            start = start[2:]

        base_depth: int = start.count(os.sep)
        for root, dirnames, filenames in os.walk(start):
            for dir, file in zip_longest(dirnames[:], filenames[:]):
                if dir:
                    rel_dirname: str = os.sep.join((root, dir))
                    if whitelist and whitelist.directories:
                        if not whitelist.in_dirs(rel_dirname):
                            dirnames.remove(dir)
                    elif blacklist and blacklist.in_dirs(rel_dirname):
                        dirnames.remove(dir)

                if file:
                    rel_filename: str = os.sep.join((root, file))
                    if whitelist and whitelist.files:
                        if not whitelist.in_files(rel_filename):
                            filenames.remove(file)
                    elif blacklist and blacklist.in_files(rel_filename):
                        filenames.remove(file)

            current_depth: int = root.count(os.sep) - base_depth
            if 0 <= max_depth <= current_depth:
                del dirnames[:]

            yield root, dirnames, filenames

    def add_files(self, filenames: Iterable[str]) -> None:
        """Update py_files with new files.

        If a file name already exists in py_files, it's data will be cleared.
        Items in the iterable that are: not strings, valid file paths or don't
        have a .py extension will be ignored.

        Args:
            filenames: an iterable of paths to files.

        Raises:
            TypeError: filenames is not an iterable.
        """
        if not isinstance(filenames, Iterable) or type(filenames) is str:
            raise TypeError("filenames must be an Iterable of strings")

        for file in filenames:
            if (
                type(file) is str and
                os.path.isfile(file) and
                os.path.splitext(file)[1] == ".py"
            ):
                file = file.rstrip(os.sep)
                self.__file_cache[
                    file[2:] if file.startswith(f".{os.sep}") else file
                    ] = PyFileData()

    def clear(self) -> None:
        """Clear all items in py_files."""
        self.__file_cache = {}

    def update(self, filename: str, data: PyFileData) -> None:
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
