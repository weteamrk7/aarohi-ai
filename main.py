"""
====================================================================
  AAROHI - AI Voice Assistant (WE TEAM RK7)
  Author: Rohith Krishna
  Enhanced & Production-Ready Voice Assistant with Dual Input Mode
====================================================================
"""

import sys
import os
import datetime
import webbrowser
import subprocess

# Ensure UTF-8 output on Windows consoles to prevent UnicodeEncodeError
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia

# Optional joke library support
try:
    import pyjokes
    HAS_PYJOKES = True
except ImportError:
    HAS_PYJOKES = False

# Global flag to track if microphone is active
MIC_AVAILABLE = True

# ==================================================================
# 1. INITIALIZE SPEECH RECOGNITION & TTS ENGINE
# ==================================================================
listener = sr.Recognizer()
listener.energy_threshold = 300
listener.dynamic_energy_threshold = True

engine = pyttsx3.init()

# Configure Voice: Select female voice for "Aarohi" if available
try:
    voices = engine.getProperty('voices')
    female_voice_selected = False
    if voices:
        for voice in voices:
            if "zira" in voice.name.lower() or "female" in voice.name.lower() or "hazel" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                female_voice_selected = True
                break
        if not female_voice_selected and len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        elif not female_voice_selected and len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
except Exception as e:
    print(f"[Voice Init Note]: Using default system voice ({e})")

# Set natural speech rate and volume
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)


# ==================================================================
# 2. CORE AUDIO FUNCTIONS (TALK & LISTEN)
# ==================================================================
def talk(text: str):
    """Speaks out the given text using TTS and prints to console."""
    print(f"\n🤖 Aarohi: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS Error]: {e}")


def take_command(require_wake_word: bool = False) -> str:
    """
    Listens to microphone input or falls back to text input if mic is unavailable.
    Handles ambient noise, timeouts, and unknown speech cleanly without crashing.
    """
    global MIC_AVAILABLE
    command = ""

    if not MIC_AVAILABLE:
        try:
            command = input("\n💬 Type your command (or 'exit' to quit): ").strip().lower()
            return command
        except (KeyboardInterrupt, EOFError):
            return "exit"

    try:
        with sr.Microphone() as source:
            print("\n" + "-" * 50)
            print("🎧 Calibrating background noise...")
            listener.adjust_for_ambient_noise(source, duration=0.8)
            listener.pause_threshold = 0.8
            print("🎙️  Listening... Speak now!")

            # Listen with safety timeouts to avoid hanging indefinitely
            audio = listener.listen(source, timeout=6, phrase_time_limit=10)

            print("⏳ Processing speech...")
            command = listener.recognize_google(audio, language="en-IN")
            command = command.lower().strip()
            print(f"👤 You said: \"{command}\"")

            # Check for wake word
            wake_words = ['aarohi', 'arohi', 'hey aarohi', 'alexa', 'aarohee']
            matched_wake_word = any(w in command for w in wake_words)

            if matched_wake_word:
                for w in wake_words:
                    command = command.replace(w, '').strip()
            elif require_wake_word:
                return ""

    except sr.WaitTimeoutError:
        print("⏳ No speech detected (listening timed out).")
        return ""
    except sr.UnknownValueError:
        print("❓ Could not understand audio. Please speak clearly.")
        return ""
    except sr.RequestError as e:
        print(f"⚠️ Speech Recognition Service Error: {e}")
        talk("Sorry, speech recognition is currently unavailable. Please check your internet connection.")
        return ""
    except (OSError, AttributeError) as e:
        print(f"\n⚠️ Microphone not detected or PyAudio error: {e}")
        print("👉 Switching to interactive Text Mode for this session.")
        MIC_AVAILABLE = False
        return take_command(require_wake_word)
    except Exception as e:
        print(f"⚠️ Audio Error: {e}")
        return ""

    return command


# ==================================================================
# 3. GREETING ON STARTUP
# ==================================================================
def wish_user():
    """Greets the user according to the current time of day."""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 17:
        greeting = "Good afternoon!"
    elif 17 <= hour < 21:
        greeting = "Good evening!"
    else:
        greeting = "Hello!"

    talk(f"{greeting} I am Aarohi, your AI voice assistant from WE TEAM RK7. How can I help you today?")


