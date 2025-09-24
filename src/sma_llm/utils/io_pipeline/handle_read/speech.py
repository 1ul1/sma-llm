from .read_input_interface import ReadInput
from sma_llm.utils.text_handler import TextHandler
from .speech_to_text.stt import SpeechToText

class Speech(ReadInput):
    _stt = None

    def __init__(self):
        if self._stt is None:
            self._stt = SpeechToText()

    @property
    def get_stt(self) -> SpeechToText | None:
        return self._stt

    @staticmethod
    def process_input() -> str:
        return TextHandler.spell_corrector(
            TextHandler.pre_process_text(Speech.get_stt.STT())
        )