from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from time import sleep
from PyQt6.QtCore import QObject, pyqtSignal
load_dotenv()
GOOGLE_API_KEY= os.getenv('GEMINI_API_KEY')

system_prompt = """ 
yoy are a helpful assistant.

"""

class GeminiWorker(QObject):
    """
    A worker that runs the Gemini API call in a separate thread.
    """
    # Signal to emit a chunk of text when it's received
    chunk_received = pyqtSignal(str)
    # Signal to emit when the entire process is finished
    finished = pyqtSignal()

    def __init__(self,prompt: str, img = None,  model: str = "gemini-1.5-flash", temp : float = 0.1):
        super().__init__()
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model = model
        self.prompt = prompt
        self.img = img
        self.temp = temp
        self.is_running = True
        self.system_prompt = ''''''

    def run(self):
        """Generates text and emits chunks."""
        # This is the blocking call, but it's now in a background thread
        con = []
        if self.img is not None:
            con.append(self.img)
        con.append(self.prompt)
        response = self.client.models.generate_content_stream(
            model= self.model,
            contents= con,
            config=types.GenerateContentConfig(
                temperature= self.temp,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                system_instruction= self.system_prompt
                
            )
        )
        
        for chunk in response:
            if not self.is_running:
                break
            if chunk.text:
                # Emit each piece of text as it arrives
                self.chunk_received.emit(chunk.text)
        
        # Signal that the work is done
        self.finished.emit()

if __name__ == "__main__":
    pass