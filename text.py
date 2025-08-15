import sys
import textwrap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea, QFrame
from PyQt6.QtCore import QTimer, Qt
import markdown2

class MarkdownTypewriter(QMainWindow):
    """
    A PyQt6 window that displays streamed markdown text with a typewriter animation.
    """
    def __init__(self, parent=None):
        super().__init__()
        
        self.parent_overlay = parent
        self.setGeometry(925, 40, 350, 625)
        self.setWindowTitle("Markdown Typewriter")
        self.setStyleSheet("background-color: white;")
        self.setWindowFlags( Qt.WindowType.WindowStaysOnTopHint)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label.setStyleSheet("""
            color: black; font-size: 16px; padding: 15px;
            line-height: 1.5; background-color: transparent;
            code { 
                background-color: #f0f0f0; padding: 2px 5px; 
                border-radius: 4px; font-family: 'Courier New', monospace;
            }
            h3 { margin-bottom: 10px; }
        """)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout.addWidget(self.scroll_area)

        self.markdowner = markdown2.Markdown(extras=["fenced-code-blocks", "smarty-pants"])

        # --- NEW & MODIFIED ATTRIBUTES ---
        # The buffer that holds text received from the API stream but not yet displayed.
        self.text_buffer = "" 
        # The text that is currently visible on the label.
        self.current_display_text = ""
        
        # RE-INTRODUCED: The timer for the character-by-character animation.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        # We will start the timer only when there is text to display.

    def markdown_to_html(self, text):
        return self.markdowner.convert(text)
        
    def clear_text(self):
        """Clears the buffer and the display for a new response."""
        self.text_buffer = ""
        self.current_display_text = ""
        self.label.setText("")
        self.timer.stop() # Stop any animation in progress

    def append_text(self, chunk):
        """
        MODIFIED: This slot now just adds text to the buffer and ensures the
        animation timer is running. It does NOT update the UI directly.
        """
        self.text_buffer += chunk
        if not self.timer.isActive():
            # Start the typewriter animation at 10ms per character.
            self.timer.start(10) 

    def update_display(self):
        """
        NEW: This method is called by the QTimer. It moves one character
        from the buffer to the display, creating the animation.
        """
        if self.text_buffer:
            # Move the first character from the buffer to the display text
            char_to_add = self.text_buffer[0]
            self.text_buffer = self.text_buffer[1:]
            self.current_display_text += char_to_add
            
            # Update the label with the newly grown text
            html_text = self.markdown_to_html(self.current_display_text)
            self.label.setText(html_text)
            
            # Scroll to the bottom
            scrollbar = self.scroll_area.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        else:
            # If the buffer is empty, stop the timer to save resources.
            self.timer.stop()
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    typewriter = MarkdownTypewriter()
    typewriter.show()
    sys.exit(app.exec())