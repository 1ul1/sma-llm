from .write_output_interface import WriteOutput
from .print_output import PrintOutput
from .write_UI import WriteUI
from .speak_output import TextToSpeech

_SHOW = PrintOutput()
_TEXT_TO_SPEECH = TextToSpeech()

def set_SHOW(obj: WriteOutput) -> None:
    global _SHOW
    _SHOW = obj
    
def get_SHOW() -> WriteOutput:
    return _SHOW

def get_TEXT_TO_SPEECH() -> WriteOutput:
    return _TEXT_TO_SPEECH
