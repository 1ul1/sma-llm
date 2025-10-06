import PySide6.QtWidgets as Widget
from PySide6.QtCore import Qt
from .global_instances import get_FRONTEND

class ReadInputUI(Widget.QTextEdit):
    """Widget for input line.
    It extends upwards when running out of available widht"""

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setLineWrapMode(Widget.QTextEdit.WidgetWidth)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumHeight(230)
        self.line_count = 1

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            # resize Blob
            new_height = 50
            delta_height = new_height - self.height()
            self.move(self.pos().x(), self.pos().y() - delta_height)
            self.setFixedHeight(new_height)
            
            # excute read logic
            get_FRONTEND().read()
            self.setFixedHeight(50)
            self.line_count = 1
            return
        
        super().keyPressEvent(e)

        new_height = (
            self.height() + 35 * (self.document().firstBlock().layout().lineCount() -  self.line_count)
        )
        new_height = 50 if new_height < 50 else new_height

        delta_height = new_height - self.height()

        self.line_count = self.document().firstBlock().layout().lineCount()

        # update visual size upwards
        if new_height < 230:
            self.move(self.pos().x(), self.pos().y() - delta_height)
            self.setFixedHeight(new_height)
        elif self.height() < 200:
            nr_new_lines = (225 - self.height()) % 35
            new_height = nr_new_lines * 35 + self.height()
            delta_height = new_height - self.height()
            self.move(self.pos().x(), self.pos().y() - delta_height)

        return
