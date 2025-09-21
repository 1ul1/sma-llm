"""Same Network class, but adapted for benchmarking
Note: look at perf_counter() calls to see the exact times registered
"""

from transformers import AutoModelForCausalLM as LLM, AutoTokenizer as Tokenizer # type: ignore
import torch #type: ignore
import os
from time import perf_counter
from sma_llm.utils.memory import Memory
from .model_interface import ModelInterface

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class PyTorchTransformers(ModelInterface):
    model = None # the model itself = LLM.from_pretrained("../model")
    tokenizer = None # Tokenizer.from_pretrained("../model/tokenizer")
    mps_device = None
    instance = None
    _upload_time = None
    
    # singletone, the instance exists only when model uploaded on RAM
    def __new__(cls):
        if cls.instance is None:
            upload_start = perf_counter()
            cls.upload_model()
            upload_done = perf_counter()
            cls._upload_time = upload_done - upload_start
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    @classmethod
    def upload_model(cls) -> None:
        try:
            cls.model =  LLM.from_pretrained("./sma_llm/models/hf_pytorch/model")
            cls.tokenizer = Tokenizer.from_pretrained("./sma_llm/models/hf_pytorch/tokenizer")
        except Exception as e:
            print(f"{e}")
            return

        # Metal accelerated # https://developer.apple.com/metal/pytorch/
        if torch.backends.mps.is_available():
            cls.mps_device = torch.device("mps")
        else:
            cls.mps_device = torch.device("cpu") # already on cpu but doesn't break
            
        # "For models, .to(device) does modify in-place, so reassignment is optional"
        cls.model = cls.model.to(cls.mps_device)
        cls.model.eval()
        

    def terminate(self) -> None:
        self.model = None
        self.tokenizer = None
        self.instance = None

    def generate(self, memory: Memory) -> float:
        """Single generate() for benchmarking"""
        answer = ""
        context = memory.memory_as_string + "Assistant: "
        with torch.no_grad():
            inputs = self.tokenizer(context, return_tensors = "pt")
            input_ids = inputs["input_ids"].to(self.mps_device)
            attention_mask = inputs["attention_mask"].to(self.mps_device)

            start = perf_counter()

            output_ids = self.model.generate(
                input_ids = input_ids,
                attention_mask=attention_mask,
                pad_token_id = self.tokenizer.eos_token_id,
                eos_token_id = self.tokenizer.eos_token_id,
                do_sample = True,
                top_p = 0.5,
                temperature = 0.5,
                repetition_penalty = 1.9,
                no_repeat_ngram_size = 3,
                max_new_tokens = 500
            )
            answer = self.tokenizer.decode(output_ids[0][input_ids.size(1):], skip_special_tokens=True)
            end = perf_counter()
        print(answer)
        return (answer, end - start)
    
    def generate_TTFT(self, memory: Memory) -> float:
        """Single generate() for benchmarking"""
        answer = ""
        context = memory.memory_as_string + "Assistant: "
        with torch.no_grad():
            inputs = self.tokenizer(context, return_tensors = "pt")
            input_ids = inputs["input_ids"].to(self.mps_device)
            attention_mask = inputs["attention_mask"].to(self.mps_device)

            start_TTFT = perf_counter()

            output_ids = self.model.generate(
                input_ids = input_ids,
                attention_mask=attention_mask,
                pad_token_id = self.tokenizer.eos_token_id,
                eos_token_id = self.tokenizer.eos_token_id,
                do_sample = True,
                top_p = 0.5,
                temperature = 0.5,
                repetition_penalty = 1.9,
                no_repeat_ngram_size = 3,
                max_new_tokens = 1
            )
            answer = self.tokenizer.decode(output_ids[0][input_ids.size(1):], skip_special_tokens=True)
            end_TTFT = perf_counter()
        return end_TTFT - start_TTFT
    
    @property
    def type(self) -> str:
        return "pytorch-hf"
    
    @property
    def upload_time(self) -> float:
        return self._upload_time