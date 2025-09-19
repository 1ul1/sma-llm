"""
Speech to text using:
    openai-whisper to transcribe audio;
    ffmpeg to access microphone and pipe audio
"""

from sma_llm.utils.io_pipeline.handle_write import SHOW
import subprocess
import whisper #type: ignore

def STT() -> str:
    """
    Message is recorded until pressing ENTER
    """
    print("System: Listening... ")
    process = subprocess.Popen(
        [
        'ffmpeg', '-y', '-f', 'avfoundation', '-i',
        ':0','-ac', '1', '-ar', '16000', 'output.wav'
        ],
        stderr = subprocess.DEVNULL,
        stdout = subprocess.DEVNULL
    )
    # upload model while waiting for input message to be recorded
    model = whisper.load_model("medium.en")

    input()
    process.terminate()
    process.wait()

    message = (model.transcribe("output.wav"))["text"]
    
    SHOW.display_output(f"User: {message}")
    return message
