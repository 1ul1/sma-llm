from .conversation import Conversation
from sma_llm.utils import MLCLLM, PyTorchTransformers # the engines

def run():
    chat = Conversation(MLCLLM())
    chat.converse()

if __name__ == "__main__":
    run()