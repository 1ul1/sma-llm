import PySide6.QtWidgets as Widget
from PySide6.QtCore import Qt
from .global_instances import get_FRONTEND, INPUT_FONT, INPUT_BAR_SIZE, BOTTOM_BAR_SIZE

INPUT_FONT += 5 # to account for font errors

MAXIMUM_HEIGHT = INPUT_BAR_SIZE + INPUT_FONT * 5

class ReadInputUI(Widget.QTextEdit):
    """Widget for input line.
    It extends upwards when running out of available width"""

    def __init__(self, parent = None):
        # set Maximum geight it can extend to to be whole 
        # conversation window with same padding as at the bottom
        try:
            global MAXIMUM_HEIGHT
            MAXIMUM_HEIGHT = (
                get_FRONTEND().body.height() - (BOTTOM_BAR_SIZE - INPUT_BAR_SIZE) / 2
            )
        finally:
            super().__init__(parent)
            self.setLineWrapMode(Widget.QTextEdit.WidgetWidth)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setMaximumHeight(MAXIMUM_HEIGHT)
            self.line_count = 1
            self.new_lines_nr = 0
            self.pressed_keys = {"Enter": False, "Shift": False}

    def keyPressEvent(self, e):
        """Handle Input Bar behaviour.
        Handle resizing after each input
        Handle sending the input
        Handle new lines chars from: clipboard and shift+enter"""

        if e.key() == Qt.Key_Shift:
            self.pressed_keys["Shift"] = True

        if e.key() == Qt.Key_Return:
            if not self.pressed_keys["Shift"]:
                # resize Blob when clearing it
                new_height = INPUT_BAR_SIZE
                delta_height = new_height - self.height()
                self.move(self.pos().x(), self.pos().y() - delta_height)
                self.setFixedHeight(new_height)
                
                # excute read logic
                get_FRONTEND().read()
                self.setFixedHeight(INPUT_BAR_SIZE)
                self.line_count = 1
                self.new_lines_nr = 0
                return
            
            elif self.pressed_keys["Shift"]:
                self.new_lines_nr += 1
        
        super().keyPressEvent(e)

        self.update_height(internal_call=True)

        return
    
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Shift:
            self.pressed_keys["Shift"] = False
            
        return super().keyReleaseEvent(e)
    
    def update_height(self, internal_call = False):
        if not internal_call:
            self.line_count = 1

            global MAXIMUM_HEIGHT
            MAXIMUM_HEIGHT = (
                get_FRONTEND().body.height() - (BOTTOM_BAR_SIZE - INPUT_BAR_SIZE) / 2
            )

        # the nr of lines the text paragraphs themselves require
        needed_height = 0
        block = self.document().firstBlock()

        while block.isValid():
            # the height the text paragraphs themselves require
            needed_height += block.layout().lineCount()
            block = block.next()

        new_height = (
            self.height() + INPUT_FONT * (needed_height -  self.line_count)
        )
        new_height = INPUT_BAR_SIZE if new_height < INPUT_BAR_SIZE else new_height

        delta_height = new_height - self.height()

        self.line_count = needed_height

        # update visual size upwards
        if not (new_height <= MAXIMUM_HEIGHT) and self.height() < MAXIMUM_HEIGHT:
            nr_new_lines = int((MAXIMUM_HEIGHT - self.height()) / INPUT_FONT)
            new_height = nr_new_lines * INPUT_FONT + self.height()
            delta_height = new_height - self.height()

        self.move(self.pos().x(), self.pos().y() - delta_height)
        self.setFixedHeight(new_height)
