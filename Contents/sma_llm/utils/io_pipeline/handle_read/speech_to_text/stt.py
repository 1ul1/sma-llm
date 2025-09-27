"""
Speech to text using:
    openai-whisper to transcribe audio;
    ffmpeg to access microphone and pipe audio
"""

import subprocess
import whisper

class SpeechToText:
    """Handle all the Speech to Text logic, methods, data.
    - singletone cause the system has only one microphone"""
    instance = None
    model = None
    process = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if self.model is None:
            self.model = whisper.load_model("medium.en")

    def terminate(self):
        self.model = None
        self.process = None

    def STT(self, call_from_UI = False) -> None:
        """Record message, save it in."""
        # from sma_llm.utils.io_pipeline.handle_write.write_global_instance import get_SHOW
        # get_SHOW().display_output("System: Listening... ")
        self.process = subprocess.Popen(
            [
            'ffmpeg', '-y', '-f', 'avfoundation', '-i',
            ':0','-ac', '1', '-ar', '16000', './Output/output.wav'
            ],
            stderr = subprocess.DEVNULL,
            stdout = subprocess.DEVNULL
        )

        if not call_from_UI:
            self.STT_normal()

        return

    def STT_normal(self) -> str:
        """Message is recorded until pressing ENTER"""
        from sma_llm.utils.io_pipeline.handle_write.write_global_instance import get_SHOW
        input()
        self.process.terminate()
        self.process.wait()

        message = (self.model.transcribe("./Output/output.wav"))["text"]
        
        get_SHOW().display_output(f"User: {message}")
        self.terminate()

        return message

    def STT_UI(self) -> str:
        """Message is recorded until the UI button signals it"""
        self.process.terminate()
        self.process.wait()
        message = (self.model.transcribe("./Output/output.wav"))["text"]
        self.terminate()

        return message
