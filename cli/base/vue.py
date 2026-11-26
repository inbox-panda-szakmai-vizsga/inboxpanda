from pathlib import Path

from ._base import ComponentBase, ProjectBase


class VueBase(ComponentBase):
    def __init__(self, parent: ProjectBase, folder: Path) -> None:
        super().__init__(name="site", parent=parent, folder=folder)

        for k, v in self.__dict__:
            if not k.endswith("_command"):
                continue
            print(f"[{folder.name or "N/A-site"} |", type(v))

        self.command()(self.test)

    def test(self):
        print("asd")
