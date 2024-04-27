#!/usr/bin/python3
"""Module for re_annotation_remover.

INCOMPLETE
"""

import regex
import os
import json


class PyRegexEdit:
    """Class for PyRegexEdit."""

    __annotations_pattern: str = r"""
    ## Return Value Type Annotations ##
    # Must be preceeded by ' ->'
    (?P<returns>\ ->
        (?P<annotation>\ #
            # Type name should be a valid Python name
            (?P<opt_unquoted_quoted>[[:alpha:]_]\w*|["'][[:upper:]_]\w+["'])
            # Followed by a '[', '|' or nothing
            (?P<opt_brace_slash_none>
                # If a brace match valid type annotations till the last ']'
                # in the sequence
                (?P<sqr_braces>\[ (?P&opt_unquoted_quoted)
                    # Option if comma,
                    (?P<opt_comma_brace_slash_loop>,
                        # Check if ' ...' other wise match another annotation
                        (?P<opt_elipses_annotation>\ \.{3} | (?P&annotation)) |
                    # if a brace match another brace sequence
                    (?P&sqr_braces) |
                    # if ' |' match another annotation
                    \ \|(?P&annotation))*
                \]) |
                # Else match '| ' and more valid type annotations
                \ \|(?P&annotation)
            )?
        )
    ): |
    ## Function Parameters and Variables Type Annotations ##
    # Skip through any dictionaries before trying to match an annotation
    (?:{[^\{\}]*} | (?P<params_vars>:(?P&annotation)) (?:[,\)] | \ =))
    """
    __directives_pattern: str = r"""\#(?P<directives>\ type:\ .+)$"""
    __imports_pattern: str = r"""
    (?P<imports>^\ *(?:import\ typing | from\ typing(?:\.\w+)*\ import\ \w+(?:,\ \w+)*))
    """

    def __init__(self, py_files: str | tuple[str, ...] = (),
                 folders: str | tuple[str, ...] = (),
                 flags: int = 0) -> None:
        """Initialise instance attributes."""
        self.__pattern_object: regex.Pattern | None = None
        self.__folders_dict: dict[str, tuple[str, ...]] = {}
        self.py_files: str | tuple[str, ...] = py_files  # type: ignore
        self.folders: str | tuple[str, ...] = folders  # type: ignore
        self.flags: int = flags

    @property
    def flags(self) -> int:
        """Return current set flags."""
        return self.__flags

    @flags.setter
    def flags(self, val: int) -> None:
        """Set flags."""
        if type(val) is not int:
            raise TypeError("flags must be an int")

        self.__flags: int = val

    @property
    def py_files(self) -> tuple[str, ...]:
        """Return files to be processed."""
        return self.__py_files

    @py_files.setter
    def py_files(self, py_files: str | tuple[str, ...]) -> None:
        """Check for .py file extensions and store the paths.

        Args:
            py_files [str | tuple[str, ...]]: It is either a path to a single
            python script or a tuple of multiple paths.
        """
        if type(py_files) is str:
            if os.path.splitext(py_files)[1] == ".py":
                self.__py_files = tuple([py_files])
            else:
                raise ValueError("filename must end with .py")
        elif type(py_files) is tuple:
            file_list: list[str] = []
            for f in py_files:
                if type(f) is str and os.path.splitext(f)[1] == ".py":
                    file_list.append(f)
            else:
                self.__py_files = tuple(file_list)
        else:
            raise TypeError("py_file must be a string or a tuple of strings")

        p_len: int = len(self.__py_files)
        if p_len:
            self.__folders_dict["00 unknown"] = self.__py_files
            print(f"Files in cache: {p_len}")

    @property
    def folders(self) -> tuple[str, ...]:
        """Return directories to be processed."""
        return self.__folders

    @folders.setter
    def folders(self, folders: str | tuple[str, ...]) -> None:
        """Extract Python files from directories and store the paths.

        Args:
            folders [str | tuple[str, ...]]: It is either a path to a single
            directory with python scripts or a tuple with multiple paths.
        """
        if type(folders) is str:
            self.__folders = tuple([folders])
        elif type(folders) is tuple:
            self.__folders = tuple([f for f in folders if type(f) is str])
        else:
            raise TypeError("folders must be a string or a tuple of strings.")

        for dirname in self.__folders:
            file_list: list[str] = []
            with os.scandir(dirname) as folder:
                for entry in folder:
                    ext: str = os.path.splitext(entry.path)[1]
                    if entry.is_file() and ext == ".py":
                        file_list.append(entry.path)
                else:
                    self.__folders_dict[dirname] = tuple(file_list)
                    self.py_files = tuple([*self.py_files, *file_list])

        d_len: int = len(self.__folders_dict)
        if d_len > 1 or "00 unknown" not in self.__folders_dict:
            print("Discovered {} files in {} directories.".format(
                len(self.py_files), d_len))

    def sub(self, regex_str: str = "", repl: str = "", flags: int = 0) -> None:
        """Substitute repl whenever regex_str matches the text in the file."""
        self.__pattern_object = self.compile(regex_str, flags)
        for filename in self.py_files:
            with open(filename, "r", encoding="utf-8") as file:
                contents: str = file.read()

            edited: str = self.__pattern_object.sub(repl, contents)
            if edited:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(edited)

    def compile(self, regex_str: str = "", flags: int = 0) -> regex.Pattern:
        """Compile a regex pattern."""
        if type(regex_str) is not str:
            raise TypeError("regex_str must be a string")

        if regex_str or not self.__pattern_object:
            if regex_str:
                compile_str: str = regex_str
                self.flags = flags
            else:
                compile_str = self.__annotations_pattern + r"|" +\
                    self.__directives_pattern + r"|" +\
                    self.__imports_pattern
                self.flags = int(regex.MULTILINE |
                                 regex.VERBOSE | regex.V1 | flags)

            self.__pattern_object = regex.compile(
                compile_str, flags=self.flags)

        return self.__pattern_object

    def capturesdict_files(self, regex_str: str = "",
                           flags: int = 0, file_time: float | None = None) -> dict[str, dict[str, list[str]]]:
        """Return a dict of filenames with a dict of named capturing groups
        and their list of captures.
        """
        self.flags = flags
        self.__pattern_object = self.compile(regex_str, self.flags)
        file_matches: dict[str, dict[str, list[str]]] = {}
        for filename in self.py_files:
            with open(filename, "r", encoding="utf-8") as file:
                contents: str = file.read()

            file_matches[filename] = {name: []
                                      for name in self.__pattern_object.groupindex.keys()}
            for match_obj in self.__pattern_object.finditer(
                    contents, overlapped=True, timeout=file_time):
                for group_name, items in match_obj.capturesdict().items():
                    file_matches[filename][group_name] += items

        return file_matches

    def reset(self) -> None:
        """Reset all instance attributes."""
        self.flags = 0
        self.py_files = ()
        self.folders = ()
        self.__pattern_object = None
        self.__folders_dict = {}


def main() -> None:
    """Entry Point."""
    dirs: tuple[str, ...] = ()
    i = PyRegexEdit(folders=("models", "tests/test_models",
                    "models/engine", "tests/test_models/test_engine"))
    # i.sub()
    clean_dict: dict[str, dict[str, list[str]]] = {}
    for file_name, captures in i.capturesdict_files().items():
        clean_dict[file_name] = {}
        for group, lst in captures.items():
            if group == "returns" or group == "params_vars" or group == "directives" or group == "imports":
                clean_dict[file_name][group] = lst

    with open("matched_groups.json", "w", encoding="utf-8") as file:
        json.dump(clean_dict, file, indent="\t")


if __name__ == "__main__":
    main()
