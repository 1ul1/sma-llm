"""Wait Screen while models upload."""
import PySide6.QtWidgets as Widget
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
import signal

class WaitScreen():
    """Wait Screen while models upload."""
    def __init__(self):
        self.wait_screen = Widget.QApplication([])
        self.layout = Widget.QVBoxLayout()

        self.window = Widget.QWidget()
        self.window.setLayout(self.layout)
        self.window.setWindowFlags(Qt.FramelessWindowHint)

        self.window.setFixedSize(700, 400)
        self.window.setStyleSheet("background-color: white; border-radius: 10px;")

        # Text
        self.text = Widget.QLabel()
        self.layout.addWidget(self.text, alignment=Qt.AlignCenter)

        self.text.setStyleSheet(
            "background-color: transparent; color: black;"
            + " font-size: 32px; text-align: center; font-weight: bold;"
        )
        self.text.setText("Launching   ")

        # Timer for animation
        self.animation = ["Launching   ", "Launching.  ", "Launching.. ", "Launching..."]
        self.index = 0
        self.timer = QTimer()
        self.timer.setInterval(750) # 0.75 seconds
        self.timer.timeout.connect(self.loading_animation)

        self.run()

    def loading_animation(self):
        self.text.setText(self.animation[self.index])
        self.index = (self.index + 1) if self.index < 3 else 0
        self.timer.start()

    def run(self):
        self.timer.start()
        self.window.show()

        # handle termination
        def exit_gracefully(_1 = None, _2 = None):
            Widget.QApplication.quit()
            exit(0)

        signal.signal(signal.SIGINT, exit_gracefully)
        signal.signal(signal.SIGTERM, exit_gracefully)
        signal.signal(signal.SIGHUP, exit_gracefully)
        signal.signal(signal.SIGQUIT, exit_gracefully)

        try:
            self.wait_screen.exec()
        finally:
            exit_gracefully()

if __name__ == "__main__":
    WaitScreen()