from .conversation import Conversation
from sma_llm.utils import Network, MLCLLM, PyTorchTransformers # the engines

def run():
    chat = Conversation(PyTorchTransformers())
    chat.converse()

if __name__ == "__main__":
    run()