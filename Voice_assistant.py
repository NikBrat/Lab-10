import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
newVoiceRate = 180

voices = engine.getProperty('voices')
engine.setProperty('voices', 'en')

for voice in voices:
    if voice.name == 'Shelley (English (UK))':
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', newVoiceRate)

r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.listen()

def greetings():
    engine.say('Hello, I am personal assistant in learning new about every word')


def talk(say):
    engine.say(say)
    engine.runAndWait()


