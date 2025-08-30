from mlc_llm import MLCEngine # type: ignore

class Network:
    model = None # the model itself
    engine = None

    # Singletone: the instance exists only when the model is on RAM
    def __new__(cls):
        if cls.engine is None:
            cls.engine = MLCEngine(cls.model)
        return super(Network, cls).__new__(cls)
    
    def __init__(self):
        pass

    # Free memory after use
    @classmethod
    def terminate(cls):
        if cls.engine is not None:
            cls.engine.terminate()
            cls.engine = None

    def generate_answer(memory: str) -> str:
        
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