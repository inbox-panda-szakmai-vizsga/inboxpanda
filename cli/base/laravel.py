from pathlib import Path


from ._base import ComponentBase, ProjectBase

class LaravelBase(ComponentBase):
    def __init__(self, parent: ProjectBase, folder: Path) -> None:
            super().__init__(name="plane", parent=parent, folder=folder)