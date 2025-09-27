from abc import ABC, abstractmethod

class ModelInterface(ABC):
    @property
    @abstractmethod
    def type(self) -> str:
        pass
    
    @property
    @abstractmethod
    def upload_time(self) -> float:
        pass

    @abstractmethod
    def generate_TTFT(self, memory) -> str:
        pass

    @abstractmethod
    def generate(self, memory) -> str:
        pass