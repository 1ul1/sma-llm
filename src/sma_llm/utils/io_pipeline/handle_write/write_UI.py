from .write_output_interface import WriteOutput
from sma_llm.utils.gui.global_instances import get_FRONTEND

class WriteUI(WriteOutput):
    @staticmethod
    def display_output(string: str) -> None:
        if get_FRONTEND() is None:
            return
        get_FRONTEND().write(string)