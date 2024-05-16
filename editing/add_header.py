#!/usr/bin/env python
"""Module for add_header."""
from contextlib import AbstractContextManager
import os
from os.path import basename, splitext
import shutil
import stat
from tempfile import NamedTemporaryFile
from types import TracebackType


class Escape(AbstractContextManager):
    """Context manager wrapper for 'breaking' out of context managers."""

    class Break(Exception):
        """Break out of the with statement."""

    def __init__(self, context: AbstractContextManager):
        """Initialise with the context manager."""
        self.context = context

    def __enter__(self):
        """Enter with wrapped context manager."""
        return self.context.__enter__()

    def __exit__(
        self, exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> bool | None:
        """Break out or exit with wrapped context manager."""
        if exc_type == self.Break:
            return True

        return self.context.__exit__(exc_type, exc_value, traceback)


def add_header(
    file_path: str | bytes | os.PathLike,
    shebang: str = "#!/usr/bin/env python\n",
    docstring: str | None = None,
) -> None:
    """Add a shebang and a simple module docstring."""
    if not isinstance(shebang, str):
        raise TypeError("shebang must be a string")

    shebang = "".join([shebang.strip(), "\n"])
    if not shebang.startswith("#!"):
        raise ValueError(
            "shebang must be a valid unix shebang."
            "For example: '#!/usr/bin/env python\\n'"
        )

    if docstring is not None and not isinstance(docstring, str):
        raise TypeError("docstring must be a string or None")

    if isinstance(docstring, str) and docstring:
        docstring = docstring.strip()
        if not docstring.startswith(("'''", '"""')):
            docstring = "".join(['"""', docstring])

        if not docstring.endswith(("'''", '"""')):
            docstring = "".join([docstring, '"""'])

    try:
        with (
            open(file_path, "r", encoding="utf-8") as file,
            NamedTemporaryFile(
                "wb", prefix=f"{basename(file.name)}.", delete=False,
            ) as tmpf
        ):
            line1: str = file.readline()
            if line1.startswith("#!"):
                raise Escape.Break

            docline: str = line1.lstrip()
            while not docline:
                docline = file.readline().lstrip()

            if docline.startswith(("'''", '"""')):
                docline = ""
            else:
                if docstring is not None:
                    docline = "".join([docstring, "\n"])
                else:
                    docline = (
                        '"""Module for '
                        f'{splitext(basename(file.name))[0]}."""\n'
                    )

            file.seek(0)
            tmpf.write(
                bytes(f"{shebang}{docline}{file.read()}", encoding="utf-8"))
            tmpf.flush()

        shutil.copystat(file.name, tmpf.file.name)
    except Exception as err:
        if os.path.exists(tmpf.file.name):
            os.remove(tmpf.file.name)

        if not isinstance(err, Escape.Break):
            raise err

    if os.path.exists(tmpf.file.name):
        os.chmod(
            tmpf.file.name, os.stat(tmpf.file.name).st_mode | stat.S_IXUSR
        )
        shutil.move(tmpf.file.name, file.name)
    else:
        os.chmod(file.name, os.stat(file.name).st_mode | stat.S_IXUSR)


if __name__ == "__main__":
    add_header("test.py")
