#!/usr/bin/env python
"""Module for file_tracker."""


from collections.abc import Iterable
import os
from sys import stderr
from types import MappingProxyType
from typing import Union

from file_handlers.file_data import FileData
from file_handlers.file_system_search_list import FSSearchList
from file_handlers.walk_directory import walk_directory
from text.string import strip_path


class FileTracker:
    """A data tracker for files."""

    def __init__(
        self,
        files: Union[
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
            files: a path to a file or an Iterable of file paths.
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
        self.files = files  # type: ignore
        self._pfmap: MappingProxyType[str, FileData] = MappingProxyType(
            self.__files)
        self.depth = max_descent
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.pattern = pattern
        self.directory = directory  # type: ignore

    @property
    def files(self) -> MappingProxyType[str, FileData]:
        """A mapping proxy of the files and their data."""
        return self._pfmap

    @files.setter
    def files(
            self,
            files: Union[
                Iterable[str | bytes | os.PathLike], str, bytes, os.PathLike
            ],
    ) -> None:
        """Initialise files.

        Initialises a new mapping of filenames to instances of FileData.
        If an iterable is provided, any objects in it that raise a TypeError
        when called with os.fspath(), or that cannot be validated as Python
        scripts via their extensions or shebangs will be skipped and .

        Updates to self.directory will not remove any files already stored.

        Args:
            files: a path to a file or an Iterable of file paths.

        Raises:
            TypeError: files is neither an instance of os.PathLike,
                str or bytes nor an iterable of the same.
        """
        self.__files: dict[str, FileData] = {}
        if isinstance(files, (str, bytes, os.PathLike)):
            temp: FileData = FileData(files)
            if temp.filepath:
                temp.filepath = strip_path(temp.filepath)
                self.__files[temp.filepath] = temp

            return

        if not isinstance(files, Iterable):
            raise TypeError(
                f"files must be an instance of {str}, {bytes} or "
                f"{os.PathLike} objects or an Iterable of the same."
            )

        for file in files:
            try:
                temp = FileData(file)  # type: ignore
            except (TypeError, ValueError) as err:
                print(f"Skipping {str(file)}: Reason: {err}", file=stderr)
                continue

            self.__files[temp.filepath] = temp

    @property
    def directory(self) -> str:
        """Path to a directory with Python scripts."""
        return self.__workingdir

    @directory.setter
    def directory(self, directory: str | bytes | os.PathLike) -> None:
        """Initialise files with files in directory.

        The given directory will be searched for Python scripts with depth,
        whitelist and blacklist applied to the search. All Python scripts
        found will be added to files as a relative path from directory.
        The files will only be updated and not cleared.

        Args:
            directory: path to a directory with Python scripts.

        Raises:
            Any errors raised by os.fspath(directory).
        """
        # TODO(Andrew): check that encoding for bytes->str is utf-8
        directory = str(os.fspath(directory))
        self.__workingdir = strip_path(directory)
        for root, _dirs, files in walk_directory(
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
        return (f"{self.__class__.__name__}({self.files}, "
                f"{self.directory}, {self.depth}, {self.blacklist}, "
                f"{self.whitelist})")

    def __getitem__(self, filename: str) -> FileData:
        """Get file data for filename.

        filename should be as it was added. For example if a directory search
        was performed, filename will be the path to the file starting from the
        project directory name. If filename was added to files directly, the
        name should be as it was added.

        Args:
            filename: name of the file to look up.

        Returns:
            An instance of FileData.

        Raises:
            TypeError: filename is not a str type
            KeyError: filename does not exist in files.
        """
        if type(filename) is not str:
            raise TypeError("filename must be a str")

        return self.__files[strip_path(filename)]

    def __setitem__(self, filename: str, data: FileData) -> None:
        """Update a file in files with data.

        Filename should be as it was added. For example if a directory search
        was performed, filename will be the path to the file starting from the
        project directory name. If filename was added to files directly, the
        name should be as it was added.

        Args:
            filename: path of the file to be updated.
            data: an instance of FileData.

        Raises:
            TypeError: filename is not a str, data is not a FileData object.
        """
        if type(filename) is not str:
            raise TypeError("filename must be a string")

        if not isinstance(data, FileData):
            raise TypeError(f"data must be an instance of {FileData}")

        self.__files[strip_path(filename)] = data

    def __delitem__(self, filename: str) -> None:
        """Delete filename from mapping."""
        del self.__files[filename]

    def add_files(
        self,
        filepaths: Iterable[str | bytes | os.PathLike],
    ) -> None:
        """Update files with files in filepaths.

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

        temp: FileData
        for file in filepaths:
            try:
                temp = FileData(file)
            except (ValueError):
                continue

            if temp.filepath:
                self.__files.setdefault(
                    strip_path(temp.filepath), FileData()
                )

    def pop(self, filename: str) -> FileData | None:
        """Pop filename from mapping if found else None."""
        return self.__files.pop(filename, None)

    def clear(self) -> None:
        """Clear all items in files."""
        self.__files = {}
