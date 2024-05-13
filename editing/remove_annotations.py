#!/usr/bin/python3
"""Module for remove_annotations."""

import ast
# import json
import os
import shutil
import sys
from tempfile import NamedTemporaryFile

import autopep8  # type: ignore
from rich import box
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
)

try:
    from editing.code_parsing.ast_edit import TypeHintsRemover
except ModuleNotFoundError:
    from sys import path
    from os.path import realpath, dirname
    path.append(dirname(dirname(realpath(__file__))))
    from editing.code_parsing.ast_edit import TypeHintsRemover
    del path, realpath, dirname

from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
from editing.file_handlers.pyfile_tracker import PyFileData, PyFileTracker
# from editing.code_parsing.regex_edit import PyRegexEdit


class FancyProgressBars():
    """Rich progress bars."""

    def __init__(self) -> None:
        """Initialise progress trackers."""
        self.current_file_progress: Progress = Progress(
            TimeElapsedColumn(),
            TextColumn("[bold royal_blue1]{task.description}"),
            TextColumn("[bold]{task.fields[file]}"),
        )

        self.file_progress: Progress = Progress(
            SpinnerColumn("dots", style="pale_turquoise1"),
            TimeElapsedColumn(),
            BarColumn(),
            TextColumn("[bold]({task.completed} of {task.total})"),
            TextColumn("[bold cyan2]{task.fields[step]}"),
            transient=True,
        )

        self.overall_progress: Progress = Progress(
            TimeElapsedColumn(),
            TextColumn("[bold deep_sky_blue3]{task.description}"),
            SpinnerColumn("dots2", style="pale_turquoise1"),
            BarColumn(),
            TextColumn(" [bold]{task.completed} of {task.total}"),
        )


def ast_annotation_removal(
        filename: str, data: PyFileData, file_progress: Progress | None = None
) -> None:
    """Remove type annotations from files.

    Args:
        filename: path to a python script file.
        data: a PyFileData object that can store the file's data.
        file_progress: a Progress tracker or None.
    """
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
            data.tree = ast.parse(file.read(), filename)
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


def main(argv: list[str]) -> None:
    """Entry point.

    Args:
        argv: command line args
    """
    # Instantiate a file tracker
    files: set[str] = set()
    dir: str = "./env_arcade/arcade"
    wl: FileSystemBWlist | None = None
    bl: FileSystemBWlist | None = FileSystemBWlist(
        {".git", "__pycache__", ".mypy_cache", ".pytest_cache"})
    depth: int = -1
    tracker: PyFileTracker = PyFileTracker(
        files, dir, depth, blacklist=bl, whitelist=wl)

    p: FancyProgressBars = FancyProgressBars()
    progress_group: Group = Group(
        Panel(
            Group(p.current_file_progress, p.file_progress),
            box=box.SIMPLE, expand=False, padding=0,
        ),
        p.overall_progress,
    )
    overall_taskid = p.overall_progress.add_task(
        "Processing", total=len(tracker.pyfiles)
    )
    with Live(progress_group, vertical_overflow="visible"):
        for file, data in tracker.pyfiles.items():
            if not os.stat(file).st_size:
                continue

            task_id = p.current_file_progress.add_task(
                description="Editing...", file=file)

            ast_annotation_removal(file, data, p.file_progress)

            p.current_file_progress.stop_task(task_id)
            p.current_file_progress.update(
                task_id, description="[dark_green]Finished")
            p.overall_progress.update(overall_taskid, advance=1)

        p.overall_progress.stop_task(overall_taskid)
        p.overall_progress.update(
            overall_taskid, description="[bold green]Completed")


if __name__ == "__main__":
    main(sys.argv)


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
