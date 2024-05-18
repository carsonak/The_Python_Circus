#!/usr/bin/python3
"""Module for main."""

import argparse
from argparse import ArgumentParser

from code_parsing.remove_annotations_ast import remove_annotations_ast


def main() -> None:
    """Entry point."""
    main_parser: ArgumentParser = ArgumentParser(
        description="Programmatically modify Python code."
    )
    sub_parsers: argparse._SubParsersAction = main_parser.add_subparsers()

    remove_annotations: ArgumentParser = sub_parsers.add_parser(
        "remove-annotations", aliases=["remove-ast", "rm-ann", "rm-ast"]
    )
    remove_annotations.add_argument(
        "-f", "--files", action="extend", nargs="+",
        help=("List of space separated files. "
              "Supports Unix style shell wildcards."),
    )
    remove_annotations.add_argument(
        "-dir", "--directory", action="store", nargs="?", const=".",
        help=("Path to a Python project directory. "
              "Defaults to current directory."),
    )
    remove_annotations.add_argument(
        "--exclude-files", action="extend", nargs="+",
        help=("List of file path patterns to be excluded from a search.")
    )
    remove_annotations.add_argument(
        "--exclude-dirs", action="extend", nargs="+",
        help=("List of directory path patterns to exclude from a search.")
    )


if __name__ == "__main__":
    main()
