from threading import Thread, Event
from sma_llm.utils import READ, SHOW, Network, Memory, TOGGLE

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
    def history(self) -> None:
        self.memory.get_memory()
 
    # Recursive method instead of loop for open-ended conversation
    def converse(self) -> None:
        """
        The underlying method that keeps the chat itself going,
        generating processing input, generating answers, updating
        the conversation data so far.
        """
        question = READ.process_input()
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

        terminate_thread = Thread(target=terminate)
        TOGGLE.clear()
        terminate_thread.start()
        self.model.generate(self.memory)
        terminate_thread.join()
        self.converse()
