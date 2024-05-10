#!/usr/bin/python3
"""Module for filesysytem_blacklist_whitelist."""

from collections.abc import Iterable
from os.path import basename

try:
    from editing.file_handlers.blackwhite_list import BlackWhitelist
except ModuleNotFoundError:
    from sys import path
    from os.path import abspath, dirname
    path.append(abspath(dirname(dirname(dirname(__file__)))))
    from editing.file_handlers.blackwhite_list import BlackWhitelist
    del path, abspath, dirname


class FileSystemBWlist:
    """Blacklist/whitelist manager for files and directories."""

    def __init__(self, files: Iterable[str] = ("", ),
                 directories: Iterable[str] = ("", )):
        """Initialise a files List and a directories List.

        Args:
            files: an iterable of strings representing paths to files.
            directories: an iterable of strings representing paths to
                directories.
        """
        self.files = files
        self.directories = directories

    @property
    def files(self) -> Iterable[str]:
        """A List of Files."""
        return self.__fileList.itemslist

    @files.setter
    def files(self, files: Iterable[str]) -> None:
        """Create a List of files.

        Any items in the iterable that are not strings will be ignored.

        Args:
            files: an iterable of strings and not type str itself.

        Raises:
            TypeError: files is a string or not an iterable of strings.
        """
        if not isinstance(files, Iterable) or type(files) is str:
            raise TypeError("files only accepts and iterable of strings.")

        self.__fileList: BlackWhitelist = BlackWhitelist(())
        tmp: set[str] = set()
        for f in files:
            if isinstance(f, str):
                tmp.add(f[2:] if f.startswith("./") else f)

        self.__fileList.add(tmp)

    @property
    def directories(self) -> Iterable[str]:
        """A List of directories."""
        return self.__dirList.itemslist

    @directories.setter
    def directories(self, directories: Iterable[str]) -> None:
        """Create a List of directories.

        Any items in the iterable that are not strings will be ignored.

        Args:
            directories: an iterable of strings and not type str itself.

        Raises:
            TypeError: directories is a string or not an iterable of strings.
        """
        if not isinstance(directories, Iterable) or type(directories) is str:
            raise TypeError("directories must be an Iterable of strings")

        self.__dirList: BlackWhitelist = BlackWhitelist(())
        tmp: set[str] = set()
        for d in directories:
            if isinstance(d, str):
                tmp.add(d[2:] if d.startswith("./") and len(d) > 2 else d)

    def __repr__(self) -> str:
        """Return an official string representation of this instance."""
        return (f"{self.__class__.__name__}"
                f"({self.__fileList}, {self.__dirList})")

    def __contains__(self, path: str) -> bool:
        """Check if a path exists in either List.

        Args:
            path: a path to a file or directory.
        """
        if type(path) is str:
            if path.startswith("./") and len(path) > 2:
                path = path[2:]

            return (
                (path in self.__fileList or path in self.__dirList) or
                (basename(path) in self.__fileList or
                 basename(path) in self.__fileList)
            )

        return False

    def add_file(self, path: str | Iterable[str]) -> None:
        """Add a path or paths to the file List.

        Args:
            path: path to a file or an iterable with pathnames.
        """
        if type(path) is str:
            tmp: set[str] = {path[2:] if path.startswith("./") else path}
            self.__fileList.add(tmp)
        elif isinstance(path, Iterable):
            tmp = set()
            for p in path:
                if isinstance(p, str):
                    tmp.add(p[2:] if p.startswith("./") else p)

            self.__fileList.add(tmp)
        else:
            raise TypeError("path must be a string or an iterable of strings")

    def add_dir(self, path: str | Iterable[str]) -> None:
        """Add a path or paths to the directory List.

        Args:
            path: path to a directory or an iterable with pathnames.
        """
        if type(path) is str:
            tmp: set[str] = {path[2:] if path.startswith("./") and
                             len(path) > 2 else path}
            self.__dirList.add(tmp)
        elif isinstance(path, Iterable):
            tmp = set()
            for p in path:
                if isinstance(p, str):
                    tmp.add(p[2:] if p.startswith("./") and len(p) > 2 else p)

            self.__dirList.add(tmp)
        else:
            raise TypeError("path must be a string or an iterable of strings")

    def drop_file(self, path: str | Iterable[str]) -> None:
        """Delete an entry or entries from the file List.

        Args:
            path: path to a file or an iterable with pathnames.
        """
        if type(path) is str:
            tmp: set[str] = {path[2:] if path.startswith("./") else path}
            self.__fileList.add(tmp)
        elif isinstance(path, Iterable):
            tmp = set()
            for p in path:
                if isinstance(p, str):
                    tmp.add(p[2:] if p.startswith("./") else p)

            self.__fileList.discard(tmp)

    def drop_dir(self, path: str | Iterable[str]) -> None:
        """Delete an entry or entries from the directory List.

        Args:
            path: a directory pathname or an iterable with pathnames.
        """
        if type(path) is str:
            tmp: set[str] = {path[2:] if path.startswith("./") and
                             len(path) > 2 else path}
            self.__dirList.add(tmp)
        elif isinstance(path, Iterable):
            tmp = set()
            for p in path:
                if isinstance(p, str):
                    tmp.add(p[2:] if p.startswith("./") and len(p) > 2 else p)

            self.__dirList.discard(tmp)

    def in_files(self, path: str) -> str | None:
        """Return path if found in files List else None.

        Searches both the basename and the original path.

        Args:
            path: a pathname.

        Returns:
            a str of either the full path or basename if found else None.
        """
        if type(path) is str:
            if path.startswith("./"):
                path = path[2:]

            if path in self.__fileList:
                return path
            elif basename(path) in self.__fileList:
                return basename(path)

        return None

    def in_dirs(self, path: str) -> str | None:
        """Return path if found in directories List else None.

        Searches both the basename and the original path.

        Args:
            path: a pathname.

        Returns:
            a str of either the full path or basename if found else None.
        """
        if type(path) is str:
            if path.startswith("./") and len(path) > 2:
                path = path[2:]

            if path in self.__dirList:
                return path
            elif basename(path) in self.__dirList:
                return basename(path)

        return None

    def clear_files(self) -> None:
        """Delete all entries in files List."""
        self.__fileList.clear()

    def clear_dirs(self) -> None:
        """Delete all entries in directories List."""
        self.__dirList.clear()

    def clear_all(self) -> None:
        """Clear both files and directories Lists."""
        self.clear_dirs()
        self.clear_files()
