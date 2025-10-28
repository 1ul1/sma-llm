from abc import ABC, abstractmethod
from threading import Event

TOGGLE = Event()

class Network(ABC):
    @abstractmethod
    def terminate(self):
        pass

    @abstractmethod
    def generate(self, memory: str) -> str:
        pass

    @property
    @abstractmethod
    def get_context_window_size(self) -> int:
        pass

    @property
    @abstractmethod
    def get_eos_token_id(self) -> int:
        pass