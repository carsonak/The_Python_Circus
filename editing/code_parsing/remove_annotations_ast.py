#!/usr/bin/python3
"""Module for remove_annotations."""

from argparse import Namespace
import ast
import os
import shutil
from tempfile import NamedTemporaryFile

import autopep8  # type: ignore
from rich import box
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn)

from code_parsing.ast_node_transformer import TypeHintsRemover
from file_handlers.file_data import FileData, Interpretor
from file_handlers.file_system_search_list import FSSearchList
from file_handlers.file_tracker import FileTracker


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


def process_remove_annotations_args(args: Namespace) -> None:
    """Process parsed arguments."""
    f: list[str] = []
    if args.files:
        f = args.files

    dir: str = ""
    if args.directory:
        dir = args.directory

    depth: int = -1
    if args.depth:
        depth = args.depth

    wl: FSSearchList = FSSearchList()
    if args.include_files:
        wl.files = args.include_files

    if args.include_dirs:
        wl.directories = args.include_dirs

    bl: FSSearchList = FSSearchList()
    if args.exclude_files:
        bl.files = args.exclude_files

    if args.exclude_dirs:
        bl.directories = args.exclude_dirs

    tracker: FileTracker = FileTracker(
        files=f, directory=dir, max_descent=depth, blacklist=bl,
        whitelist=wl,
    )

    for file, data in tracker.files.copy().items():
        if data.file_interpretor != Interpretor.PYTHON:
            del tracker[file]

    process_files(tracker, args.show_progress)


def process_files(tracker: FileTracker, show_progress: bool = False) -> None:
    """Iterate over discovered files and remove annotations."""
    p: FancyProgressBars = FancyProgressBars()
    progress_group: Group = Group(
        Panel(
            Group(p.file_overall_progess, p.file_tasks_progress),
            box=box.SIMPLE, expand=False, padding=0,
        ),
        p.overall_progress,
    )
    if show_progress:
        task_id_o = p.overall_progress.add_task(
            "Processing", total=len(tracker.files)
        )

    with Live(progress_group, vertical_overflow="visible"):
        for file, data in tracker.files.items():
            if not os.stat(file).st_size:
                continue

            if show_progress:
                task_id_f = p.file_overall_progess.add_task(
                    description="...", file=file)
                remove_annotations_ast(data, file, p.file_tasks_progress)
                p.file_overall_progess.stop_task(task_id_f)
                p.file_overall_progess.update(
                    task_id_f, description="[dark_green]Finished")
                p.overall_progress.update(task_id_o, advance=1)
            else:
                remove_annotations_ast(data, file)

        if show_progress:
            p.overall_progress.stop_task(task_id_o)
            p.overall_progress.update(
                task_id_o, description="[bold green]Completed")


def remove_annotations_ast(
        data: FileData, file_path: str | bytes | os.PathLike | None = None,
        file_progress: Progress | None = None,
) -> None:
    """Remove type annotations from python scripts.

    This function will parse and remove type annotations from the Python
    script specified by data.filepath or file_path. data.tree will be updated
    with the modified Abstract Syntax Tree.

    Args:
        data: a FileData object that can store the file's data.
        file_path: path to a python script file, if data.filepath is None, the
            attribute will be intatiated with file_path.
        file_progress: a Progress tracker, a task will be added and advanced
            as steps are completed, which shall be indicated by a steps field.

    Raises:
        ValueError: both data.filepath and file_path are None.
    """
    if not isinstance(data, FileData):
        raise TypeError(f"data must be an instance of {FileData}")

    if data.filepath is None:
        if file_path is None:
            raise ValueError("No file path has been provided.")

        data.filepath = file_path  # type: ignore

    filename: str = data.filepath  # type: ignore
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
