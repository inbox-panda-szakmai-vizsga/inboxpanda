import os
from pathlib import Path

from base.project import BaseProject
from cli.base.laravel import LaravelBase
from cli.base.vue import VueBase


class ControlProject(BaseProject):
    def __init__(self, **kw):
        cwd = Path(os.getcwd())

        self.vue = VueBase(parent=self, folder=cwd / "control-site")
        self.laravel = LaravelBase(parent=self, folder=cwd / "control-plane")
        super().__init__(name="control", vue=self.vue, laravel=self.laravel, **kw)