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

from editing.file_handlers.pyfile import PyFileData


def remove_annotations_ast(
        data: PyFileData, file_path: str | bytes | os.PathLike | None = None,
        file_progress: Progress | None = None,
) -> None:
    f"""Remove type annotations from python scripts.

    This function will parse and remove type annotations from the Python
    script specified by data.filename or file_path. data.tree will be updated
    with the modified Abstract Syntax Tree.

    Args:
        data: a PyFileData object that can store the file's data.
        file_path: path to a python script file, if data.filename is None, the
            attribute will be intatiated with file_path.
        file_progress: a Progress tracker, a task will be added and advanced
            as steps are completed, which shall be indicated by a steps field.

    Raises:
        ValueError: both data.filename and file_path are None.
    """
    if not isinstance(data, PyFileData):
        raise TypeError(f"data must be an instance of {PyFileData}")

    if data.filename is None:
        if file_path is None:
            raise ValueError("No file path has been provided.")

        data.filename = file_path  # type: ignore

    filename: str = data.filename  # type: ignore
    base: str = os.path.basename(filename)
    track_progress: bool = False
    if isinstance(file_progress, Progress):
        track_progress = True
        file_task_id = file_progress.add_task("", total=5, step="Parsing...")

    try:
        with (
            open(filename, "r") as file,
            NamedTemporaryFile("wb", prefix=f"{base}.", delete=False) as tmpf,
        ):
            data.tree = ast.parse(file.read(), filename)
            if track_progress:
                file_progress.update(  # type: ignore
                    file_task_id, advance=1,
                    step="Modifying Abstract Syntax Tree..."
                )

            TypeHintsRemover().visit(data.tree)
            if track_progress:
                file_progress.update(  # type: ignore
                    file_task_id, advance=1, step="Generating script..."
                )

            tmpf.write(bytes(
                (f"#!/usr/bin/python3\n{ast.unparse(data.tree)}"),
                encoding="utf-8",
            ))
            tmpf.flush()

        if track_progress:
            file_progress.update(  # type: ignore
                file_task_id, advance=1, step="Formatting script..."
            )

        autopep8.fix_file(tmpf.file.name)
        if track_progress:
            file_progress.update(  # type: ignore
                file_task_id, advance=1, step="Replacing file..."
            )

        shutil.copystat(filename, tmpf.file.name)
    except Exception as err:
        if os.path.exists(tmpf.file.name):
            os.remove(tmpf.file.name)

        raise err

    shutil.move(tmpf.file.name, file.name)
    if track_progress:
        file_progress.update(  # type: ignore
            file_task_id, advance=1, visible=False,
            step="[bold dark_green]Done",
        )


if __name__ == "__main__":
    remove_annotations_ast(PyFileData("test.py"))
