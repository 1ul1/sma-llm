"""Text to Speech for Mac only."""

from .write_output_interface import WriteOutput
from AppKit import NSSpeechSynthesizer as text_to_speech
from time import sleep
from threading import Thread
from sma_llm.utils.network.network_interface import TOGGLE

# text_to_speech
class TextToSpeech(WriteOutput):
    instance = None
    TOGGLE = None
    text = ""
    check_to_speak = None

    def __init__(self):
        def aux():
            while True:
                if TOGGLE.is_set() and not self.tts.isSpeaking():
                    self.display_output("")
                sleep(0.1)

        if self.check_to_speak is None:
            self.check_to_speak = Thread(target=aux, daemon=True)
            self.check_to_speak.start()

        return

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.tts = text_to_speech.alloc().init()
            # cls.instance.tts.setVoice_()
        return cls.instance
    
    def stop(self):
        self.tts.stopSpeaking()
        self.text = ""
    
    def display_output(self, text):
        self.text += text

        if self.tts.isSpeaking() or self.text == "":
            return
        
        text_to_speak = self.text
        self.text = ""

        def aux_display_output():
            self.tts.startSpeakingString_(text_to_speak)
            while self.tts.isSpeaking():
                sleep(0.01)
        
        thread = Thread(target=aux_display_output, daemon=True)
        thread.start()
