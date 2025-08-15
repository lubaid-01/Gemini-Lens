# Import necessary modules from PyQt6
import sys
from PyQt6.QtCore import Qt, QPoint, QThread
from PyQt6.QtGui import QPainter, QPen, QColor, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QMenu, QInputDialog
from PIL import ImageGrab 
from text import MarkdownTypewriter
from gemini import GeminiWorker 


class DrawingOverlay(QWidget):
    """
    A full-screen, transparent widget that allows you to draw on top of other windows.
    Right-click to open a menu to clear the drawing or quit the application.
    """
    def __init__(self):
        # Initialize the QWidget parent class
        super().__init__()

        # --- Window Setup ---
        # Set window flags to make the window frameless and always stay on top.
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint 
        )
        # This attribute is essential to tell the window system that the
        # widget's background can be transparent.
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # --- Fullscreen Geometry ---
        # Get the geometry of the primary screen.
        screen_geometry = QApplication.primaryScreen().geometry()
        # Set the widget's geometry to match the screen, making it fullscreen.
        self.setGeometry(screen_geometry)

        # --- Drawing State ---
        # A list to store the points of the line currently being drawn.
        self.current_path = []
        # A list to store all the completed lines (paths).
        self.paths = []
        # The color of the pen.
        self.pen_color = QColor(255, 0, 0, 200) # Semi-transparent red
        # The width of the pen.
        self.pen_width = 4
        self.pen = QPen(self.pen_color, float(self.pen_width), Qt.PenStyle.SolidLine)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

        # Screenshot wnidow
        self.typeWriter = MarkdownTypewriter(parent=self) #set pre text if you want
        #model param
        self.model = "gemini-1.5-flash"
        self.prompt = "Exlain what is on the screen in 100 words"
        self.thread = None
        self.worker = None
        self.image = None
        # Display the widget.
        self.show()

    def paintEvent(self, event):
        """
        This event is called automatically whenever the widget needs to be redrawn.
        It handles drawing all the completed paths and the current in-progress path.
        """
        # Create a QPainter object to perform drawing on this widget.
        painter = QPainter(self)
        
        # Fill the entire window with a nearly invisible color.
        # This ensures the widget has a "body" to capture mouse events everywhere,
        # preventing "click-through" issues.
        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))
        
        # Enable anti-aliasing for smoother lines.
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set up the pen for drawing.

        painter.setPen(self.pen)

        # Draw all the previously completed paths.
        for path in self.paths:
            if len(path) > 1:
                painter.drawPolyline(path)
        
        # Draw the current line that is actively being drawn.
        if len(self.current_path) > 1:
            painter.drawPolyline(self.current_path)

    def mousePressEvent(self, event):
        """
        Called when a mouse button is pressed. Starts a new drawing path.
        """
        # Check if the left mouse button was pressed.
        if event.button() == Qt.MouseButton.LeftButton:
            # Start a new path at the current mouse position.
            self.current_path = [event.pos()]

    def mouseMoveEvent(self, event):
        """
        Called when the mouse is moved while a button is held down.
        """
        # Check if the left mouse button is being held down.
        if event.buttons() & Qt.MouseButton.LeftButton:
            # Add the new mouse position to the current path.
            self.current_path.append(event.pos())
            # Schedule a repaint to show the line being drawn in real-time.
            self.update()

    def mouseReleaseEvent(self, event):
        """
        Called when a mouse button is released. Finalizes the current path.
        """
        # Check if the left mouse button was released.
        if event.button() == Qt.MouseButton.LeftButton and self.current_path:
            # Add the finished path to our list of all paths.
            self.paths.append(self.current_path)
            # Clear the current path.
            self.current_path = []

            
    def contextMenuEvent(self, event):
        """
        Called on a right-click. Creates and shows a context menu.
        """
        # Create a context menu.
        context_menu = QMenu(self)
        
        # Create a "Clear" action.
        clear_action = QAction("Clear", self)
        # Connect the action's 'triggered' signal to the clear_drawing method.
        clear_action.triggered.connect(self.clear_drawing)
        # Add the action to the menu.
        context_menu.addAction(clear_action)

        # Add a separator line to the menu.
        context_menu.addSeparator()
        # Create a "Minimize" action.
        minimize_action = QAction("Minimize", self)
        # Connect the action's 'triggered' signal to the widget's showMinimized method.
        minimize_action.triggered.connect(self.showMinimized)
        context_menu.addAction(minimize_action)

        # Add a separator line to the menu.
        context_menu.addSeparator()

        #add a "Screenshot" action.
        query_action = QAction("ask", self)
        query_action.triggered.connect(self.query_gemini)
        context_menu.addAction(query_action)
        context_menu.addSeparator()

        #add askwith screen option
        ask_with_screenshot_action = QAction("ask with screen", self)
        ask_with_screenshot_action.triggered.connect(self.query_gemini_with_screenshot)
        context_menu.addAction(ask_with_screenshot_action)
        context_menu.addSeparator()
        # Create a "Quit" action.
        quit_action = QAction("Quit", self)
        # Connect the action's 'triggered' signal to the application's quit method.
        quit_action.triggered.connect(QApplication.instance().quit)
        context_menu.addAction(quit_action)


        # Show the menu at the position where the user right-clicked.
        context_menu.exec(event.globalPos())

    def clear_drawing(self):
        """
        Clears all drawings from the screen.
        """
        # Clear both the completed paths and any current path.
        self.paths.clear()
        self.current_path.clear()
        # Schedule a repaint to make the screen blank.
        self.update()
    def get_prompt_input(self):
        """
        Creates and shows a modal QInputDialog to get multiline text from the user.
        This is now a method of the class, so it uses 'self' as the parent.
        """
        # CRITICAL: No new QApplication is created here.
        # The dialog's parent is 'self', which is the DrawingOverlay instance.
        dialog = QInputDialog(self)
        
        dialog.setWindowTitle("Enter Your Prompt")
        dialog.setLabelText("Your question for Gemini:")
        dialog.setTextValue("e.g., Explain the marked portion on the screen.")
        dialog.setGeometry(450, 500, 400, 40)
        # Enable multi-line input
        dialog.setOption(QInputDialog.InputDialogOption.UsePlainTextEditForTextInput, True)
        
        # Show the dialog and wait for the user to click OK or Cancel
        # The 'ok' variable will be True if OK was clicked, False otherwise.
        ok = dialog.exec()
        
        if ok:
            return dialog.textValue()
        return None # Return None if the user cancels
    def query_gemini(self):
        """
        Takes a screenshot of the current screen and saves it to a file.
        """
        
        self.prompt = self.get_prompt_input()
        if self.prompt == None or self.prompt.strip() == "":
            print("No prompt provided. Exiting Gemini query.")
            self.prmopt = "explain what is on the screen in 100 words"
            return
        self.typeWriter.clear_text()
        self.typeWriter.show()
        self.typeWriter.activateWindow()
        self.thread = QThread()
        self.worker = GeminiWorker(prompt=self.prompt, model=self.model, temp=0.1, img=self.image)
        self.worker.moveToThread(self.thread)
        #connect start signal to worker's run method
        self.thread.started.connect(self.worker.run)

        #connect worker's chunk_received signal to typewriter's set_text method
        self.worker.chunk_received.connect(self.typeWriter.append_text)
        self.worker.finished.connect(self.worker.deleteLater)
        #connect worker's finished signal to thread's quit method
        self.worker.finished.connect(self.thread.quit)  
        #connect thread's finished signal to worker's deleteLater method

        self.thread.start()
        self.prmopt = "explain what is on the screen in 100 words"
        return 
    def query_gemini_with_screenshot(self):
        """
        Takes a screenshot of the current screen and saves it to a file.
        """
        # Take a screenshot of the entire screen.
        self.image = ImageGrab.grab()
        
        # Now call the Gemini query with the saved screenshot.
        self.query_gemini()

        return

# This is the main entry point of the script.
if __name__ == "__main__":
    # Create the application instance.
    app = QApplication(sys.argv)
    # Create an instance of our custom overlay widget.
    overlay = DrawingOverlay()
    # Start the application's event loop and exit cleanly when it's done.
    sys.exit(app.exec())
