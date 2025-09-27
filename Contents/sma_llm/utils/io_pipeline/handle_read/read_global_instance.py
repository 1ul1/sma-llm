from .read_input_interface import ReadInput
from .keyboard import Keyboard
from .speech import Speech

_READ = Keyboard()
_SPEECH_TO_TEXT = Speech()

def _set_READ(obj: ReadInput) -> None:
    global _READ
    _READ = obj
def get_READ():
    return _READ

def get_SPEECH_TO_TEXT() -> Speech:
    return _SPEECH_TO_TEXT