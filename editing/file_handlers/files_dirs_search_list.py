#!/usr/bin/python3
"""Module for filesysytem_blacklist_whitelist."""

from collections.abc import Iterable, Iterator
from contextlib import suppress
import fnmatch
from os.path import basename
import re

from file_handlers.static_set import StaticSet
from text.string import strip_path


class FSSearchList:
    """Search list manager for files and directories."""

    def __init__(self, files: str | Iterable[str] | None = None,
                 directories: str | Iterable[str] | None = None):
        """Initialise a files List and a directories List.

        Args:
            files: an iterable of strings representing path_patterns to files.
            directories: an iterable of strings representing path_patterns to
                directories.
        """
        self.files = files  # type: ignore
        self.directories = directories  # type: ignore

    @property
    def files(self) -> Iterator[str]:
        """An iterator of all file patterns."""
        return self.__fileList.items

    @files.setter
    def files(self, files: str | Iterable[str] | None) -> None:
        """Create a StaticSet for files.

        Any items in the iterable that are not strings will be ignored.

        Args:
            files: a string or an iterable of strings or None.

        Raises:
            TypeError: files is not a string or an iterable of strings or None.
        """
        if files is not None and not isinstance(files, (str, Iterable)):
            raise TypeError(
                "files must be str or an Iterable of strings or None.")

        self.__fileList: StaticSet = StaticSet()
        if isinstance(files, str):
            self.__fileList = StaticSet(strip_path(files))
        elif isinstance(files, Iterable):
            for path_pattern in files:
                with suppress(TypeError):
                    self.__fileList.add(strip_path(path_pattern))

    @property
    def directories(self) -> Iterator[str]:
        """An iterator of all directory patterns."""
        return self.__dirList.items

    @directories.setter
    def directories(self, directories: str | Iterable[str] | None) -> None:
        """Create a StaticSet for directories.

        Any items in the iterable that are not strings will be ignored.

        Args:
            directories: a string or an iterable of strings or None.

        Raises:
            TypeError: directories is not a string or an iterable of strings or
                None.
        """
        if (
            directories is not None and
            not isinstance(directories, (str, Iterable))
        ):
            raise TypeError(
                "directories must be str or an Iterable of strings or None.")

        self.__dirList: StaticSet = StaticSet()
        if isinstance(directories, str):
            self.__dirList = StaticSet(strip_path(directories))
        elif isinstance(directories, Iterable):
            for path_pattern in directories:
                with suppress(TypeError):
                    self.__dirList.add(strip_path(path_pattern))

    def __repr__(self) -> str:
        """Return an official string representation of this instance."""
        return (f"{self.__class__.__name__}"
                f"({self.__fileList}, {self.__dirList})")

    def __contains__(self, path_pattern: str) -> bool:
        """Check if a path_pattern exists in either List.

        Args:
            path_pattern: Unix like filename patterns.
        """
        if isinstance(path_pattern, str):
            path_pattern = strip_path(path_pattern)
            return (
                (path_pattern in self.__fileList or
                 path_pattern in self.__dirList) or
                (basename(path_pattern) in self.__fileList or
                 basename(path_pattern) in self.__fileList)
            )

        return False

    def add_files(self, path_patterns: str | Iterable[str]) -> None:
        """Add a path_pattern or several path_patterns to the file List.

        Args:
            path_patterns: Unix like filename patterns.

        Raises:
            TypeError: path_patterns is not a string or an iterable of strings.
        """
        if isinstance(path_patterns, str):
            self.__fileList.add(strip_path(path_patterns))
        elif isinstance(path_patterns, Iterable):
            for p in path_patterns:
                with suppress(TypeError):
                    self.__fileList.add(strip_path(p))
        else:
            raise TypeError(
                "path_patterns must be a string or an iterable of strings")

    def add_dirs(self, path_patterns: str | Iterable[str]) -> None:
        """Add a path_pattern or several path_patterns to the directory List.

        Args:
            path_pattern: Unix like filename patterns.

        Raises:
            TypeError: path_patterns is not a string or an iterable of strings.
        """
        if isinstance(path_patterns, str):
            self.__dirList.add(strip_path(path_patterns))
        elif isinstance(path_patterns, Iterable):
            for p in path_patterns:
                with suppress(TypeError):
                    self.__dirList.add(strip_path(p))
        else:
            raise TypeError(
                "path_patterns must be a string or an iterable of strings")

    def drop_files(self, path_patterns: str | Iterable[str]) -> None:
        """Delete an entry or several entries from the file List.

        Args:
            path_patterns: Unix like filename patterns.

        Raises:
            TypeError: path_patterns is not a string or an iterable of strings.
        """
        if isinstance(path_patterns, str):
            self.__fileList.discard(strip_path(path_patterns))
        elif isinstance(path_patterns, Iterable):
            for p in path_patterns:
                with suppress(TypeError):
                    self.__fileList.discard(strip_path(p))
        else:
            raise TypeError(
                "path_patterns must be a string or an iterable of strings")

    def drop_dirs(self, path_patterns: str | Iterable[str]) -> None:
        """Delete an entry from the directory List.

        Args:
            path_patterns: Unix like filename patterns.

        Raises:
            TypeError: path_patterns is not a string or an iterable of strings.
        """
        if isinstance(path_patterns, str):
            self.__dirList.discard(strip_path(path_patterns))
        elif isinstance(path_patterns, Iterable):
            for p in path_patterns:
                with suppress(TypeError):
                    self.__fileList.discard(strip_path(p))
        else:
            raise TypeError(
                "path_patterns must be a string or an iterable of strings")

    def in_files(self, path_pattern: str) -> str | None:
        """Return path_pattern if found in files List else None.

        Searches both the basename and the original path_pattern.

        Args:
            path_pattern: Unix like filename pattern.

        Returns:
            a str of either the full path_pattern or basename if found else
                None.
        """
        if isinstance(path_pattern, str):
            path_pattern = strip_path(path_pattern)
            if path_pattern in self.__fileList:
                return path_pattern

            path_pattern = basename(path_pattern)
            if path_pattern in self.__fileList:
                return path_pattern

        return None

    def in_dirs(self, path_pattern: str) -> str | None:
        """Return path_pattern if found in directories List else None.

        Searches both the basename and the original path_pattern.

        Args:
            path_pattern: Unix like filename pattern.

        Returns:
            a str of either the full path_pattern or basename if found else
                None.
        """
        if isinstance(path_pattern, str):
            path_pattern = strip_path(path_pattern)
            if path_pattern in self.__fileList:
                return path_pattern

            path_pattern = basename(path_pattern)
            if path_pattern in self.__fileList:
                return path_pattern

        return None

    def clear_files(self) -> None:
        """Delete all entries in files List."""
        self.__fileList.clear()

    def clear_dirctories(self) -> None:
        """Delete all entries in directories List."""
        self.__dirList.clear()

    def match_file(self, path: str) -> bool:
        """Match to path path patterns in file List.

        Args:
            path: path to a file.

        Returns:
            True if match is found else False.

        Raises:
            TypeError: path is not a str.
        """
        if not isinstance(path, str):
            raise TypeError("path must be a str")

        matching_pattern: str = "|".join(
            [fnmatch.translate(pat) for pat in self.files])

        return bool(re.match(matching_pattern, path))

    def match_dir(self, path: str) -> bool:
        """Match to path path patterns in directory List.

        Args:
            path: path to a directory.

        Returns:
            True if match is found else False.

        Raises:
            TypeError: path is not a str.
        """
        if not isinstance(path, str):
            raise TypeError("path must be a str")

        matching_pattern: str = "|".join(
            [fnmatch.translate(pat) for pat in self.directories])

        return bool(re.match(matching_pattern, path))
