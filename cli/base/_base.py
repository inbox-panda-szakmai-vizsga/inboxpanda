
from pathlib import Path

from typing import TypedDict, Unpack
from typer import Typer

from typer.models import Default


class BaseTyper(Typer):
    def __init__(self, **kw):
        super().__init__(**kw, no_args_is_help=True)
Typer()


class ConsoleKwargs(TypedDict): ...


class LogKwargs(TypedDict): ...


class ProjectBase(BaseTyper):
    def __init__(self, *, name: str | None = Default(None)):
        self.name = name
        super().__init__(name=name)

    def console(self, child: "ComponentBase", message: str, **kwargs: Unpack[ConsoleKwargs]):
        print(f"[{child.folder.name or "N/A"}]")

    def log(self, child: "ComponentBase", message: str, **kwargs: Unpack[LogKwargs]):
        ...


class ComponentBase(BaseTyper):
    def __init__(self, *, name: str, parent: ProjectBase, folder: Path):
        self.parent = parent
        self.folder = folder
        super().__init__(name=name)

    def console(self, message: str, **kwargs: Unpack[ConsoleKwargs]):
        self.parent.console(self, message, **kwargs)

    def log(self, message: str, **kwargs: Unpack[LogKwargs]):
        self.parent.log(self, message, **kwargs)
