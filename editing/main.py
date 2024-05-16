#!/usr/bin/python3
"""Module for main."""

import os
import sys
import time

from rich import box
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
)

try:
    from editing.remove_annotations import remove_annotations_ast
except ModuleNotFoundError:
    from os.path import dirname, realpath
    sys.path.append(dirname(dirname(realpath(__file__))))
    from editing.remove_annotations import remove_annotations_ast
    del dirname, realpath

from editing.file_handlers.filesystem_bw_list import FileSystemBWlist
from editing.file_handlers.pyfile import PyFileTracker


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


def main(argv: list[str]) -> None:
    """Entry point.

    Args:
        argv: command line args
    """
    bl: FileSystemBWlist | None = FileSystemBWlist(
        {".git", "__pycache__", ".mypy_cache", ".pytest_cache"}
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
                description="Editing...", file=file)

            remove_annotations_ast(data, file, p.file_tasks_progress)

            p.file_overall_progess.stop_task(task_id_f)
            p.file_overall_progess.update(
                task_id_f, description="[dark_green]Finished")
            p.overall_progress.update(task_id_o, advance=1)

        p.overall_progress.stop_task(task_id_o)
        p.overall_progress.update(
            task_id_o, description="[bold green]Completed")
        time.sleep(0.2)


if __name__ == "__main__":
    main(sys.argv)
