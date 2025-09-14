from abc import ABC, abstractmethod
from .print_output import PrintOutput

class WriteOutput(ABC):
    @staticmethod
    @abstractmethod
    def display_output(string: str) -> None:
        return
    
SHOW = PrintOutput()