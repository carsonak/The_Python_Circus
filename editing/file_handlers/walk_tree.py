#!/usr/bin/env python
"""Module for walk_tree."""
from collections.abc import Iterator
from itertools import zip_longest
import os
import re

from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
from editing.text.string import strip_path


def walk_tree(
    start: str, pattern: str | None = None,
    whitelist: FileSystemBWlist | None = None,
    blacklist: FileSystemBWlist | None = None,
    max_depth: int = -1,
) -> Iterator[tuple[str, list[str], list[str]]]:
    """Genarate the directory tree of the given directory.

    This is a directory tree generator that behaves similar to os.walk()
    except it can prune directories according to a depth, filter out
    files/directories according to a blacklist or search only for specific
    files/directories according to a whitelist.

    Args:
        start: a path to a directory.
        max_depth: an int indicating how many levels to descend while
            searching for files. A negative int means a full depth search,
            a positive int n means upto n levels deep, with 0 being the
            start directory.
        pattern:
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
            pattern is not a string.
            maxdepth is not an int.
            whitelist is not None or an instance of FileSystemBWlist.
            blacklist is not None or an instance of FileSystemBWlist.
    """
    if type(start) is not str:
        raise TypeError("start must be a string")

    if pattern is not None and not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    if (
        whitelist is not None and
        not isinstance(whitelist, FileSystemBWlist)
    ):
        raise TypeError(
            "whitelist must be None or an instance of FileSystemBWlist"
        )

    if (
        blacklist is not None and
        not isinstance(blacklist, FileSystemBWlist)
    ):
        raise TypeError(
            "blacklist must be None or an instance of FileSystemBWlist"
        )

    if type(max_depth) is not int:
        raise TypeError("max_depth must be an int")

    start = strip_path(start)
    base_depth: int = start.count(os.sep)
    pat_obj: re.Pattern | None = re.compile(pattern) if pattern else None
    for root, dirnames, filenames in os.walk(start):
        matched_files: set[str] = set()
        matched_dirs: set[str] = set()
        for dir, file in zip_longest(dirnames, filenames):
            if dir is not None:
                rel_dirname: str = os.sep.join((root, dir))
                if pat_obj is not None and re.match(pat_obj, rel_dirname):
                    matched_dirs.add(dir)

                if (
                    (whitelist and whitelist.in_dirs(rel_dirname)) or
                    (blacklist and not blacklist.in_dirs(rel_dirname))
                ):
                    matched_dirs.add(dir)

            if file is not None:
                rel_filename: str = os.sep.join((root, file))
                if pat_obj is not None and re.match(pat_obj, rel_filename):
                    matched_files.add(file)

                if (
                    (whitelist and not whitelist.in_files(rel_filename)) or
                    (blacklist and blacklist.in_files(rel_filename))
                ):
                    matched_files.add(file)

        dirnames = list(matched_dirs)
        filenames = list(matched_files)
        yield root, dirnames, filenames
        current_depth: int = root.count(os.sep) - base_depth
        if 0 <= max_depth <= current_depth:
            del dirnames[:]
