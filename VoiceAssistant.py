import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random
import os

class VoiceAssistant:
    def __init__(self):
        # Set assistant name FIRST
        self.name = "Assistant"
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
            self.setup_voice()
            print(f"Hello! I'm your {self.name}. Say 'hello' to start!")
        except Exception as e:
            print(f"Error initializing TTS engine: {e}")
            print("TTS might not work, but speech recognition should still function.")
            self.tts_engine = None
    
    def setup_voice(self):
        """Configure the text-to-speech engine"""
        if not self.tts_engine:
            return
            
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            
            # Use female voice if available
            if voices and len(voices) > 1:
                self.tts_engine.setProperty('voice', voices[1].id)
            
            # Set speech rate (words per minute)
            self.tts_engine.setProperty('rate', 200)
            
            # Set volume (0.0 to 1.0)
            self.tts_engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"Warning: Could not configure voice settings: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
        else:
            print("(TTS not available - text only)")
    
    def listen(self):
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5)
            
            print("Processing...")
            # Convert speech to text
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
            
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that. Could you repeat?")
            return None
        except sr.RequestError as e:
            self.speak(f"Sorry, there's an issue with the speech service: {e}")
            return None
        except sr.WaitTimeoutError:
            print("Listening timeout - no speech detected")
            return None
        except Exception as e:
            print(f"Unexpected error in listen(): {e}")
            return None
    
    def get_current_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}"
    
    def get_current_date(self):
        """Get current date"""
        today = datetime.date.today()
        date_str = today.strftime("%B %d, %Y")
        return f"Today is {date_str}"
    
    def search_web(self, query):
        """Search the web"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return f"Searching for {query} on Google"
        except Exception as e:
            return f"Sorry, couldn't open browser: {e}"
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the math book look so sad? Because it had too many problems!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? He was outstanding in his field!"
        ]
        return random.choice(jokes)
    
    def process_command(self, command):
        """Process voice commands and respond accordingly"""
        if not command:
            return True
        
        # Greeting
        if any(word in command for word in ['hello', 'hi', 'hey']):
            greetings = [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! I'm here to assist you!"
            ]
            self.speak(random.choice(greetings))
        
        # Time
        elif any(word in command for word in ['time', 'clock']):
            response = self.get_current_time()
            self.speak(response)
        
        # Date
        elif any(word in command for word in ['date', 'today', 'day']):
            response = self.get_current_date()
            self.speak(response)
        
        # Web search
        elif 'search' in command or 'google' in command:
            # Extract search query
            if 'search for' in command:
                query = command.split('search for', 1)[1].strip()
            elif 'search' in command:
                query = command.split('search', 1)[1].strip()
            elif 'google' in command:
                query = command.split('google', 1)[1].strip()
            else:
                query = "python programming"
            
            if query:
                response = self.search_web(query)
                self.speak(response)
            else:
                self.speak("What would you like me to search for?")
        
        # Joke
        elif any(word in command for word in ['joke', 'funny', 'laugh']):
            joke = self.tell_joke()
            self.speak(joke)
        
        # Exit commands
        elif any(word in command for word in ['bye', 'goodbye', 'exit', 'quit', 'stop']):
            self.speak("Goodbye! Have a great day!")
            return False
        
        # Weather (placeholder - would need weather API)
        elif 'weather' in command:
            self.speak("I would need a weather API to check the weather. For now, you can search for weather online!")
        
        # Name
        elif any(word in command for word in ['name', 'who are you']):
            self.speak(f"I'm your voice assistant. You can call me {self.name}!")
        
        # Help
        elif 'help' in command:
            help_text = """Here's what I can do:
            Say hello to greet me, ask for the time or date, ask me to search for something, 
            ask me to tell a joke, or say goodbye to exit"""
            self.speak(help_text)
        
        # Default response
        else:
            responses = [
                "I'm not sure how to help with that. Try asking for the time, date, or say 'help' for more options.",
                "I didn't understand that command. You can ask me about time, date, search, or jokes!",
                "Sorry, I don't know how to do that yet. Ask me for help to see what I can do."
            ]
            self.speak(random.choice(responses))
        
        return True
    
    def run(self):
        """Main loop to run the voice assistant"""
        self.speak(f"Voice assistant activated! Say something to get started.")
        
        while True:
            try:
                # Listen for command
                command = self.listen()
                
                # Process command
                continue_running = self.process_command(command)
                
                # Exit if user said goodbye
                if continue_running == False:
                    break
                    
            except KeyboardInterrupt:
                print("\nKeyboard interrupt detected.")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                self.speak("Sorry, something went wrong. Let me try again.")

# Test if packages are installed
def test_imports():
    """Test if all required packages are available"""
    try:
        import speech_recognition as sr
        print("✓ speech_recognition imported successfully")
    except ImportError:
        print("✗ speech_recognition not found. Run: pip install speechrecognition")
        return False
    
    try:
        import pyttsx3
        print("✓ pyttsx3 imported successfully")
    except ImportError:
        print("✗ pyttsx3 not found. Run: pip install pyttsx3")
        return False
    
    try:
        import pyaudio
        print("✓ pyaudio imported successfully")
    except ImportError:
        print("✗ pyaudio not found. Run: pip install pyaudio")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing imports...")
    if test_imports():
        print("\nAll packages available! Starting voice assistant...")
        try:
            # Create and run the voice assistant
            assistant = VoiceAssistant()
            assistant.run()
        except Exception as e:
            print(f"Failed to start assistant: {e}")
    else:
        print("\nPlease install missing packages and try again.")