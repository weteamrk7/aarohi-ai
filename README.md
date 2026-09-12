# 🎙️ Aarohi - AI Voice Assistant (WE TEAM RK7)

An intelligent, interactive Python voice assistant built for **WE TEAM RK7** (founded by **Rohith Krishna**). Aarohi can play YouTube videos, answer general knowledge questions via Wikipedia, tell time/date, search Google, launch apps, tell jokes, and introduce the team mission.

---

## 🛠️ Issues in the Original Code & Fixes Applied

| # | Original Issue | How It Was Fixed |
|---|----------------|-------------------|
| 1 | **`UnboundLocalError` in `take_command()`**<br>`command` was only assigned inside `try:`. If an exception occurred, `except: pass` left `command` undefined, crashing the script on `return command`. | Initialized `command = ""` beforehand and handled specific speech recognition exceptions gracefully. |
| 2 | **Single-Run Execution**<br>`run_alexa()` ran only once and exited immediately. | Converted the execution loop to a continuous `while True:` loop with graceful exit commands (`stop`, `exit`, `quit`, `bye`). |
| 3 | **Crashes on Unrecognized Speech / None**<br>If speech was not recognized or empty, `'play' in command` would cause unexpected behavior. | Added safety check `if not command: return` and fallback handling. |
| 4 | **Missing Spacing in Speech Concatenations**<br>`talk('playing' + song)` produced `"playingfaded"` with no spaces. | Replaced string concatenation with formatted strings: `talk(f"Playing {song} on YouTube")`. |
| 5 | **Wikipedia Exceptions Crashing Script**<br>Queries with multiple results or missing pages crashed with `DisambiguationError` or `PageError`. | Added `try...except` blocks around `wikipedia.summary()` to handle ambiguous or missing topics cleanly. |
| 6 | **Ambient Noise & Freezing**<br>Microphone had no ambient noise calibration or timeout, causing it to hang indefinitely in noisy rooms or silence. | Added `listener.adjust_for_ambient_noise()` and configured `timeout=6, phrase_time_limit=10`. |
| 7 | **Voice Selection & Speed**<br>Hardcoded `voices[0]` was often male or robotic. Rate was set to a slow 130. | Added automated detection for female voice (e.g., *Microsoft Zira* for Aarohi) and set speed to a natural 160 wpm. |
| 8 | **No Fallback / Text Mode**<br>If a microphone was not plugged in or PyAudio was missing, the program crashed with `OSError`. | Added automatic fallback to **Interactive Text Mode** (`--text`), allowing testing without a microphone. |

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.8 to 3.12 installed on your system.

### 2. Install Required Packages
Open your terminal in this directory and run:

```bash
pip install -r requirements.txt
```

> **Note for Windows Users (PyAudio):**
> If `pip install pyaudio` gives an error about C++ build tools, run:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

---

## 💻 How to Run

### Option 1: Voice Mode (Microphone)
```bash
python main.py
```

### Option 2: Text / Console Mode (No Microphone Needed)
```bash
python main.py --text
```

---

## 🗣️ Supported Commands & Features

| Action | Example Voice Command |
|---|---|
| 🎵 **Play YouTube Music** | *"Play Believer"*, *"Play Shape of You"* |
| 🕒 **Current Time** | *"What is the time?"*, *"Tell me time"* |
| 📅 **Current Date & Day** | *"What is today's date?"*, *"Which day is today?"* |
| 📖 **Wikipedia Lookup** | *"Who is Elon Musk?"*, *"What is Artificial Intelligence?"* |
| 🔍 **Google Search** | *"Search for Python programming tutorials"*, *"Google weather today"* |
| 🌐 **Open Websites** | *"Open YouTube"*, *"Open Google"*, *"Open GitHub"* |
| 🖥️ **Open Desktop Apps** | *"Open Notepad"*, *"Open Calculator"* |
| 😂 **Tell Jokes** | *"Tell me a joke"*, *"Make me laugh"* |
| 🏢 **Creator Info** | *"Who built you?"*, *"Who is your founder?"* |
| 🤝 **Team Introduction** | *"Greet my friends"*, *"Introduce yourself"* |
| 👋 **Exit Assistant** | *"Exit"*, *"Stop"*, *"Quit"*, *"Bye"* |

---

## 📁 Project Structure
```text
aarohi_voice_assistant/
├── main.py              # Main assistant source code (voice + text engine)
├── requirements.txt     # Python library dependencies
└── README.md            # Documentation and user guide
```

---

## 🌟 WE TEAM RK7
Created and designed under the leadership of **Rohith Krishna**.
