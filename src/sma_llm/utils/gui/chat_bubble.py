"""Module to handle the UI of messages."""
import PySide6.QtWidgets as Widget
from PySide6.QtCore import Qt
from sma_llm.utils.network.network_interface import TOGGLE
from sma_llm.utils.io_pipeline import get_TEXT_TO_SPEECH

class ChatBubble(Widget.QWidget):
    """Each class instance is a message bubble."""
    def __init__(self, string: str = "", internal_call: bool = False, parent = None):
        """Set up the buble."""
        # If new message, Text_to_speech should move over the last
        if internal_call:
            get_TEXT_TO_SPEECH().stop()

        super().__init__(parent)

        self.message = Widget.QLabel()
        self.message.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.message.setSizePolicy(Widget.QSizePolicy.Minimum, Widget.QSizePolicy.Minimum)
        self.message.setMaximumWidth(5000)
        self.message.setWordWrap(True)
        self.message.setText(string)

        self.layout = Widget.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        if internal_call is False:
            self.message.setStyleSheet(
                "background-color: transparent; color: black; padding: 15px; font-size: 14px; text-align: left"
                + "; font-weight: bold"
            )
        else:
            self.message.setStyleSheet(
                "background-color: transparent; color: black; padding: 15px; font-size: 14px; max-width: 650px; "
                + "text-align: right; font-weight: bold"
            )
            self.layout.addStretch()

        self.layout.addWidget(self.message)

        TOGGLE.clear()

    def write(self, string: str) -> None:
        """Print assistant response live."""
        self.message.setText(self.message.text() + string)
