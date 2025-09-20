"""Same Network class, but adapted for benchmarking
Note: look at perf_counter() calls to see the exact times registered
"""

from mlc_llm import MLCEngine # type: ignore
from sma_llm.utils.memory import Memory
from time import perf_counter
from .model_interface import ModelInterface

class MLCLLM(ModelInterface):
    model = None # the model itself
    engine = None
    instance = None
    _upload_time = None

    # Singletone: the instance exists only when the model is on RAM
    def __new__(cls):
        if cls.instance is None:
            cls.model =  "./sma_llm/models/mlc_llm/model"
            try:
                upload_start = perf_counter()
                cls.engine = MLCEngine(cls.model)
                upload_done = perf_counter()
                cls._upload_time = upload_done - upload_start
            except Exception as e:
                print(f"{e}")
                return

            cls.instance = super(MLCLLM, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
       pass

    # Free memory after use
    def terminate(self) -> None:
        if self.engine is not None:
            self.engine = None
            self.instance = None
    
    def generate(self, memory: Memory) -> str:
        # https://llm.mlc.ai/docs/deploy/python_engine.html
        start = perf_counter()
        response = self.engine.chat.completions.create(
            messages=memory,
            model=self.model,
            stream=False,
        )
        end = perf_counter()     
        return (response, end - start)
    
    def generate_TTFT(self, memory: Memory) -> str:
        start_TTFT = perf_counter()
        for response in self.engine.chat.completions.create(
            messages = memory.get_memory(self),
            model = self.model,
            stream = True
        ):
            for choice in response.choices:
                end_TTFT = perf_counter()
                return end_TTFT - start_TTFT

    @property
    @staticmethod
    def type() -> str:
        return "mlc-llm"
    
    @property
    def upload_time(self) -> float:
        return self._upload_time