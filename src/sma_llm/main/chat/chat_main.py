"""Define and start Conversations."""

from .conversation import Conversation
from sma_llm.utils import MLCLLM, PyTorchTransformers # the engines
# from sma_llm.utils import TEXT_TO_SPEECH, SPEECH_TO_TEXT

def run():
    """Choose an engine and start generating."""
    match input('Choose engine: "mlc" or "pytorch"'):
        case "mlc":
            chat = Conversation(MLCLLM())
        case "pt":
            chat = Conversation(PyTorchTransformers())
        case _:
            raise ValueError("Nothing selected")

    chat.converse()

if __name__ == "__main__":
    run()