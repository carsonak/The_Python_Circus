#!/usr/bin/python3
"""Module for remove_annotations."""

import ast
import os
from collections.abc import Iterable, Generator
from itertools import zip_longest


class FileTracker:
    """Class for parsing files."""

    def __init__(self, py_files: Iterable[str] = (), directory: str = "",
                 max_descent: int = -1,
                 blacklist: "FileSystemBWlist" | None = None,
                 whitelist: "FileSystemBWlist" | None = None) -> None:
        """Initialise instance attributes."""
        self.__file_cache: dict[str, ast.AST | None] = {}
        self.depth = max_descent
        self.py_files = py_files
        self.directory = directory
        self.blacklist = blacklist
        self.whitelist = whitelist

    @property
    def depth(self) -> int:
        """Return depth."""
        return self.__depth

    @depth.setter
    def depth(self, depth: int) -> None:
        """Initialise max search depth for directories."""
        if type(depth) is not int:
            raise TypeError("depth must be an integer")

        self.__depth = depth

    @property
    def blacklist(self) -> "FileSystemBWlist" | None:
        """Return a blacklist of files and directories."""
        return self.__blacklist

    @blacklist.setter
    def blacklist(self, blacklist: "FileSystemBWlist" | None) -> None:
        """Initialise blacklist."""
        if isinstance(blacklist, FileSystemBWlist) or blacklist is None:
            self.__blacklist = blacklist
        else:
            raise TypeError(
                "blacklist must be an instance of FileSystemBWlist or None")

    @property
    def whitelist(self) -> "FileSystemBWlist" | None:
        """Return a whitelist of files and directories."""
        return self.__whitelist

    @whitelist.setter
    def whitelist(self, whitelist: "FileSystemBWlist" | None) -> None:
        """Initialise whitelist."""
        if isinstance(whitelist, FileSystemBWlist) or whitelist is None:
            self.__whitelist = whitelist
        else:
            raise TypeError(
                "whitelist must be an instance of FileSystemBWlist or None")

    @property
    def py_files(self) -> Iterable[str]:
        """Return files to be processed."""
        return self.__file_cache.keys()

    @py_files.setter
    def py_files(self, py_files: Iterable[str]) -> None:
        """Update the file cache with paths to python files.

        Args:
            py_files: An iterable of file pathnames.
        """
        if not isinstance(py_files, Iterable) or type(py_files) is str:
            raise TypeError("py_files must be an Iterable")

        self.__file_cache = {}
        for file in py_files:
            if (
                type(file) is str and
                os.path.isfile(file) and
                os.path.splitext(file)[1] == ".py"
            ):
                self.__file_cache[file] = None

    @property
    def directory(self) -> str:
        """Return the working directory being processed."""
        return self.__workingdir

    @directory.setter
    def directory(self, directory: str) -> None:
        """Explore directories and add python files to cache.

        Args:
            directory : This the name of the directory that will be used as
                a working directory.
        """
        if type(directory) is not str:
            raise TypeError("directory must be an instance of str")

        self.__workingdir = directory
        for root, dirs, files in self.walkdepth(directory, self.depth,
                                                self.blacklist,
                                                self.whitelist):
            self.add_files(files)

    @staticmethod
    def walkdepth(start: str, max_depth: int = -1,
                  blacklist: "FileSystemBWlist" | None = None,
                  whitelist: "FileSystemBWlist" | None = None) -> Generator[
                      tuple[str, list[str], list[str]], None, None]:
        """Traverse the sub-directories of the given directory
        and yield a three tuple of the root, directories and files.
        """
        if type(start) is not str:
            raise TypeError("start must be a string")

        base_depth: int = start.count(os.path.sep)
        for root, dirs, files in os.walk(start):
            for d, f in zip_longest(dirs[:], files[:]):
                if d:
                    if whitelist and not whitelist.in_dirs(d):
                        dirs.remove(f)
                    elif blacklist and blacklist.in_dirs(d):
                        dirs.remove(f)

                if f:
                    if whitelist and not whitelist.in_files(f):
                        files.remove(f)
                    elif blacklist and blacklist.in_files(f):
                        files.remove(f)

            current_depth: int = root.count(os.path.sep) - base_depth
            if 0 <= max_depth <= current_depth:
                del dirs[:]

            yield root, dirs, files

    def add_files(self, items: Iterable[str]) -> None:
        """Update the file cache with new files."""
        if not isinstance(items, Iterable) or type(items) is str:
            raise TypeError("items must be an Iterable of strings")

        for file in items:
            if (
                type(file) is str and
                os.path.isfile(file) and
                os.path.splitext(file)[1] == ".py"
            ):
                self.__file_cache[file] = None


