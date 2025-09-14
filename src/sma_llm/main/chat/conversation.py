from sma_llm.utils import *

class Conversation:
    def __init__(self, model: Network) -> None:
        self.memory = Memory()
        self.model = model
    
    def terminate(self) -> None:
        self.model = self.model.terminate()

    def set_model(self, model: Network) -> None:
        self.model = model

    @property
    def history(self) -> None:
        self.memory.get_memory()

    def converse(self):
        


        pass