#!/usr/bin/python3
"""Module for remove_annotations."""

import json

try:
    from editing.code_parsing.ast_remove_annotation import TypeHintsRemover
except ModuleNotFoundError:
    from sys import path
    path.append("/home/line/Github_Repositories/The_Python_Circus")
    from editing.code_parsing.ast_remove_annotation import TypeHintsRemover
    del path

from editing.file_handlers.blackwhite_list import BlackWhitelist
from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
from editing.file_handlers.pyfile_tracker import PyFileTracker
from editing.code_parsing.re_remove_annotation import PyRegexEdit

def regex_annotation_removal() -> None:
    """"""
    editor = PyRegexEdit(PyFileTracker(("/home/line/Github_Repositories/The_Python_Circus/test_re.py",)))
    # i.sub()
    captured: dict[str, dict[str, list[str]]] | None = editor.capturesdict_files()
    clean_dict: dict[str, dict[str, list[str]]] = {}
    if captured:
        for file_name, captures in captured.items():
            clean_dict[file_name] = {}
            for group, lst in captures.items():
                if (group == "return" or group == "arg_var" or
                    group == "directive" or group == "import"):
                    clean_dict[file_name][group] = lst

    with open("matched_groups.json", "w", encoding="utf-8") as file:
        json.dump(clean_dict, file, indent="\t")


def main() -> None:
    """Entry point."""
    # Instantiate a black list
    # Instantiate a file tracker
    # Generate edited ASTs for the files
    # Parse the ASTs and update the files
    a = PyFileTracker(("./editing/file_handlers/__init__.py", "./editing/file_handlers/__pycache__", "./editing/file_handlers/blackwhite_list.py",
                       "./editing/file_handlers/filesystem_bw_list.py", "./editing/file_handlers/pyfile_tracker.py"))

    for file in a.py_files:
        print(file)


if __name__ == "__main__":
    regex_annotation_removal()
