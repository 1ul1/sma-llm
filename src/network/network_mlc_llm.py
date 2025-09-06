from mlc_llm import MLCEngine # type: ignore
from network_interface import Network

class MLCLLM(Network):
    model = None # the model itself
    engine = None
    max_position_embeddings = None # for needed for receiving memory

    # Singletone: the instance exists only when the model is on RAM
    def __new__(cls):
        if cls.engine is None:
            cls.engine = MLCEngine(cls.model)
        return super(MLCLLM, cls).__new__(cls)
    
    def __init__(self):
        pass

    # Free memory after use
    def terminate(self):
        if self.engine is not None:
            self.engine.terminate()
            self.engine = None
    
    def generate(self, memory: str) -> str:
        answer = ""
        for completion in self.engine.chat.completions.create(
            messages = memory,
            model = self.model,
            stream = True
        ):
            for choices in response.choices: #type: ignore
                print(choice.delta.content, end="", flush=True) #type: ignore
                answer += choice.delta.content #type: ignore
        print("\n")
        return answer