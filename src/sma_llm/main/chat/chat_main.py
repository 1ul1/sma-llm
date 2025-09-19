from .conversation import Conversation
from sma_llm.utils import MLCLLM, PyTorchTransformers # the engines
from sma_llm.utils import TEXT_TO_SPEECH

def run():
    """
    Define and start Conversations
    """
    
    chat = Conversation(MLCLLM())
    chat.converse()

if __name__ == "__main__":
    run()