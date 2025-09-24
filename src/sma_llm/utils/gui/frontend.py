"""All the GUI logic."""
import PySide6.QtWidgets as Widget
from sma_llm.utils.network.network_interface import TOGGLE
from sma_llm.utils.io_pipeline import get_SPEECH_TO_TEXT
from sma_llm.utils.gui.global_instances import get_CONVERSATION_UI

class Frontend():
    def __init__(self):
        self.chat = Widget.QApplication([])
        self.layout = Widget.QVBoxLayout()
        self.toggle = True
        self.audio = False
        self.frontend_logic()

    def frontend_logic(self) -> None:
        """Main logic."""
        self.window = Widget.QWidget()
        self.window.setLayout(self.layout)

        self.conversation_full = Widget.QScrollArea()
        self.conversation_full.setWidgetResizable(True)
        self.conversation = Widget.QWidget()
        self.conversation_full.setWidget(self.conversation)
        self.message_layout = Widget.QVBoxLayout()
        self.conversation.setLayout(self.message_layout)
        
        self.layout.addWidget(self.conversation_full)

        self.bottom = Widget.QWidget()
        self.bottom_layout = Widget.QHBoxLayout()
        self.bottom.setLayout(self.bottom_layout)

        # message
        self.input_message = Widget.QLineEdit()
        self.bottom_layout.addWidget(self.input_message)

        # microphone
        self.input_vocal = Widget.QPushButton("🎤")
        self.bottom_layout.addWidget(self.input_vocal)

        self.layout.addWidget(self.bottom)

    def run(self):
        self.input_message.returnPressed.connect(self.read)
        self.input_vocal.clicked.connect(self.read_vocal)
        self.window.show()
        self.chat.exec()

    
    # Read and Write texts:
    def set_write(self):
        """Set up the buble for the assistant's live response."""
        self.toggle = False

        self.message = Widget.QTextEdit()
        self.message.setStyleSheet("background-color: pink; color: black;")
        self.message.setReadOnly(True)
        self.message.setPlainText("")
        self.message_layout.addWidget(self.message)
        # Toggle.clear() is handled in conversation module

    def unset_write(self):
        """Called from the model when done generating."""
        self.message = None
        self.toggle = True

    def write(self, string: str) -> None:
        """Print assistant response live."""
        if TOGGLE.is_set():
            self.unset_write()
            return

        if self.message is None:
            return
        
        self.message.append(string)
        
        self.conversation_full.verticalScrollBar().setValue(
            self.conversation_full.verticalScrollBar().maximum()
        )

    def read(self) -> str:
        """Read stdin and add move it into chat."""
        my_input = self.input_message.text()

        if my_input == "" and self.toggle is False:
            TOGGLE.set()
            return

        if my_input == "" or self.toggle is False:
            return

        message = Widget.QTextEdit()
        message.setStyleSheet("background-color: lightblue; color: black;")
        message.setReadOnly(True)
        message.setPlainText(my_input)
        self.message_layout.addWidget(message)
        self.input_message.clear()

        self.conversation_full.verticalScrollBar().setValue(
            self.conversation_full.verticalScrollBar().maximum()
        )

        self.set_write()

        get_CONVERSATION_UI().converse_UI(my_input)

        return my_input
    
    def read_vocal(self) -> None | str:
        self.audio = not self.audio
        if self.audio is True:
            # start recording
            self.input_vocal.setText("🔴")
            get_SPEECH_TO_TEXT().get_stt.STT(True)
            return

        if self.audio is False:
            # stop recording gather input transcribe return
            self.input_vocal.setText("🎤")

            my_input = get_SPEECH_TO_TEXT().get_stt.STT_UI()

            self.set_write()
            self.message.setPlainText(my_input)
            self.conversation_full.verticalScrollBar().setValue(
                self.conversation_full.verticalScrollBar().maximum()
            )
            self.unset_write()

            return my_input
