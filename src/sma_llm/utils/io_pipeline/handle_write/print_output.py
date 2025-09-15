from .write_output import WriteOutput

class PrintOutput(WriteOutput):
    def __init__(self):
        pass
    
    @staticmethod
    def display_output(string: str) -> None:
        print(string, end="", flush=True)