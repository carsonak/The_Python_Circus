#!/usr/bin/python3
"""Module for remove_annotations."""

import ast
import json
import mmap
import os
from shutil import move
from tempfile import NamedTemporaryFile

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
    tracker.whitelist = FileSystemBWlist(("./editing/file_handlers/pyfile_tracker.py",))
    tracker.directory = "./editing/"
    # Generate edited ASTs for the files
    for filename in tracker.py_files:
        file_size: int = os.stat(filename).st_size
        if not file_size:
            continue

        with open(filename, "rb") as file:
            with mmap.mmap(file.fileno(), file_size, access=mmap.ACCESS_READ) as mmfile:
                tracker[filename] = PyFileData(tree=ast.parse(mmfile, filename))

        new_tree: ast.AST = TypeHintsRemover().visit(tracker[filename].tree)
        if new_tree != tracker[filename].tree:
            tracker[filename].tree = new_tree
        else:
            continue

        # Parse the ASTs and update the files
        base: str = os.path.basename(filename)
        with NamedTemporaryFile("wb", prefix=f"{base}.bak.", delete=False) as tmp_file:
            with mmap.mmap(tmp_file.fileno(), file_size, access=mmap.ACCESS_WRITE) as mmtmp_file:
                mmtmp_file.write(bytes(ast.unparse(tracker[filename].tree), encoding="utf-8"))
                mmtmp_file.flush()

        move(tmp_file.file.name, base)

if __name__ == "__main__":
    main()
