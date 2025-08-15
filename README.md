# 👁️✨ Gemini Lens

**Ask questions about anything on your screen.**  
Gemini Lens is a desktop tool that lets you draw on your screen, capture it, and get AI-powered explanations about the content.

A demonstration of Gemini Lens analyzing a code snippet.

---

## 🚀 Key Features

- **Screen Overlay Canvas** – Draw and annotate anywhere on your screen with a simple, transparent overlay.
- **Multimodal AI Queries** – Uses Google's Gemini Pro Vision to understand both your text prompts and screen captures.
- **Context-Aware Analysis** – Get explanations for code, text, images, or any visual element on your screen.
- **Real-time Responses** – AI-generated answers are streamed back with a typewriter effect for an interactive experience.
- **Simple & Intuitive UI** – A clean, minimal interface accessed via a right-click menu.

---

## 🤔 How It Works

1. **Activate & Draw** – Run the application to enable the transparent overlay. Use your mouse to draw a circle, arrow, or any annotation over the content you want to ask about.  
2. **Ask with Screen** – Right-click to open the context menu and select **"ask with screen"**.  
3. **Enter Your Prompt** – A dialog box will appear. Type your question (e.g., *"What does this function do?"* or *"Summarize this article"*).  
4. **Get an Instant Answer** – The tool captures your screen (with your drawings), sends it to the Gemini API along with your prompt, and displays the AI's response in a new window.

---

## 🛠️ Installation & Setup

Follow these steps to get **Gemini Lens** running on your local machine.

### 1. Prerequisites
- Python **3.9** or newer
- A Google AI API Key – You can get one from [Google AI Studio](https://aistudio.google.com/)

### 2. Clone the Repository
```bash
git clone https://github.com/lubaid-01/Gemini-Lens.git
cd gemini-lens
```
### 3. Set Up a Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

### macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
4. Install Dependencies
From requirements.txt:
```bash
pip install -r requirements.txt
```
If you don't have a requirements.txt file, you can create one with:
```bash
PyQt6
Pillow
google-generativeai
python-dotenv
```
Or install manually:
```bash
pip install PyQt6 Pillow google-generativeai python-dotenv
```
5. Configure Your API Key

Create a file named .env in the root directory of the project and add:
```bash
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```
Ensure your gemini.py script loads this key.


▶️ How to Use

Run the main application script:
```bash
python main.py
```

# 🔐Controls:

- **Left-click & drag – Draw on the screen**
- **Right-click – Open the menu:**
- **Clear – Erase all drawings**
- **Minimize – Hide the application window**
-**ask – Send a text-only prompt to the AI**
- **ask with screen – Capture the screen and send it with a prompt to the AI**
- **Quit – Close the application**

# 🙏 Acknowledgements

- **Built with the powerful PyQt6 framework.**
- **Image processing handled by Pillow.**
- **AI capabilities powered by Google's Gemini API.**
