 Voice Assistant – Date & Time

A simple Python-based voice assistant that responds with the current date and time using speech recognition and text-to-speech libraries. A great beginner project to explore Python automation, speech processing, and voice interaction.

 Features:

Listens for user voice commands

Responds with the current date or current time

Uses Text-to-Speech (TTS) to speak responses

Lightweight and easy to run locally

Good introduction to voice-controlled Python applications

 Technologies Used:

Python 3

speech_recognition – for capturing and interpreting voice input

pyttsx3 – for text-to-speech output

datetime – for fetching date and time

pyaudio – (used by speech_recognition)

How It Works:

The program uses your microphone to listen for voice input.

Converts your voice to text using Google's speech recognition API.

Based on keywords like "date" or "time", it fetches the appropriate info.

Uses text-to-speech to respond aloud.

 Future Improvements:

Add more commands (weather, jokes, reminders, etc.)

Wake word detection (e.g., “Hey Assistant”)

GUI interface using Tkinter or PyQt

Add error handling for ambient noise or unclear commands
