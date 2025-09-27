"""All classes are singletone to keep changing global vars."""
from abc import ABC, abstractmethod

class WriteOutput(ABC):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def display_output(string: str) -> None:
        return