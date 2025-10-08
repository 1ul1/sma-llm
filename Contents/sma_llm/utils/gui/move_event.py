import PySide6.QtWidgets as Widget
from PySide6.QtCore import Qt, QObject, QEvent, QPointF, QPoint
from PySide6.QtGui import QMouseEvent

class MoveEvent(QObject):
    """Handle and Enable the moving of the app."""
    def __init__(self, target, parent=None):
        super().__init__(parent)

        self.target = target # the main app window
        self.toggle = False # only move during event
        self.initial_pos = QPointF()

    def eventFilter(self, watched, event):
        """The logic behind the moving with the mouse."""
        if isinstance(event, QMouseEvent):
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.toggle = True
                self.initial_pos = event.globalPosition()

                return True

            if (
                (event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton)
                or event.type() == QEvent.Leave
                ):
                self.toggle = False
                self.initial_pos = QPointF()

                return True

            if self.toggle and event.type() == QEvent.MouseMove:
                current_pos = event.globalPosition()
                offset = QPoint()
                offset = (current_pos - self.initial_pos).toPoint()

                self.initial_pos = current_pos

                self.target.move(self.target.pos() + offset)

                return True

        return super().eventFilter(watched, event)