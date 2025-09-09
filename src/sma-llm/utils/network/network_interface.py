from abc import ABC, abstractmethod

class Network(ABC):
    @abstractmethod
    def terminate(self):
        pass

    @abstractmethod
    def generate(self, memory: str) -> str:
        pass

    @property
    @abstractmethod
    def max_position_embeddings(self) -> int:
        pass