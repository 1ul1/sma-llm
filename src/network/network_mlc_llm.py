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
        for completion in engine.chat.completions.create(
            messages = memory,
            model = self.model,
            stream = True
        ):
            pass
        pass




# https://llm.mlc.ai/docs/deploy/python_engine.html
# from mlc_llm import MLCEngine

# # Create engine
# model = "HF://mlc-ai/Llama-3-8B-Instruct-q4f16_1-MLC"
# engine = MLCEngine(model)

# # Run chat completion in OpenAI API.
# for response in engine.chat.completions.create(
#     messages=[{"role": "user", "content": "What is the meaning of life?"}],
#     model=model,
#     stream=True,
# ):
#     for choice in response.choices:
#         print(choice.delta.content, end="", flush=True)
# print("\n")

# engine.terminate()