class BlackWhitelist:
    """Class for creating a blacklist or whitelist of objects."""

    def __init__(self, items: Iterable) -> None:
        """Initialise a Black/Whitelist of items."""
        self.itemslist = items

    @property
    def itemslist(self) -> Iterable:
        """Return a tuple of items in the List."""
        return tuple(self.__itemList)

    @itemslist.setter
    def itemslist(self, items: Iterable) -> None:
        """Create a List of items."""
        if isinstance(items, Iterable):
            self.__itemList: set = set([i for i in items])
        else:
            raise TypeError("itemslist must be an Iterable")

    def __str__(self) -> str:
        """Return a string listing the items in the List."""
        return str(self.__itemList)

    def __repr__(self) -> str:
        """Return a string of valid Python code that can recreate
        this instance.
        """
        return f"{self.__class__.__name__}({self.__itemList})"

    def __add__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return a union of self and other."""
        if isinstance(other, BlackWhitelist):
            t = BlackWhitelist(self.__itemList.union(other.__itemList))
            return t
        else:
            return NotImplemented

    def __iadd__(self, other: "BlackWhitelist") -> None:
        """Update self with a union of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__itemList.update(other.__itemList)
        else:
            return NotImplemented

    def __sub__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return a difference of self and other."""
        if isinstance(other, BlackWhitelist):
            t = BlackWhitelist(self.__itemList.difference(other.__itemList))
            return t
        else:
            return NotImplemented

    def __isub__(self, other: "BlackWhitelist") -> None:
        """Update self with the difference of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__itemList.difference_update(other.__itemList)
        else:
            return NotImplemented

    def __and__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return an intersection of self and other."""
        if isinstance(other, BlackWhitelist):
            t = BlackWhitelist(self.__itemList & other.__itemList)
            return t
        else:
            return NotImplemented

    def __iand__(self, other: "BlackWhitelist") -> None:
        """Return an intersection of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__itemList.intersection(other.__itemList)
        else:
            return NotImplemented

    def __or__(self, other: "BlackWhitelist") -> "BlackWhitelist":
        """Return a union of self and other."""
        if isinstance(other, BlackWhitelist):
            t = BlackWhitelist(self.__itemList.union(other.__itemList))
            return t
        else:
            return NotImplemented

    def __ior__(self, other: "BlackWhitelist") -> None:
        """Update self with a union of self and other."""
        if isinstance(other, BlackWhitelist):
            self.__itemList.update(other.__itemList)
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        """Return self == other."""
        if isinstance(other, BlackWhitelist):
            return self.__itemList == other.__itemList
        else:
            return NotImplemented

    def __lt__(self, other: object) -> bool:
        """Return self < other."""
        if isinstance(other, BlackWhitelist):
            return self.__itemList < other.__itemList
        else:
            return NotImplemented

    def __len__(self) -> int:
        """Return length of the List."""
        return len(self.__itemList)

    def __contains__(self, item) -> bool:
        """Return whether an item is in List"""
        return item in self.__itemList

    def add(self, item) -> None:
        """Add an item to the List."""
        self.__itemList.add(item)

    def discard(self, item) -> None:
        """Remove an item from the List if it is a member.
        If the item is not a member, do nothing.
        """
        self.__itemList.discard(item)

    def clear(self) -> None:
        """Clear all items from the List."""
        self.__itemList.clear()


