#!/usr/bin/python3
"""Module for re_annotation_remover."""

import regex
import os
import json

try:
    from editing.file_handlers.pyfile_tracker import PyFileTracker
except ModuleNotFoundError:
    from sys import path
    path.append("/home/line/Github_Repositories/The_Python_Circus")
    from editing.file_handlers.pyfile_tracker import PyFileTracker
    del path

class PyRegexEdit:
    """Search Python scripts with regexes.

    Attributes:
        __annotations_pattern: A regex pattern that tries to match Python type
            annotations.
        __directives_pattern: A regex pattern that tries to match type
            directives.
        __imports_pattern: A regex patten that tries to match imports from the
            typing module.
    """

    __annotations_pattern: str = r"""
    ## Return Value Type Annotations ##
    (?P<return>\ ->
        (?P<annotation> \ # space
            # Type name should be a valid Python name
            (?P<opt_unquoted_quoted>
                (?P<py_var> [[:alpha:]_]\w*?) | [\"\'] [[:upper:]_]\w+ [\'\"])
            (?P<opt_brace_slash_none>
                # If '[' recursively match annotations till the braces balance
                (?P<sqr_braces> \[ (?P&opt_unquoted_quoted)
                    # Recursion will be triggered after a '[', ',' or '|'
                    (?P<opt_comma_brace_slash_loop> ,
                        # If ', ...' break out of <opt_comma_brace_slash_loop>
                        # otherwise match another <annotation>.
                        (?P<opt_elipses_annotation> \ \.{3} | (?P&annotation)) |
                    # If '[' match another <sqr_braces>
                    (?P&sqr_braces) |
                    # if ' |' match another <annotation>
                    \ \|(?P&annotation))*
                # Else match a ']' and break out of <sqr_braces>
                \]) |
                # Else match '| ' and another <annotation>
                \ \|(?P&annotation)
            )?
        )
    ): |
    (?:
        # Skip dictionaries to avoid false positives
        # White space characters are limmited to 32
        (?P<dict> \{\s{0,32}
            # Recursively match elements till the braces balance, if present
            (?P<elements>
                # Possible key variants
                (?P<key>
                    (?P<str> (?:r|f)?
                        (?:
                            ["'].+?(?<!\\['"])["'] |
                            ["']{3} [\w\W]+? (?<!\\['"])["']{3}
                        )
                    ) |
                    (?&py_var) |
                    (?P<num> \d+?(?:\.\d+)?) |
                    (?P<set_tup_lst> [\[\{\(]
                        (?: [^\[\]\{\}\(\)]+? | (?&set_tup_lst) )*+
                    [\]\}\)] )
                ):\ # space
                # Possible value variants
                (?P<val>
                    (?&dict) | (?&str) | (?&py_var)(?&set_tup_lst)? |
                    (?&num) | (?&set_tup_lst)
                )
                # If ',' match another <elements>
                (?:, \s{1,32} (?&elements))?
            # Match the closing '}'
            )? ,? \s{0,32} \}
        ) |
        ## Function Parameters and Variables Type Annotations ##
        (?P<arg_var> :(?&annotation)) (?:[,\)] | \ =)
    )
    """
    __directives_pattern: str = r"""\#(?P<directive>\ type:\ .+)$"""
    __imports_pattern: str = r"""
    (?P<import>^[\ \t]*
        (?:import\ typing | from\ typing(?:\.\w+)*\ import\ \w+(?:,\ \w+)*)
    )
    """

    def __init__(self, file_tracker: PyFileTracker | None = None, flags: int = 0) -> None:
        """Initialise instance attributes."""
        self.__pattern_object: regex.Pattern | None = None
        self.flags: int = flags
        self.files = file_tracker

    @property
    def flags(self) -> int:
        """A bit mask of flags for the regex search engine."""
        return self.__flags

    @flags.setter
    def flags(self, val: int) -> None:
        """Set flags."""
        if type(val) is not int:
            raise TypeError("flags must be an int")

        self.__flags: int = val

    @property
    def files(self) -> PyFileTracker | None:
        """A python file tracker."""
        return self.__files

    @files.setter
    def files(self, file_tracker: PyFileTracker | None) -> None:
        """Initialise a python file tracker."""
        if file_tracker and not isinstance(file_tracker, PyFileTracker):
            raise TypeError("file_tracker must be an instance of PyFileTracker")

        self.__files = file_tracker

    # def sub(self, regex_str: str = "", repl: str = "", flags: int = 0) -> None:
    #     """Substitute repl whenever regex_str matches the text in the file."""
    #     if not self.files:
    #         return

    #     self.__pattern_object = self.compile(regex_str, flags)
    #     for filename in self.files.py_files:
    #         with open(filename, "r", encoding="utf-8") as file:
    #             contents: str = file.read()

    #         edited: str = self.__pattern_object.sub(repl, contents)
    #         if edited:
    #             with open(filename, "w", encoding="utf-8") as file:
    #                 file.write(edited)

    def compile(self, regex_str: str = "", flags: int = 0) -> regex.Pattern:
        """Compile a regex pattern."""
        if type(regex_str) is not str:
            raise TypeError("regex_str must be a string")

        if regex_str or not self.__pattern_object:
            if regex_str:
                compile_str: str = regex_str
                self.flags = flags
            else:
                compile_str = r"|".join([self.__annotations_pattern,
                                         self.__directives_pattern,
                                         self.__imports_pattern])
                self.flags = int(regex.MULTILINE | regex.VERBOSE |
                                 regex.V1 | flags)

            self.__pattern_object = regex.compile(compile_str,
                                                  flags=self.flags)

        return self.__pattern_object

    def capturesdict_files(self, regex_str: str = "",
                           flags: int = 0, file_time: float | None = None
                           ) -> dict[str, dict[str, list[str]]] | None:
        """Return a dict of filenames with a dict of named capturing groups
        and their list of captures.
        """
        if not self.files:
            return None

        self.flags = flags
        self.__pattern_object = self.compile(regex_str, self.flags)
        file_matches: dict[str, dict[str, list[str]]] = {}
        for filename in self.files.py_files:
            with open(filename, "r", encoding="utf-8") as file:
                self.files[filename].contents = file.read()

            file_matches[filename] = {name: [] for name in
                                      self.__pattern_object.groupindex.keys()}
            for match_obj in self.__pattern_object.finditer(
                    self.files[filename].contents, overlapped=True,
                    timeout=file_time):
                for group_name, items in match_obj.capturesdict().items():
                    file_matches[filename][group_name] += items

        return file_matches

    def reset(self) -> None:
        """Reset all instance attributes."""
        self.flags = 0
        self.files = None
        self.__pattern_object = None
