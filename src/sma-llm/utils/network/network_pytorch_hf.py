from transformers import AutoModelForCausalLM as LLM, AutoTokenizer as Tokenizer # type: ignore
import torch #type: ignore
import os
from network_interface import Network
from text_handler import TextHandler

#huggingface/tokenizers: The current process just got forked, after parallelism has already been used.
#Disabling parallelism to avoid deadlocks...
#To disable this warning, you can either:
#	- Avoid using `tokenizers` before the fork if possible
#	- Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def downloadModel():
    model_id = "mistralai/Mistral-7B-v0.1"
    tokenizer = Tokenizer.from_pretrained(model_id)
    model = LLM.from_pretrained(model_id)
    tokenizer.save_pretrained("../model/tokenizer")
    model.save_pretrained("../model/myModel")
    print("Download Completed")
    return 0

class PyTorchTransformers(Network):
    model = None # the model itself = LLM.from_pretrained("../model")
    tokenizer = None # Tokenizer.from_pretrained("../model/tokenizer")
    eos_token_id = None
    max_position_embeddings = None
    mps_device = None
    instance = None

    # singletone, the instance exists only when model uploaded on RAM
    def __new__(cls):
        if cls.instance is None:
            cls.upload_model()
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init(self):
        pass

    @classmethod
    def upload_model(cls) -> None:
        cls.model =  LLM.from_pretrained("../model")
        cls.tokenizer = Tokenizer.from_pretrained("../model/tokenizer")
        cls.eos_token_id = cls.tokenizer.eos_token_id
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

    def generate(self, memory: str) -> str:
        answer = ""
        live_answer = ""
        memory = memory + "Assistant: "
        write_output.main("Assistant: ") #type: ignore

        with torch.no_grad():
            while True:
                answer += live_answer
                inputs = self.tokenizer(memory + answer, return_tensors = "pt")
                input_ids = inputs["input_ids"].to(self.mps_device)
                attention_mask = inputs["attention_mask"].to(self.mps_device)

                # live generation, max_new_tokens at a time
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
                    max_new_tokens = 2
                )
                live_answer = self.tokenizer.decode(output_ids[0][input_ids.size(1):], skip_special_tokens=True)
                live_answer = TextHandler.post_process_text(live_answer) #type: ignore
                write_output.main(live_answer) #type: ignore
                
                # STOP
                if (self.eos_token_id in (output_ids[0][input_ids.size(1):].tolist()) 
                    or TextHandler.stop(live_answer)):

                    TextHandler.sentence_counter = 0
                    # if (input_ids.size(1) >= 1500): 
                    #     lines = conversation.split("User:")
                    #     conversation = initialPrompt + lines[-1]
                    break
            #
        return answer

    @property
    def max_position_embeddings(self) -> int:
        pass