from typer import Typer
from typer.models import Default

from .laravel import LaravelBase
from .vue import VueBase


class BaseProject(Typer):
    def __init__(
        self,
        *,
        name: str | None = Default(None),
        vue: VueBase,
        laravel: LaravelBase,
        **kw,
    ):
        super().__init__(name=name, no_args_is_help=True, **kw)
        self.add_typer(vue)
        self.add_typer(laravel)
