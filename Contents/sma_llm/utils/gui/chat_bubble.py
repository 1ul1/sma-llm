"""Module to handle the UI of messages."""
import PySide6.QtWidgets as Widget
from PySide6.QtCore import Qt
from sma_llm.utils.network.network_interface import TOGGLE
from sma_llm.utils.io_pipeline import get_TEXT_TO_SPEECH
from .global_instances import get_FRONTEND, MESSAGES_PADDING

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
        self.message.setMaximumWidth(get_FRONTEND().window.width() - MESSAGES_PADDING * 2)
        self.message.setWordWrap(True)
        self.message.setText(string)

        self.layout = Widget.QHBoxLayout()
        self.setLayout(self.layout)

        if internal_call is False:
            self.message.setStyleSheet(
                "background-color: transparent; color: #B0FFFD; font-size: 20px; font-weight: bold;"
            )
        else:
            # #FFB0DA
            self.layout.addStretch()
            self.message.setStyleSheet(
                "background-color: transparent; color: white; " 
                + "font-size: 20px; font-weight: bold; padding-left: 300px"
            )

        self.layout.addWidget(self.message)

        TOGGLE.clear()

    def write(self, string: str) -> None:
        """Print assistant response live."""
        self.message.setText(self.message.text() + string)
