#!/usr/bin/python3
"""Module for remove_annotations."""


from editing.code_parsing.ast_remove_annotation import TypeHintsRemover
from editing.file_handlers.blackwhite_list import BlackWhitelist
from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
from editing.file_handlers.pyfile_tracker import PyFileTracker


def main() -> None:
    """Entry point."""
    # Instantiate a black list
    # Instantiate a file tracker
    # Generate edited ASTs for the files
    # Parse the ASTs and update the files


if __name__ == "__main__":
    main()
