"""Wait Screen while models upload."""
import PySide6.QtWidgets as Widget

class WaitScreen():
    """Wait Screen while models upload."""
    def __init__(self):
        self.wait_screen = Widget.QApplication([])
        self.layout = Widget.QVBoxLayout()

        self.window = Widget.QWidget()
        self.window.setLayout(self.layout)

        self.window.setFixedSize(200, 100)
        self.window.setStyleSheet("background-color: white")

        # Text
        self.text = Widget.QLabel()
        self.layout.addWidget(self.text)

        self.text.setStyleSheet(
            "background-color: transparent; color: black;"
            + " font-size: 14px; text-align: center; font-weight: bold"
        )
        self.text.setText("Launching")

        self.run()

    def run(self):
        self.window.show()
        self.wait_screen.exec()

if __name__ == "__main__":
    WaitScreen()