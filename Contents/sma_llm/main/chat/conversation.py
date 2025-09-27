from threading import Thread
from sma_llm.utils import get_READ, Network, Memory
from sma_llm.utils.network.network_interface import TOGGLE

class Conversation:
    """
    Class used to hold all the data for a conversation.
    Puts together all the methods and classes to simulate an open-ended conversation.
    Attributes:
        memory = It holds the context and the conversation so far
        model = the model running the completion for the Assistant's response
    """
    def __init__(self, model: Network) -> None:
        self.memory = Memory()
        self.model = model
    
    def terminate(self) -> None:
        self.model = self.model.terminate()

    def set_model(self, model: Network) -> None:
        self.model = model

    def set_memory(self, memory: Memory) -> None:
        self.memory = memory

    @property
    def history(self) -> str:
        return self.memory.get_memory()
 
    # Recursive method instead of loop for open-ended conversation
    def converse(self) -> None:
        """
        The underlying method that keeps the chat itself going,
        generating processing input, generating answers, updating
        the conversation data so far.
        """
        question = get_READ().process_input()
        if question == "Q":
            self.history
            return 
        self.memory.update_memory(question)

        def terminate() -> None:
            """
            if ENTER is pressed generation is interrupted
            """
            input()
            TOGGLE.set()

        terminate_thread = Thread(target=terminate, daemon=True)
        TOGGLE.clear()
        terminate_thread.start()
        self.model.generate(self.memory)
        terminate_thread.join()
        self.converse()

    def converse_UI(self, question: str) -> None:
        """Call the model to generate answer for the input.
        This method is called by the UI
        The termination of generation is handled by UI too"""
        self.memory.update_memory(question)
        self.model.generate(self.memory)