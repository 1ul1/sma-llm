"""Define and start Conversations."""

from .conversation import Conversation
from sma_llm.utils import MLCLLM, PyTorchTransformers
from sma_llm.utils import start_GUI, set_CONVERSATION_UI
import signal
import os

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

def run_UI() -> None:
    try:
        set_CONVERSATION_UI(Conversation(MLCLLM()))
        start_GUI()
    except:
        os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)