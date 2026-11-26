
from typer import Typer
import sys
import os


from .control import ControlProject
from .tenant import TenantProject

if not os.environ.get("FROM_CLI"):
    print("You need to run this script using the dedicated entrypoint!")
    exit(0)

executor = sys.argv.pop(1)

class CLI(Typer):
    def __init__(self):
        super().__init__(name="repo")
        self.control = ControlProject()
        self.tenant = TenantProject()



control = ControlProject()


if __name__ == "__main__":
    CLI()(prog_name="repo")
