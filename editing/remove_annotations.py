#!/usr/bin/python3
"""Module for remove_annotations."""

import ast
import json
from mmap import mmap
from pprint import pprint

try:
    from editing.code_parsing.ast_edit import TypeHintsRemover
except ModuleNotFoundError:
    from sys import path
    from os.path import abspath, dirname
    path.append(abspath(dirname(dirname(__file__))))
    from editing.code_parsing.ast_edit import TypeHintsRemover
    del path, abspath, dirname

from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
from editing.file_handlers.pyfile_tracker import PyFileTracker
from editing.file_handlers.pyfile_tracker import PyFileData
from editing.code_parsing.regex_edit import PyRegexEdit

def regex_annotation_removal() -> None:
    """Remove type annotations via regexes."""
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
    bl: FileSystemBWlist = FileSystemBWlist(("practice/pangram2.py", "practice/inf_vs_nan.py"))
    # Instantiate a file tracker
    tracker: PyFileTracker = PyFileTracker(directory="practice", blacklist=bl)
    # Generate edited ASTs for the files
    for filename in tracker.py_files:
        with open(filename, "r+") as file:
            with mmap(file.fileno(), 0) as mmfile:
                tracker[filename] = PyFileData(tree=ast.parse(mmfile, filename))

    # Parse the ASTs and update the files
    pprint(tracker.__dict__)


if __name__ == "__main__":
    main()
