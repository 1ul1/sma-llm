from .read_input import ReadInput
from sma_llm.utils.text_handler import TextHandler

class Keyboard(ReadInput):
    def __init__(self):
        pass

    @staticmethod
    def process_input() -> str:
        return TextHandler.spell_corrector(
            TextHandler.pre_process_text(input("User: "))
        )