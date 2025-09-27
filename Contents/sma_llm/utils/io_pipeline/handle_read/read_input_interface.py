from abc import ABC, abstractmethod

class ReadInput(ABC):
    
    @staticmethod
    @abstractmethod
    def process_input() -> str:
        pass