# ==================================================================
# 4. COMMAND EXECUTION ENGINE
# ==================================================================
def execute_command(command: str) -> bool:
    """
    Executes an action based on the recognized command.
    Returns False when the user commands the assistant to exit, True otherwise.
    """
    if not command:
        return True

    # 1. Play Music / YouTube Video
    if 'play' in command:
        song = command.replace('play', '').strip()
        if song:
            talk(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            talk("What would you like me to play on YouTube?")

    # 2. Time Query
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {current_time}")

    # 3. Date / Day Query
    elif 'date' in command or 'day' in command or 'today' in command:
        today_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        talk(f"Today is {today_date}")

    # 4. Wikipedia / Information Lookup
    elif any(q in command for q in ['who is', 'what is', 'tell me about', 'wikipedia']):
        query = command
        for phrase in ['who is', 'what is', 'tell me about', 'wikipedia']:
            query = query.replace(phrase, '')
        query = query.strip()

        if query:
            try:
                talk(f"Searching Wikipedia for {query}...")
                wikipedia.set_lang("en")
                info = wikipedia.summary(query, sentences=2)
                talk(info)
            except wikipedia.exceptions.DisambiguationError:
                talk(f"There are multiple topics matching '{query}'. Could you please be more specific?")
            except wikipedia.exceptions.PageError:
                talk(f"Sorry, I couldn't find any Wikipedia page matching '{query}'.")
            except Exception:
                talk("Sorry, I encountered an error while searching Wikipedia.")
        else:
            talk("Who or what would you like me to search for on Wikipedia?")

    # 5. Search on Google
    elif 'search' in command or 'google' in command:
        search_query = command.replace('search for', '').replace('search', '').replace('google', '').strip()
        if search_query:
            talk(f"Searching Google for {search_query}")
            pywhatkit.search(search_query)
        else:
            talk("What would you like me to search on Google?")

    # 6. Open Popular Websites
    elif 'open youtube' in command:
        talk("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in command:
        talk("Opening Google")
        webbrowser.open("https://www.google.com")

    elif 'open github' in command:
        talk("Opening GitHub")
        webbrowser.open("https://www.github.com")

    # 7. Open Windows Applications
    elif 'open notepad' in command:
        talk("Opening Notepad")
        try:
            subprocess.Popen(['notepad.exe'])
        except Exception:
            talk("Could not open Notepad.")

    elif 'open calculator' in command or 'calc' in command:
        talk("Opening Calculator")
        try:
            subprocess.Popen(['calc.exe'])
        except Exception:
            talk("Could not open Calculator.")

    # 8. Tell a Joke
    elif 'joke' in command:
        if HAS_PYJOKES:
            joke = pyjokes.get_joke()
            talk(joke)
        else:
            jokes_list = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "There are 10 types of people in the world: those who understand binary, and those who don't.",
                "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
                "Why did the computer go to the doctor? Because it had a virus!"
            ]
            import random
            talk(random.choice(jokes_list))

    # 9. Identity & Creator (Rohith Krishna & WE TEAM RK7)
    elif 'who built you' in command or 'who made you' in command or 'who created you' in command:
        talk("I was built by Rohith Krishna, who is the founder and CEO of WE TEAM RK7.")

    # 10. Pleasantries & Small Talk
    elif 'how are you' in command:
        talk("I'm doing great, thank you! How can I assist you today?")

    elif 'hai' in command or 'hello' in command or 'hey' in command:
        talk("Hello! How can I help you?")

    elif 'greet my friends' in command or 'introduce yourself' in command:
        speech = (
            "Good afternoon all! I am Aarohi, the AI Assistant of WE TEAM RK7. "
            "The Technical Team is a multidisciplinary team that includes experts in all core technology values. "
            "WE TEAM RK7 aims to provide high quality information across technology domains, "
            "building upcoming courses and projects to enable everyone to learn without spending a single penny. "
            "Thank you, Jai Hind!"
        )
        talk(speech)

    # 11. Exit / Shutdown Assistant
    elif any(exit_word in command for exit_word in ['stop', 'exit', 'quit', 'bye', 'goodbye', 'shutdown', 'sleep']):
        talk("Goodbye! Have a fantastic day ahead. Signing off from WE TEAM RK7.")
        return False

    # 12. Fallback for unrecognized commands
    else:
        talk(f"I heard '{command}', but I am not sure how to handle that yet. You can ask me to play a song, tell the time, search Wikipedia, open apps, or tell a joke!")

    return True


# ==================================================================
# 5. MAIN LOOP
# ==================================================================
def run_aarohi():
    """Main execution loop for Aarohi AI Assistant."""
    print("=" * 65)
    print("           🌟 AAROHI - AI VOICE ASSISTANT 🌟           ")
    print("                   WE TEAM RK7                         ")
    print("=" * 65)
    print("💡 Example Commands:")
    print("  • 'Play Believer on YouTube'")
    print("  • 'What is the time?'")
    print("  • 'What is today's date?'")
    print("  • 'Who is Albert Einstein?' / 'Tell me about Artificial Intelligence'")
    print("  • 'Search for Python tutorials'")
    print("  • 'Tell me a joke'")
    print("  • 'Open YouTube' / 'Open GitHub' / 'Open Notepad'")
    print("  • 'Who built you?'")
    print("  • 'Greet my friends'")
    print("  • 'Exit' / 'Stop' / 'Bye'")
    print("=" * 65)

    wish_user()

    # Continuous listening loop
    while True:
        try:
            command = take_command(require_wake_word=False)
            if command:
                keep_running = execute_command(command)
                if not keep_running:
                    break
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down Aarohi. Goodbye!")
            talk("Goodbye!")
            break
        except Exception as e:
            print(f"\n[Unexpected Error]: {e}")
            continue


if __name__ == "__main__":
    # Check if user passed --text flag
    if len(sys.argv) > 1 and sys.argv[1].lower() in ['--text', '-t', 'text']:
        MIC_AVAILABLE = False
        print("⌨️  Running Aarohi in Text/Console Mode.")
    run_aarohi()
