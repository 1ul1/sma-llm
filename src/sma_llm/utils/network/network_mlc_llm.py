from mlc_llm import MLCEngine # type: ignore
from .network_interface import Network
from sma_llm.utils.text_handler import TextHandler
from sma_llm.utils.io_pipeline import SHOW
from .read_model_config import model_config

class MLCLLM(Network):
    model = None # the model itself
    engine = None
    config = None
    max_position_embeddings = None # needed for receiving memory
    eos_token_id = None # handle generation break
    instance = None
    text_handler = None

    # Singletone: the instance exists only when the model is on RAM
    def __new__(cls):
        if cls.instance is None:
            cls.model =  "./sma_llm/models/mlc_llm/model"
            cls.engine = MLCEngine(cls.model)
            cls.instance = super(MLCLLM, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        if any(var is None for var in ([
            self.config,
            self.max_position_embeddings, 
            self.eos_token_id
        ])):
            self.config = model_config(self)
            self.max_position_embeddings =  self.config["original_max_position_embeddings"]
            self.eos_token_id = self.config["eos_token_id"]

        if self.text_handler is None:
            self.text_handler = TextHandler()

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
                SHOW.display_output(choice.delta.content) #type: ignore
                answer += choice.delta.content #type: ignore
                # Stop after n sentences
                if (self.text_handler.stop(choice.delta.content)):
                    self.text_handler.sentence_counter = 0
                    break

        SHOW.display_output("\n") #type: ignore
        return TextHandler.post_process_text(answer)
    
    @property
    def max_position_embeddings(self) -> int:
        self.max_position_embeddings

    @property
    def eos_token_id(self) -> int:
        self.eos_token_id