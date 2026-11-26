from base.project import BaseProject
from cli.base.laravel import LaravelBase
from cli.base.vue import VueBase


class TenantProject(BaseProject):
    def __init__(self,**kw):
        self.vue = VueBase()
        self.laravel = LaravelBase()
        super().__init__(name="tenant", vue=vue, laravel=laravel, **kw)
        self.demo = VueBase(name="demo")
        self.add_typer(self.demo)