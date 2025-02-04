import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Set the voice (0 for male, 1 for female)
engine.setProperty('voice', voices[0].id)  # or voices[1].id for female
engine.say("Hello, this is a test.")
engine.runAndWait()
