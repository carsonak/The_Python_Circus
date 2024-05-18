#!/usr/bin/python3
"""Module for remove_annotations."""

import ast
import os
import shutil
from tempfile import NamedTemporaryFile
import time

import autopep8  # type: ignore
from rich import box
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
)

from code_parsing.ast_node_transformer import TypeHintsRemover
from file_handlers.files_dirs_search_list import FSSearchList
from file_handlers.pyfile import PyFileData, PyFileTracker


class FancyProgressBars():
    """Rich progress bars."""

    def __init__(self) -> None:
        """Initialise progress trackers."""
        self.file_overall_progess: Progress = Progress(
            TimeElapsedColumn(),
            TextColumn("[bold royal_blue1]{task.description}"),
            TextColumn("[bold]{task.fields[file]}"),
        )

        self.file_tasks_progress: Progress = Progress(
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
            TextColumn("[bold]step {task.completed} of {task.total}"),
        )


def parse_rm_ast(args) -> None:
    """Process parsed arguments."""
    bl: FSSearchList | None = FSSearchList(
        directories={"__pycache__"}
    )
    tracker: PyFileTracker = PyFileTracker(
        set(), "./env_arcade/arcade", blacklist=bl)

    p: FancyProgressBars = FancyProgressBars()
    progress_group: Group = Group(
        Panel(
            Group(p.file_overall_progess, p.file_tasks_progress),
            box=box.SIMPLE, expand=False, padding=0,
        ),
        p.overall_progress,
    )
    task_id_o = p.overall_progress.add_task(
        "Processing", total=len(tracker.pyfiles)
    )
    with Live(progress_group, vertical_overflow="visible"):
        for file, data in tracker.pyfiles.items():
            if not os.stat(file).st_size:
                continue

            task_id_f = p.file_overall_progess.add_task(
                description="...", file=file)

            remove_annotations_ast(data, file, p.file_tasks_progress)

            p.file_overall_progess.stop_task(task_id_f)
            p.file_overall_progess.update(
                task_id_f, description="[dark_green]Finished")
            p.overall_progress.update(task_id_o, advance=1)

        p.overall_progress.stop_task(task_id_o)
        p.overall_progress.update(
            task_id_o, description="[bold green]Completed")
        time.sleep(0.2)


def remove_annotations_ast(
        data: PyFileData, file_path: str | bytes | os.PathLike | None = None,
        file_progress: Progress | None = None,
) -> None:
    """Remove type annotations from python scripts.

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
