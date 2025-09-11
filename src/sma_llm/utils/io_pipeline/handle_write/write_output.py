from abc import ABC, abstractmethod

class WriteOutput(ABC):
    @staticmethod
    @abstractmethod
    def process_output(string: str) -> None:
        return