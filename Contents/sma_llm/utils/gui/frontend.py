"""All the GUI logic."""
import PySide6.QtWidgets as Widget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from sma_llm.utils.network.network_interface import TOGGLE
from sma_llm.utils.io_pipeline import get_SPEECH_TO_TEXT, get_TEXT_TO_SPEECH
from .global_instances import get_CONVERSATION_UI
from .chat_bubble import ChatBubble
from .task_automation import check_if_task
from .read_input import ReadInputUI
from time import sleep
from queue import Queue
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
        self.queue = None
        TOGGLE.set()
        self.frontend_logic()

    def frontend_logic(self) -> None:
        """Main logic of the UI."""
        self.window = Widget.QWidget()


        # Make the window appear at center
        (width, height) = Widget.QApplication.screens()[0].availableSize().toTuple()

        self.window.setGeometry((width - 1200) / 2, (height - 750) / 2, 1200, 750)
        self.window.setMinimumSize(1200, 750)
        self.window.setContentsMargins(0, 0, 0, 0)
        self.window.setLayout(self.layout)
        self.window.setWindowFlag(Qt.FramelessWindowHint)
        self.window.setAttribute(Qt.WA_TranslucentBackground)

        # Top
        self.top_layout = Widget.QHBoxLayout()
        self.top_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.top_container = Widget.QWidget()
        self.top_container.setContentsMargins(50, 0, 10, 0)
        self.top = Widget.QLabel(self.top_container, alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.top.setStyleSheet(
            "background-color: black; color: white; font-size: 16px;"
            + " text-align: right; font-weight: bold; padding-right: 10px;"
            + " border-top-left-radius: 20px; border-top-right-radius: 20px"
        )
        self.top.setText("SMA-LLM")
        self.top.setFixedHeight(42)
        self.top.setLayout(self.top_layout)
        self.top.setSizePolicy(Widget.QSizePolicy.Expanding, Widget.QSizePolicy.Expanding)
        self.layout.addWidget(self.top)
        
        # Close Button
        self.close = Widget.QPushButton("X")
        self.close.setFixedSize(16, 16)
        self.close.setStyleSheet(
            "background-color: grey; color: white;"
            + " border-radius: 8px; font-size: 12px; text-align: center;"
            + " font-weight: bold; border: none; padding: 0px;"
        )
        self.close.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.close.pressed.connect(self.window.close)
        self.top_layout.addWidget(self.close)

        # Body
        self.body = Widget.QWidget()
        self.body.setStyleSheet(
            "background-color: rgba(0, 0, 0, 150); border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;"
            + "border: none"
        )
        self.body.setContentsMargins(0, 0, 0 , 0)
        self.body_layout = Widget.QVBoxLayout()
        self.body.setLayout(self.body_layout)
        self.body_layout.setAlignment(Qt.AlignTop)
        self.body_layout.setContentsMargins(0, 0 , 0, 0)
        self.layout.addWidget(self.body)

        # Conversation UI
        self.conversation_full = Widget.QScrollArea()
        self.conversation_full.setSizePolicy(Widget.QSizePolicy.Expanding, Widget.QSizePolicy.Expanding)
        self.conversation_full.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.conversation_full.setContentsMargins(0, 0, 0, 0)
        self.conversation_full.setWidgetResizable(True)
        self.conversation_full.setStyleSheet("background-color: transparent")
        self.conversation = Widget.QWidget()
        self.conversation.setStyleSheet(
            "background-color: transparent; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;"
        )
        self.conversation_full.setWidget(self.conversation)
        self.message_layout = Widget.QVBoxLayout()
        self.message_layout.setSpacing(0)
        self.message_layout.setContentsMargins(0, 0, 0, 0)
        self.message_layout.setAlignment(Qt.AlignTop)
        self.conversation.setLayout(self.message_layout)
        
        self.conversation_full.setSizePolicy(Widget.QSizePolicy.Expanding, Widget.QSizePolicy.Expanding)
        self.body_layout.addWidget(self.conversation_full)
        self.current_chat_bubble = None

        self.bottom = Widget.QWidget()
        self.bottom.setStyleSheet(
            "background-color: transparent; border: none"
        )
        self.bottom.setFixedHeight(84)
        self.bottom.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout = Widget.QHBoxLayout()
        self.bottom_layout.setAlignment(Qt.AlignVCenter)
        self.bottom_layout.setContentsMargins(40, 0, 40, 0)
        self.bottom_layout.setSpacing(50)
        self.bottom.setLayout(self.bottom_layout)
       
        # Dark Mode | Light Mode Toggle Button
        self.light_mode_toggle = False
        self.light_mode = Widget.QPushButton("☀️")
        self.light_mode.setFont(QFont("", 30))
        self.light_mode.setStyleSheet(
            "background-color: transparent; border: none; padding: 0px;"
        )
        self.light_mode.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.bottom_layout.addWidget(self.light_mode)

        self._empty_filler =  Widget.QWidget()
        self._empty_filler.setSizePolicy(Widget.QSizePolicy.Expanding, Widget.QSizePolicy.Expanding)
        self._empty_filler.setStyleSheet("background-color: transparent;")
        self.bottom_layout.addWidget(self._empty_filler)

        # STT and TTS buttons
        self.ST = Widget.QWidget()
        self.ST.setStyleSheet("background-color: transparent; border: none;")
        self.ST.setContentsMargins(0, 0, 0, 0)
        ST_layout = Widget.QHBoxLayout()
        ST_layout.setContentsMargins(0, 0, 0, 0)
        ST_layout.setSpacing(20)
        self.ST.setLayout(ST_layout)
        self.bottom_layout.addWidget(self.ST)

        # microphone
        self.input_vocal = Widget.QPushButton("🎤")# 🎤
        self.input_vocal.setFont(QFont("", 30))
        self.input_vocal.setStyleSheet("background-color: transparent; color: #43BAA2; border: none")
        self.input_vocal.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        ST_layout.addWidget(self.input_vocal)

        # text to speech
        self.output_vocal = Widget.QPushButton("🔇")
        self.output_vocal.setFont(QFont("", 30))
        self.output_vocal.setStyleSheet("background-color: transparent; color: #43BAA2; border: none")
        self.output_vocal.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        ST_layout.addWidget(self.output_vocal)

        self.bottom.setSizePolicy(Widget.QSizePolicy.Expanding, Widget.QSizePolicy.Expanding)
        self.body_layout.addWidget(self.bottom)

    def run(self):
        self.input_vocal.clicked.connect(self.read_vocal)
        self.output_vocal.clicked.connect(self.set_vocal)
        self.light_mode.pressed.connect(self.change_light_mode)

        try:
            # signal wait_screen UI
            os.kill(int(sys.argv[1]), signal.SIGINT)
        finally:
            self.window.show()
            self.chat.lastWindowClosed.connect(self.kill)
            self.add_input_message_blob()
            self.chat.exec()

    def add_input_message_blob(self):
        self.input_message = ReadInputUI()
        self.input_message.setSizePolicy(Widget.QSizePolicy.Expanding, Widget.QSizePolicy.Preferred)
        self.input_message.setStyleSheet(
            "background-color: black; color: white; border: 1px solid white;"
            + " border-radius: 20px; padding-left: 20px; padding-right: 20px;"
            + " padding-top: 5px; padding-bottom: 5px"
        )
        self.input_message.setFont(QFont("", 30))
        self.input_message.setParent(self.body)
        self.input_message.setWindowFlag(Qt.FramelessWindowHint)
        self.input_message.move(
            170,
            self.body.height() - self.bottom.height() + 17
        )
        self.input_message.setFixedHeight(50)
        self.input_message.setFixedWidth(
            self.body.width() - 320
        )
        self.input_message.show()

    @staticmethod
    def kill(_1 = None, _2 = None):
        os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)
        Widget.QApplication.quit()

    def write(self, string: str) -> None:
        """Generate() runs in a thread.
        it will call this method and write output to a queue (thread safe data structure)
        which will further be used to process the output back in the main thread to update UI
        """
        self.queue.put(string)

    def aux_write(self) -> None:
        """Print assistant response live.
        Extract from Queue and process them back in the main thread
        """
        try:
            string = self.queue.get(block=False)
        except:
            # stops when queue is empty and generation is terminated
            if TOGGLE.is_set():
                self.timer.stop()
            return

        self.current_chat_bubble.write(string)

        if self.speak is True:
            get_TEXT_TO_SPEECH().display_output(string)

        self.chat.processEvents()
        
        self.conversation_full.ensureWidgetVisible(self.current_chat_bubble)

    def generate(self, my_input: str) -> None:
        """Calls the generate() that runs in a thread.
        This way everything is nonblocking for the UI"""
        self.current_chat_bubble = ChatBubble()
        self.message_layout.addWidget(self.current_chat_bubble)

        self.queue = Queue()

        get_CONVERSATION_UI().converse_UI(my_input)

        self.timer = QTimer()
        self.timer.setInterval(25)
        self.timer.timeout.connect(self.aux_write)
        self.timer.start()

    def read(self) -> str:
        """Read stdin and add move it into chat."""
        my_input = self.input_message.toPlainText()

        if my_input == "" and not TOGGLE.is_set():
            self.queue = Queue()
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
        
        self.generate(my_input=my_input)

        return my_input
    
    def read_vocal(self) -> None | str:
        """Method to handle Speech to Text."""
        if not TOGGLE.is_set():
            self.queue = Queue()
            TOGGLE.set()

        self.audio = not self.audio

        if self.audio is True:
            # start recording
            get_TEXT_TO_SPEECH().stop() # stop speaking

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

            self.generate(my_input=my_input)

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
            get_TEXT_TO_SPEECH().stop() # stop speaking

    def change_light_mode(self):
        self.light_mode_toggle = not self.light_mode_toggle

        if self.light_mode_toggle:
            self.top.setStyleSheet(
                "background-color: white; color: black; font-size: 16px;"
                + " text-align: right; font-weight: bold; padding-right: 10px;"
                + " border-top-left-radius: 20px; border-top-right-radius: 20px"
            )
            self.input_message.setStyleSheet(
                "background-color: white; color: black; border: 1px solid black;"
                + " border-radius: 20px; padding-left: 20px; padding-right: 20px;"
                + " padding-top: 5px; padding-bottom: 5px"
            )
            self.light_mode.setText("🌑")
            return
        
        self.top.setStyleSheet(
            "background-color: black; color: white; font-size: 16px;"
            + " text-align: right; font-weight: bold; padding-right: 10px;"
            + " border-top-left-radius: 20px; border-top-right-radius: 20px"
        )
        self.input_message.setStyleSheet(
            "background-color: black; color: white; border: 1px solid white;"
            + " border-radius: 20px; padding-left: 20px; padding-right: 20px;"
            + " padding-top: 5px; padding-bottom: 5px"
        )
        self.light_mode.setText("☀️")
        return
        