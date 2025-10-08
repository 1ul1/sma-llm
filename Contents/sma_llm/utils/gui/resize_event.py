import PySide6.QtWidgets as Widget
from PySide6.QtCore import QObject, QEvent
from .global_instances import get_FRONTEND, MESSAGES_PADDING, BOTTOM_BAR_SIZE, INPUT_BAR_SIZE

class ResizeEvent(QObject):
    """Handle and Enable the moving of the app."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, watched, event):
        ok = False

        if event.type() == QEvent.WindowStateChange:
            get_FRONTEND().fullscreen.show()
            ok = True # trigger resizing

        if event.type() == QEvent.Resize or ok:
            get_FRONTEND().input_message.move(
                MESSAGES_PADDING,
                get_FRONTEND().body.height() - (BOTTOM_BAR_SIZE + INPUT_BAR_SIZE) / 2
            )
            get_FRONTEND().input_message.setFixedHeight(INPUT_BAR_SIZE)
            get_FRONTEND().input_message.setFixedWidth(
                get_FRONTEND().body.width() - MESSAGES_PADDING * 2
            )
            get_FRONTEND().input_message.update_height()

            return True

        return super().eventFilter(watched, event)