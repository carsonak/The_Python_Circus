#!/usr/bin/python3
"""Module for filesysytem_blacklist_whitelist."""

from collections.abc import Iterable

from editing.file_handlers.blackwhite_list import BlackWhitelist


class FileSystemBWlist:
    """Blacklist/whitelist manager for files and directories."""

    def __init__(self, files: Iterable[str] = ("", ),
                 directories: Iterable[str] = ("", )) -> None:
        """Initialise a files List and a directories List.

        Args:
            files: an iterable of strings representing paths to files.
            directories: an iterable of strings representing paths to
                directories.
        """
        self.files = files
        self.directories = directories

    @property
    def files(self) -> BlackWhitelist:
        """Files List."""
        return self.__fileList

    @files.setter
    def files(self, files: Iterable[str]) -> None:
        """Create a List of files."""
        self.__fileList: BlackWhitelist = BlackWhitelist(())
        for f in files:
            if isinstance(f, str):
                self.__fileList.add(f)
            else:
                raise TypeError(
                    "All items in files must be instances of str")

    @property
    def directories(self) -> BlackWhitelist:
        """Directories List."""
        return self.__dirList

    @directories.setter
    def directories(self, directories: Iterable[str]) -> None:
        """Create a List of directories."""
        self.__dirList: BlackWhitelist = BlackWhitelist(())
        for d in directories:
            if isinstance(d, str):
                self.__dirList.add(d)
            else:
                raise TypeError(
                    "All items in directories must be instances of str")

    def __str__(self) -> str:
        """Return an informal str representation of this instance."""
        return f"Directories: {self.__dirList}, Files: {self.__fileList}"

    def __repr__(self) -> str:
        """Return an official string representation of this instance."""
        return (f"{self.__class__.__name__}"
                f"({self.__fileList}, {self.__dirList})")

    def __contains__(self, path: str) -> bool:
        """Check if path exists in either List.

        Args:
            path: a path to a file or directory.
        """
        if type(path) is str:
            return path in self.__fileList or path in self.__dirList

        return False

    def add_file(self, path: str | Iterable[str]) -> None:
        """Add path to the file List.

        Args:
            path: path to a file or an iterable with pathnames.
        """
        if type(path) is str:
            self.__fileList.add(path)
        elif isinstance(path, Iterable):
            self.__fileList.add({p for p in path if type(p) is str})
        else:
            raise TypeError("path must be a string or an iterable of strings")

    def add_dir(self, path: str | Iterable[str]) -> None:
        """Add path to the directory List.

        Args:
            path: path to a directory or an iterable with pathnames.
        """
        if type(path) is str:
            self.__dirList.add(path)
        elif isinstance(path, Iterable):
            self.__dirList.add({p for p in path if type(p) is str})
        else:
            raise TypeError("path must be a string or an iterable of strings")

    def drop_file(self, path: str | Iterable[str]) -> None:
        """Delete an entry from file List.

        Args:
            path: path to a file or an iterable with pathnames.
        """
        if type(path) is str:
            self.__fileList.discard(path)
        elif isinstance(path, Iterable):
            self.__fileList.discard({p for p in path if type(p) is str})

    def drop_dir(self, path: str | Iterable[str]) -> None:
        """Delete an entry from dir List.

        Args:
            path: path to a dir or an iterable with pathnames.
        """
        if type(path) is str:
            self.__dirList.discard(path)
        elif isinstance(path, Iterable):
            self.__dirList.discard({p for p in path if type(p) is str})

    def in_files(self, path: str) -> bool:
        """Return whether path can be found in file List."""
        if type(path) is str:
            return path in self.__fileList

        return False

    def in_dirs(self, path: str) -> bool:
        """Return whether an path can be found in directory List."""
        if type(path) is str:
            return path in self.__dirList

        return False

    def clear_files(self) -> None:
        """Delete all entries in file List."""
        self.__fileList.clear()

    def clear_dirs(self) -> None:
        """Delete all entries in dir List."""
        self.__dirList.clear()
