import json
from sma_llm.utils.network.network_interface import Network
from sma_llm.utils.network.network_mlc_llm import MLCLLM
from sma_llm.utils.network.network_pytorch_hf import PyTorchTransformers

def model_config(obj: Network) -> dict:
    if isinstance(obj, MLCLLM):
        path = "./sma_llm/models/mlc_llm/model/mlc-chat-config.json"
    elif isinstance(obj, PyTorchTransformers):
        path = "./sma_llm/models/hf_pytorch/model/config.json"
    else:
        return None
    
    with open(path, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return None