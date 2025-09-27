from mlc_llm import MLCEngine
from threading import Event
from sma_llm.utils.network.network_interface import Network, TOGGLE
from sma_llm.utils.text_handler import TextHandler
from sma_llm.utils.io_pipeline import get_SHOW
from sma_llm.utils.memory import Memory

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
            try:
                cls.engine = MLCEngine(cls.model)
            except Exception as e:
                print(f"{e}")
                return

            cls.instance = super(MLCLLM, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        if any(var is None for var in ([
            self.config,
            self.max_position_embeddings, 
            self.eos_token_id
        ])):
            from sma_llm.utils.network.read_model_config import model_config
            self.config = model_config(self)
            self.max_position_embeddings = (
                self.config["model_config"]["rope_scaling"]["original_max_position_embeddings"]
            )
            self.eos_token_id = self.config["eos_token_id"][0]

        if self.text_handler is None:
            self.text_handler = TextHandler()

    # Free memory after use
    def terminate(self) -> None:
        if self.engine is not None:
            self.engine = None
            self.instance = None
    
    def generate(self, memory: Memory) -> str:
        answer = ""
        # get_SHOW().display_output("\nAssistant: ")
        for response in self.engine.chat.completions.create(
            messages = memory.get_memory(self),
            model = self.model,
            stream = True
        ):
            for choice in response.choices:
                if TOGGLE.is_set():
                    memory.forget()
                    # get_SHOW().display_output('\n')
                    return
                get_SHOW().display_output(choice.delta.content)
                answer += choice.delta.content
                # Stop after n sentences
                if (self.text_handler.stop(choice.delta.content)):
                    self.text_handler.sentence_counter = 0
                    break

        # get_SHOW().display_output('\nPress "ENTER" to continue.')

        # update the conversation's memory
        answer = TextHandler.spell_corrector(
            (TextHandler.post_process_text(answer))
        )
        memory.update_memory(answer)

        TOGGLE.set()
        # get_SHOW().display_output("")

        return answer
    
    @property
    def get_max_position_embeddings(self) -> int:
        self.max_position_embeddings

    @property
    def get_eos_token_id(self) -> int:
        self.eos_token_id