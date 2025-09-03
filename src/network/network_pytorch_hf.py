from transformers import AutoModelForCausalLM as LLM, AutoTokenizer as Tokenizer # type: ignore
import torch #type: ignore
import os
from network_interface import Network

#huggingface/tokenizers: The current process just got forked, after parallelism has already been used.
#Disabling parallelism to avoid deadlocks...
#To disable this warning, you can either:
#	- Avoid using `tokenizers` before the fork if possible
#	- Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class PyTorchTransformers:
    pass

def downloadModel():
    # model_id = "mistralai/Mistral-7B-v0.1"
    model_id = "microsoft/phi-2"
    tokenizer = Tokenizer.from_pretrained(model_id)
    model = LLM.from_pretrained(model_id) # torch_dtype=torch.float16)
    tokenizer.save_pretrained("../model/tokenizer")
    model.save_pretrained("../model/myModel")
    print("Download Completed")
    return 0