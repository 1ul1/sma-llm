from mlc_llm import MLCEngine

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
            