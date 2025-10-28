"""Automated Tasks the model can perform.
single words starting with '-'
"""

from .task_scripts import *

def check_if_task(string: str) -> None:
    match string:
        case "-export":
            export()
        case "-benchmark":
            benchmark()
        case string if string.startswith("-retention"):
            try:
                retention(int(string.split("_")[-1]))
            except:
                invalid()
        case _:
            invalid()