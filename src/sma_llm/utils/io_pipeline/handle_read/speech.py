from .read_input_interface import ReadInput
from sma_llm.utils.text_handler import TextHandler
from .speech_to_text import STT

class SpeechToText(ReadInput):
    def __init__(self):
        pass

    @staticmethod
    def process_input() -> str:
        return TextHandler.spell_corrector(
            TextHandler.pre_process_text(STT())
        )