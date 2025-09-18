"""
Text to Speech for Mac only
"""

from .write_output_interface import WriteOutput
from AppKit import NSSpeechSynthesizer as text_to_speech #type: ignore
from time import sleep

# text_to_speech
class Speech(WriteOutput):
    instance = None

    def __init__(self):
        pass

    def __new__(cls):
        if Speech.instance is None:
            Speech.instance = super().__new__(cls)
            Speech.instance.tts = text_to_speech.alloc().init()
            # Speech.instance.tts.setVoice_()
        return Speech.instance
    
    @staticmethod
    def display_output(self, text):
        self.tts.startSpeakingString_(text)
        while self.tts.isSpeaking():
            sleep(0.1)