class FileSystemBWlist:
    """Class for creating a file/directory Blacklist or Whitelist."""

    def __init__(self, files: Iterable[str] = (), directories: Iterable[str] = ()) -> None:
        """Initialise a files List and a directories List."""
        self.__fileList: BlackWhitelist = BlackWhitelist(())
        self.files = files
        self.__dirList: BlackWhitelist = BlackWhitelist(())
        self.directories = directories

    @property
    def files(self) -> Iterable[str]:
        """Return a black/whitelist of files."""
        return self.__fileList.itemslist

    @files.setter
    def files(self, files: Iterable[str]) -> None:
        """Create a black/whitelist of files."""
        for f in files:
            if isinstance(f, str):
                self.__fileList.add(f)
            else:
                raise TypeError(
                    "All items in files must be instances of str")

    @property
    def directories(self) -> Iterable[str]:
        """Return a black/whitelist of directories."""
        return self.__dirList.itemslist

    @directories.setter
    def directories(self, directories: Iterable[str]) -> None:
        """Create a black/whitelist of directories."""
        for d in directories:
            if isinstance(d, str):
                self.__dirList.add(d)
            else:
                raise TypeError(
                    "All items in directories must be instances of str")

    def __str__(self) -> str:
        """Return a str representing this instance."""
        return f"Directories: {self.__dirList}, Files: {self.__fileList}"

    def __repr__(self) -> str:
        """Return a string of valid Python code that can recreate
        this instance.
        """
        return f"{self.__class__.__name__}({self.__fileList}, {self.__dirList})"

    def __contains__(self, item: str) -> bool:
        """Return whether item is found in either Lists."""
        if type(item) is str:
            return item in self.__fileList or item in self.__dirList

        return False

    def add_file(self, item: str) -> None:
        """Adds an entry to the file List."""
        if type(item) is str:
            self.__fileList.add(item)
        else:
            raise TypeError("item must be an instance of str")

    def add_dir(self, item: str) -> None:
        """Adds an entry to the directory List."""
        if type(item) is str:
            self.__dirList.add(item)
        else:
            raise TypeError("item must be an instance of str")

    def drop_file(self, item: str) -> None:
        """Delete an entry from file List."""
        if type(item) is str:
            self.__fileList.discard(item)

    def drop_dir(self, item: str) -> None:
        """Delete an entry from directory List."""
        if type(item) is str:
            self.__dirList.discard(item)

    def in_files(self, item: str) -> bool:
        """Return whether item can be found in file List."""
        if type(item) is str:
            return item in self.__fileList

        return False

    def in_dirs(self, item: str) -> bool:
        """Return whether an item can be found in directory List."""
        if type(item) is str:
            return item in self.__dirList

        return False

    def clear_files(self) -> None:
        """Delete file List."""
        self.__fileList.clear()

    def clear_dirs(self) -> None:
        """Delete file List."""
        self.__dirList.clear()


class TypeHintsRemover(ast.NodeTransformer):
    """Class for removing type annotations."""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        # remove the return type defintion
        node.returns = None
        # remove all argument annotations
        if node.args.args:
            for arg in node.args.args:
                arg.annotation = None
        return node

    def visit_Import(self, node: ast.Import) -> ast.Import | None:
        node.names = [n for n in node.names if n.name != 'typing']
        return node if node.names else None

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom | None:
        return node if node.module != 'typing' else None


def main() -> None:
    """Entry point."""
    # Instantiate a black list
    # Instantiate a file tracker
    # Generate edited ASTs for the files
    # Parse the ASTs and update the files


if __name__ == "__main__":
    main()
