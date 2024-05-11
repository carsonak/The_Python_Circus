#!/usr/bin/python3
"""Module for remove_annotations."""

import ast
# import json
from mmap import mmap, ACCESS_READ
import os
import shutil
from tempfile import NamedTemporaryFile

import autopep8
import rich

try:
    from editing.code_parsing.ast_edit import TypeHintsRemover
except ModuleNotFoundError:
    from sys import path
    from os.path import realpath, dirname
    path.append(dirname(dirname(realpath(__file__))))
    from editing.code_parsing.ast_edit import TypeHintsRemover
    del path, realpath, dirname

from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
from editing.file_handlers.pyfile_tracker import PyFileTracker
# from editing.code_parsing.regex_edit import PyRegexEdit


# def regex_annotation_removal() -> None:
#     """Remove type annotations via regexes."""
#     editor = PyRegexEdit(PyFileTracker(
#         ("/home/line/Github_Repositories/"
#          "The_Python_Circus/editing/code_parsing/test_re.py",)))
#     # i.sub()
#     captured: dict[str, dict[str, list[str]]] | None =
# editor.capturesdict_files()
#     clean_dict: dict[str, dict[str, list[str]]] = {}
#     if captured:
#         for file_name, captures in captured.items():
#             clean_dict[file_name] = {}
#             for group, lst in captures.items():
#                 if (group == "return" or group == "arg_var" or
#                     group == "directive" or group == "import"):
#                     clean_dict[file_name][group] = lst

#     with open("matched_groups.json", "w", encoding="utf-8") as file:
#         json.dump(clean_dict, file, indent="\t")

def ast_annotation_removal(tracker: PyFileTracker) -> None:
    """Remove type annotations from files."""
    print("Processing files...")

    for filename in tracker.py_files:
        if not os.stat(filename).st_size:
            continue

        base: str = os.path.basename(filename)
        with (open(filename, "rb") as file,
              mmap(file.fileno(), 0, access=ACCESS_READ) as mmfile,
              NamedTemporaryFile("wb", prefix=f"{base}.bak.",
                                 delete=False) as tmpf
              ):
            # Generate AST for the file
            print(f"Building Abstract Syntax Trees for: {filename}")

            tree: ast.Module = ast.parse(mmfile, filename)
            tracker[filename].tree = tree
            # Parse the AST, removing type annotations
            tree = TypeHintsRemover().visit(tree)
            # Write to a temporary file
            print("Generating source code...")

            tmpf.write(bytes(f"#!/usr/bin/python3\n{ast.unparse(tree)}",
                             encoding="utf-8"))
            tmpf.flush()

        # Clean up code with a formatter
        print("Tidying up...", end="")

        autopep8.fix_file(
            tmpf.file.name, autopep8._get_options({"in_place": True}, False))
        # Copy over metadata
        shutil.copystat(filename, tmpf.file.name)
        # Replace original file
        shutil.move(tmpf.file.name, filename)

        print("Done")


def main() -> None:
    """Entry point."""
    # Instantiate a file tracker
    files: set[str] = {""}
    dir: str = "."
    wl: FileSystemBWlist | None = None
    bl: FileSystemBWlist | None = FileSystemBWlist(
        {"editing/code_parsing/test_re.py"})
    depth: int = -1
    tracker: PyFileTracker = PyFileTracker(dir, depth, bl, wl)
    ast_annotation_removal(tracker)


if __name__ == "__main__":
    main()
