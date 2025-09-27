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
    def __new__(cls, engine = None):
        if cls.instance is None:
            cls.model =  "./sma_llm/models/mlc_llm/model"
            try:
                upload_start = perf_counter()
                if engine is None:
                    cls.engine = MLCEngine(cls.model)
                else:
                    cls.engine = engine
                upload_done = perf_counter()
                cls._upload_time = upload_done - upload_start
            except Exception as e:
                print(f"{e}")
                return

            cls.instance = super(MLCLLM, cls).__new__(cls)
        return cls.instance
    
    def __init__(self, _ = None):
       pass

    # Free memory after use
    def terminate(self) -> None:
        if self.engine is not None:
            self.engine = None
            self.instance = None
    
    def generate(self, memory: Memory) -> float:
        answer = ""
        start = perf_counter()
        for response in self.engine.chat.completions.create(
            messages=[{"role": "user", "content": "What is the meaning of life?"}],
            model = self.model,
            stream = True
        ):
            for choice in response.choices:
                answer = answer + choice.delta.content
        end = perf_counter()
        return(answer, end - start)
    
    def generate_TTFT(self, memory: Memory) -> float:
        start_TTFT = perf_counter()
        for response in self.engine.chat.completions.create(
            messages = memory.memory_as_dict,
            model = self.model,
            stream = True
        ):
            for choice in response.choices:
                end_TTFT = perf_counter()
                break
            break
        return end_TTFT - start_TTFT

    @property
    def type(self) -> str:
        return "mlc-llm"
    
    @property
    def upload_time(self) -> float:
        return self._upload_time