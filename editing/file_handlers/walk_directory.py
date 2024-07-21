#!/usr/bin/env python
"""Module for walk_directory."""

from collections.abc import Iterator
from itertools import zip_longest
import os
import re

from file_handlers.file_system_search_list import FSSearchList


def walk_directory(
    root: str, pattern: str | None = None,
    whitelist: FSSearchList | None = None,
    blacklist: FSSearchList | None = None,
    max_depth: int = -1,
) -> Iterator[tuple[str, list[str], list[str]]]:
    """Recursively genarate components of a given directory.

    This generator function traverses a directory tree structure in a similar
    way to os.walk() but has a few extra options to control the output.

    Args:
        root: a path to a directory that will be used as the starting point
            of the walk.
        max_depth: an int indicating how many levels to descend while walking
            the directory tree. A negative int means a full depth search, a
            positive int n means upto n levels deep with 0 being the root
            directory.
        pattern: an optional unix like file pattern that can be used to match
            files and directories. Pattern takes lowest precedence over
            blacklist and whitelist.
        whitelist: an optional instance of FSSearchList that can be used to
            include files and directories in the results of the walk.
            Whitelist takes highest precedence over blacklist and pattern.
        blacklist: an optional instance of FSSearchList that can be used to
            exclude files and directories from the results of the walk.
            Blacklist has a lower precedence than whitelist and a higher
            precedence than pattern.

    Yields:
        A tuple of three items: dirpath, dirnames, filenames.
        `dirpath` is the path to the current directory.
        `dirnames` is a list of the names of the subdirectories in dirpath
        (including symlinks to directories, and excluding '.' and '..').
        `filenames` is a list of the names of the non-directory files in
        dirpath.
        The names in the lists are just names, with no path components.

    Raises:
        TypeError: root is not a string.
            pattern is not a string.
            maxdepth is not an int.
            whitelist is not None or an instance of FSSearchList.
            blacklist is not None or an instance of FSSearchList.
    """
    if type(root) is not str:
        raise TypeError("root must be a string")

    if pattern is not None and not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    if (
        whitelist is not None and
        not isinstance(whitelist, FSSearchList)
    ):
        raise TypeError(
            "whitelist must be None or an instance of FSSearchList"
        )

    if (
        blacklist is not None and
        not isinstance(blacklist, FSSearchList)
    ):
        raise TypeError(
            "blacklist must be None or an instance of FSSearchList"
        )

    if type(max_depth) is not int:
        raise TypeError("max_depth must be an int")

    root = os.path.realpath(root, strict=True)
    base_depth: int = root.count(os.sep)
    pat_obj: re.Pattern | None = re.compile(pattern) if pattern else None
    for base_dir, dirnames, filenames in os.walk(root):
        matched_files: set[str] = set()
        matched_dirs: set[str] = set()
        for directory, file in zip_longest(dirnames, filenames):
            if directory is not None:
                full_name: str = os.sep.join((base_dir, directory))

                if blacklist and not blacklist.match_dir(full_name):
                    if pat_obj is not None and re.search(pat_obj, full_name):
                        matched_dirs.add(directory)
                    else:
                        matched_dirs.add(directory)

                if whitelist and whitelist.match_dir(full_name):
                    matched_dirs.add(directory)

            if file is not None:
                full_name = os.sep.join((base_dir, file))
                if blacklist and blacklist.match_file(full_name):
                    if pat_obj is not None and re.search(pat_obj, full_name):
                        matched_files.add(file)
                    else:
                        matched_files.add(file)

                if whitelist and not whitelist.match_file(full_name):
                    matched_files.add(file)

        for d in dirnames[:]:
            if d not in matched_dirs:
                dirnames.remove(d)

        for f in filenames[:]:
            if f not in matched_files:
                filenames.remove(f)

        yield base_dir, dirnames, filenames
        current_depth: int = base_dir.count(os.sep) - base_depth
        if 0 <= max_depth <= current_depth:
            del dirnames[:]
