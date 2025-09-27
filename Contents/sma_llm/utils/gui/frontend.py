"""All the GUI logic."""
import PySide6.QtWidgets as Widget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from sma_llm.utils.network.network_interface import TOGGLE
from sma_llm.utils.io_pipeline import get_SPEECH_TO_TEXT, get_TEXT_TO_SPEECH
from .global_instances import get_CONVERSATION_UI
from .chat_bubble import ChatBubble
from .task_automation import check_if_task
from time import sleep
import os
import signal
import sys

class Frontend():
    def __init__(self):
        self.chat = Widget.QApplication([])
        self.layout = Widget.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.audio = False
        self.speak = False
        TOGGLE.set()
        self.frontend_logic()

    def frontend_logic(self) -> None:
        """Main logic of the UI."""
        self.window = Widget.QWidget()

        # Make the window appear at center
        (width, height) = Widget.QApplication.screens()[0].availableSize().toTuple()

        self.window.setGeometry((width - 700) / 2, (height - 400) / 2, 700, 400)
        self.window.setMinimumSize(700, 400)
        self.window.setContentsMargins(0, 0, 0, 0)
        self.window.setLayout(self.layout)

        self.conversation_full = Widget.QScrollArea()
        self.conversation_full.setContentsMargins(0, 0, 0, 0)
        self.conversation_full.setWidgetResizable(True)
        self.conversation = Widget.QWidget()
        self.conversation.setStyleSheet("background-color: white")
        self.conversation_full.setWidget(self.conversation)
        self.message_layout = Widget.QVBoxLayout()
        self.message_layout.setSpacing(0)
        self.message_layout.setContentsMargins(0, 0, 0, 0)
        self.message_layout.setAlignment(Qt.AlignTop)
        self.conversation.setLayout(self.message_layout)
        
        self.layout.addWidget(self.conversation_full)
        self.current_chat_bubble = None

        self.bottom = Widget.QWidget()
        self.bottom.setStyleSheet("background-color: white")
        self.bottom.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout = Widget.QHBoxLayout()
        self.bottom_layout.setContentsMargins(20, 0, 20, 0)
        self.bottom_layout.setSpacing(20)
        self.bottom.setLayout(self.bottom_layout)

        # message
        self.input_message = Widget.QLineEdit()
        self.input_message.setFixedHeight(30)
        self.input_message.setStyleSheet("background-color: transparent; color: black; border: none")
        self.input_message.setFont(QFont("", 18))
        self.bottom_layout.addWidget(self.input_message)

        # microphone
        self.input_vocal = Widget.QPushButton("🎤")# 🎤
        self.input_vocal.setStyleSheet("background-color: transparent; color: #43BAA2; border: none")
        self.input_vocal.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.bottom_layout.addWidget(self.input_vocal)

        # text to speech
        self.output_vocal = Widget.QPushButton("🔇")
        self.output_vocal.setStyleSheet("background-color: transparent; color: #43BAA2; border: none")
        self.output_vocal.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.bottom_layout.addWidget(self.output_vocal)

        self.layout.addWidget(self.bottom)

    def run(self):
        self.input_message.returnPressed.connect(self.read)
        self.input_vocal.clicked.connect(self.read_vocal)
        self.output_vocal.clicked.connect(self.set_vocal)

        try:
            # signal wait_screen UI
            os.kill(int(sys.argv[1]), signal.SIGINT)
        finally:
            self.window.show()
            self.chat.lastWindowClosed.connect(self.kill)
            self.chat.exec()

    @staticmethod
    def kill():
        Widget.QApplication.quit()
        os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)

    def write(self, string: str) -> None:
        """Print assistant response live."""
        self.current_chat_bubble.write(string)

        if self.speak is True:
            get_TEXT_TO_SPEECH().display_output(string)

        self.chat.processEvents()
        
        self.conversation_full.ensureWidgetVisible(self.current_chat_bubble)

    def read(self) -> str:
        """Read stdin and add move it into chat."""
        my_input = self.input_message.text()

        if my_input == "" and not TOGGLE.is_set():
            TOGGLE.set()
            return

        if my_input == "" or not TOGGLE.is_set():
            return
        
        # check if task
        if my_input != "" and my_input[0] == '-' and ' ' not in my_input:
            # single words starting with '-' are not considered for conversation
            check_if_task(my_input)

            self.input_message.clear()
            return

        self.message_layout.addWidget(ChatBubble(my_input, internal_call = True))

        self.input_message.clear()

        self.conversation_full.verticalScrollBar().setValue(
            self.conversation_full.verticalScrollBar().maximum()
        )

        self.chat.processEvents()

        self.current_chat_bubble = ChatBubble()
        self.message_layout.addWidget(self.current_chat_bubble)

        get_CONVERSATION_UI().converse_UI(my_input)

        return my_input
    
    def read_vocal(self) -> None | str:
        """Method to handle Speech to Text."""
        if not TOGGLE.is_set():
            TOGGLE.set()

        self.audio = not self.audio

        if self.audio is True:
            # start recording
            self.input_vocal.setText("🔴")
            self.chat.processEvents()
            get_SPEECH_TO_TEXT().get_stt.STT(True)
            return

        if self.audio is False:
            # stop recording gather input transcribe return
            self.input_vocal.setText("🎤")
            self.chat.processEvents()

            my_input = get_SPEECH_TO_TEXT().get_stt.STT_UI()
            sleep(0.05)

            self.message_layout.addWidget(ChatBubble(my_input, internal_call = True))

            self.conversation_full.verticalScrollBar().setValue(
                self.conversation_full.verticalScrollBar().maximum()
            )

            self.chat.processEvents()

            self.current_chat_bubble = ChatBubble()
            self.message_layout.addWidget(self.current_chat_bubble)

            get_CONVERSATION_UI().converse_UI(my_input)

            return my_input
        
    def set_vocal(self) -> None:
        """Method to handle Text to Speech."""
        self.speak = not self.speak

        if self.speak is True:
            self.output_vocal.setText("🔈")
            self.chat.processEvents()
        else:
            self.output_vocal.setText("🔇")
            self.chat.processEvents()
            get_TEXT_TO_SPEECH().stop()