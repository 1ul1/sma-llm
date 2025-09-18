from abc import ABC, abstractmethod

class WriteOutput(ABC):
    @staticmethod
    @abstractmethod
    def display_output(string: str) -> None:
        return