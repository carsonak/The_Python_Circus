#!/usr/bin/python3
"""Module for remove_annotations."""


from utilities.editing.file_handler.blackwhite_list import BlackWhitelist
from utilities.editing.file_handler.filesystem_bw_list import FileSystemBWlist
from utilities.editing.file_handler.pyfile_tracker import PyFileTracker
from utilities.editing.annotations.type_hints_remover import TypeHintsRemover


def main() -> None:
    """Entry point."""
    # Instantiate a black list
    # Instantiate a file tracker
    # Generate edited ASTs for the files
    # Parse the ASTs and update the files


if __name__ == "__main__":
    main()
