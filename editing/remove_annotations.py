#!/usr/bin/python3
"""Module for remove_annotations."""

import ast
import os
import shutil
from tempfile import NamedTemporaryFile

import autopep8  # type: ignore
from rich.progress import Progress

try:
    from editing.code_parsing.ast_edit import TypeHintsRemover
except ModuleNotFoundError:
    from sys import path
    from os.path import dirname, realpath
    path.append(dirname(dirname(realpath(__file__))))
    from editing.code_parsing.ast_edit import TypeHintsRemover
    del path, dirname, realpath

from editing.file_handlers.pyfile_tracker import PyFileData


def remove_annotations_ast(
        data: PyFileData, filename: str | None = None, file_progress: Progress | None = None
) -> None:
    """Remove type annotations from files.

    Args:
        filename: path to a python script file.
        data: a PyFileData object that can store the file's data.
        file_progress: a Progress tracker or None.
    """
    if filename is not None and not isinstance(filename, str):
        raise TypeError("filename must be a string or none")
    elif filename is not None:
        base: str = os.path.basename(filename)
        tmpf = None

    if isinstance(file_progress, Progress):
        file_task_id = file_progress.add_task("", total=5, step="Parsing...")

    try:
        with (
            open(filename, "rb") as file,
            NamedTemporaryFile(
                "wb", prefix=f"{base}.bak.", delete=False
            ) as tmpf
        ):
            data.tree = ast.parse(file.read(), file)
            if isinstance(file_progress, Progress):
                file_progress.update(
                    file_task_id, advance=1,
                    step="Modifying Abstract Syntax Tree..."
                )

            TypeHintsRemover().visit(data.tree)
            if isinstance(file_progress, Progress):
                file_progress.update(
                    file_task_id, advance=1, step="Generating script..."
                )

            tmpf.write(bytes(
                (f"#!/usr/bin/python3\n{ast.unparse(data.tree)}"),
                encoding="utf-8",
            ))
            tmpf.flush()

        if isinstance(file_progress, Progress):
            file_progress.update(
                file_task_id, advance=1, step="Formatting script..."
            )

        autopep8.fix_file(tmpf.file.name)
        if isinstance(file_progress, Progress):
            file_progress.update(
                file_task_id, advance=1, step="Replacing file..."
            )

        shutil.copystat(filename, tmpf.file.name)
    except Exception as err:
        if tmpf is not None and os.path.exists(tmpf.file.name):
            os.remove(tmpf.file.name)

        raise err

    shutil.move(tmpf.file.name, file.name)
    if isinstance(file_progress, Progress):
        file_progress.update(
            file_task_id, advance=1, visible=False,
            step="[bold dark_green]Done",
        )
