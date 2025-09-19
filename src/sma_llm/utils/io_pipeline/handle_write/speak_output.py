"""
Text to Speech for Mac only
"""

from .write_output_interface import WriteOutput
from AppKit import NSSpeechSynthesizer as text_to_speech #type: ignore
from time import sleep

# text_to_speech
class TextToSpeech(WriteOutput):
    instance = None

    def __init__(self):
        pass

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.tts = text_to_speech.alloc().init()
            # cls.instance.tts.setVoice_()
        return cls.instance
    
    def display_output(self, text):
        self.tts.startSpeakingString_(text)
        while self.tts.isSpeaking():
            sleep(0.1)