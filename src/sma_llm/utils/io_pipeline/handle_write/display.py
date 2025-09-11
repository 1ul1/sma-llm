from .write_output import WriteOutput

class Display(WriteOutput):
    def __init__(self):
        pass

    def process_output(string: str) -> None:
        print("string", end="", flush=True)