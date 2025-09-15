from multiprocessing import Process
from threading import Thread, Event
from sma_llm.utils import READ, SHOW, Network, Memory

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

    # Recursive method instead of loop for open-ended conversation
    def converse(self) -> None:
        question = READ.process_input()
        if question == "q":
            return 
        self.memory.update_memory(question)

        # Note: Memory is updated only if the generation is completed
        generate_answer = Process(
            target = self.model.generate, name = "GenerateAnswer", args = (self.memory,)
        )
        generate_answer.start()
        input()
        generate_answer.terminate()
        generate_answer.join()

        self.converse()
