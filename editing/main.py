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
        required=True,
    )

    remove_annotations: ArgumentParser = sub_parsers.add_parser(
        "remove-annotations", aliases=["remove-ast", "rm-ann", "rm-ast"],
    )
    remove_annotations.add_argument(
        "-f", "--files", action="extend", nargs="+",
        help=("List of space separated file paths. "
              "Supports Unix style shell wildcards."),
    )
    remove_annotations.add_argument(
        "-dir", "--directory", action="store", nargs="?", const=".",
        help=("Path to a Python project directory. "
              "Defaults to current directory."),
    )
    remove_annotations.add_argument(
        "--depth", action="store", type=int, default=-1,
        help=(
            "An int indicating how many subdirectory levels to descend into"
            "while searching for files.\n"
            "A negative int means a full depth search, "
            "a positive int n means upto n levels deep,\n"
            "with 0 being the start directory."
        ),
    )
    remove_annotations.add_argument(
        "--exclude_files", action="extend", nargs="+",
        help=("List of file path patterns to exclude from a search. "
              "Supports Unix style shell wildcards.")
    )
    remove_annotations.add_argument(
        "--exclude_dirs", action="extend", nargs="+",
        help=("List of directory path patterns to exclude from a search. "
              "Supports Unix style shell wildcards."),
    )
    remove_annotations.add_argument(
        "--include_files", action="extend", nargs="+",
        help=("List of file path patterns to be included in a search. "
              "Supports Unix style shell wildcards."),
    )
    remove_annotations.add_argument(
        "--include_dirs", action="extend", nargs="+",
        help=("List of directory path patterns to be included in a search. "
              "Supports Unix style shell wildcards."),
    )
    remove_annotations.add_argument(
        "-p", "--show_progress", action="store_true",
        help=("Toggles on the progress bars.")
    )
    remove_annotations.set_defaults(func=remove_annotations_ast)

    header: ArgumentParser = sub_parsers.add_parser("add-header")
    header.add_argument(
        "-f", "--files", action="extend", nargs="+",
        help=("List of space separated file paths. "
              "Supports Unix style shell wildcards."),
    )
    header.add_argument(
        "-dir", "--directory", action="store", nargs="?", const=".",
        help=("Path to a Python project directory. "
              "Defaults to current directory."),
    )

    header.set_defaults(func=add_header)

    args: argparse.Namespace = main_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
