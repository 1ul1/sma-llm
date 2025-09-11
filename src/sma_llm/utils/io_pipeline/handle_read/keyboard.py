from .read_input import ReadInput
from sma_llm.utils import TextHandler

class Keyboard(ReadInput):
    def __init__(self):
        pass

    @classmethod
    def process_input() -> str:
        return TextHandler.pre_process_text(input("\nUser: "))