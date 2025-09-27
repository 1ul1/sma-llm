from .write_output_interface import WriteOutput

class PrintOutput(WriteOutput):
    instance = None

    def __init__(self):
        pass

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance


    @staticmethod
    def display_output(string: str) -> None:
        print(string, end="", flush=True)