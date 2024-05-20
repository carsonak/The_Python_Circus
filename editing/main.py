#!/usr/bin/python3
"""Module for main."""

import argparse
from argparse import ArgumentParser

from code_parsing.add_header import add_header
from code_parsing.remove_annotations_ast import remove_annotations_ast


def main() -> None:
    """Entry point."""
    main_parser: ArgumentParser = ArgumentParser(
        description="Programmatically modify Python code."
    )
    sub_parsers: argparse._SubParsersAction = main_parser.add_subparsers(
        required=True, metavar="<command>", title="commands"
    )

    remove_annotations: ArgumentParser = sub_parsers.add_parser(
        "remove-annotations", aliases=["remove-ast", "rm-ann", "rm-ast"],
        help=("remove as much type annotations from python scripts as "
              "possible without breaking the code."),
    )
    remove_annotations.add_argument(
        "-f", "--files", action="extend", nargs="+", metavar="file",
        help=("List of space separated file paths. "
              "Supports Unix style shell wildcards."),
    )
    remove_annotations.add_argument(
        "-dir", "--directory", action="store", nargs="?", const=".",
        metavar="dir",
        help=("Path to a Python project directory. "
              "Defaults to current directory."),
    )
    remove_annotations.add_argument(
        "--depth", action="store", type=int, default=-1, metavar="n",
        help=(
            "n is an int indicating how many subdirectory levels to descend "
            "into while searching for files. "
            "A negative int means a full depth search, "
            "a positive int n means upto n levels deep, "
            "with 0 being the start directory."
        ),
    )
    remove_annotations.add_argument(
        "--exclude-files", action="extend", nargs="+", metavar="file",
        help=("List of file path patterns to exclude from a search. "
              "Supports Unix style shell wildcards.")
    )
    remove_annotations.add_argument(
        "--exclude-dirs", action="extend", nargs="+", metavar="dir",
        help=("List of directory path patterns to exclude from a search. "
              "Supports Unix style shell wildcards."),
    )
    remove_annotations.add_argument(
        "--include-files", action="extend", nargs="+", metavar="file",
        help=("List of file path patterns to be included in a search. "
              "Supports Unix style shell wildcards."),
    )
    remove_annotations.add_argument(
        "--include-dirs", action="extend", nargs="+", metavar="dir",
        help=("List of directory path patterns to be included in a search. "
              "Supports Unix style shell wildcards."),
    )
    remove_annotations.add_argument(
        "-p", "--show-progress", action="store_true",
        help=("Toggles on the progress bars.")
    )
    remove_annotations.set_defaults(func=remove_annotations_ast)

    header: ArgumentParser = sub_parsers.add_parser(
        "add-header", aliases=["add-h"],
        help=("add a shebang, a module docstring if missing and "
              "execute permissions to a python script.")
    )
    header.add_argument(
        "-f", "--files", action="extend", nargs="+", metavar="file",
        help=("List of space separated file paths. "
              "Supports Unix style shell wildcards."),
    )
    header.add_argument(
        "-dir", "--directory", action="store", nargs="?", const=".",
        metavar="dir",
        help=("Path to a Python project directory. "
              "Defaults to current directory."),
    )
    header.set_defaults(func=add_header)

    args: argparse.Namespace = main_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
