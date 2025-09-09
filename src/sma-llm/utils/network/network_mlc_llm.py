from mlc_llm import MLCEngine # type: ignore
from network_interface import Network

class MLCLLM(Network):
    model = None # the model itself
    engine = None
    max_position_embeddings = None # needed for receiving memory
    instance = None

    # Singletone: the instance exists only when the model is on RAM
    def __new__(cls):
        if cls.instance is None:
            cls.engine = MLCEngine(cls.model)
            cls.instance = super(MLCLLM, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        pass

    # Free memory after use
    def terminate(self) -> None:
        if self.engine is not None:
            self.engine = None
            self.instance = None
    
    def generate(self, memory: str) -> str:
        answer = ""
        write_output.main("Assistant: ") #type: ignore
        for response in self.engine.chat.completions.create(
            messages = memory,
            model = self.model,
            stream = True
        ):
            for choice in response.choices: #type: ignore
                write_output.main(choice.delta.content) #type: ignore
                answer += choice.delta.content #type: ignore
        write_output.main("\n") #type: ignore
        return answer
    
    @property
    def max_position_embeddings(self) -> int:
        pass