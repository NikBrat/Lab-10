import speech_recognition as sr
import pyttsx3
import time
import requests

engine = pyttsx3.init()
newVoiceRate = 176

voices = engine.getProperty('voices')
engine.setProperty('voices', 'en')

for voice in voices:
    if voice.name == 'Shelley (English (UK))':
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', newVoiceRate)

r = sr.Recognizer()

def greetings():
    engine.say('Hello, My name is NIKRA, I am your personal assistant.')
    engine.say('My goal is to help you find everything about every word')
    engine.say('I can open a webpage of the word on the WikiDictionary, play the proper pronunciation.')
    engine.say('tell you the meaning of the word or give you an example of its usage.' )
    engine.say('Just tell me: find a word. For example, find a bike, find an apple.' )
    engine.runAndWait()


def talk(say):
    engine.say(say)
    engine.runAndWait()


def listening():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            time.sleep(1.5)
            print('Listening...')
            voice = r.listen(source)
            command = r.recognize_google(voice)
    except:
        engine.say("Sorry, I could not recognize what you said.")
    yield command


def asking_commands():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            time.sleep(1.5)
            print('Listening...')
            voice = r.listen(source)
            command = r.recognize_google(voice, duration=15)
    except:
        pass
    yield command


def NIKRA():
    speech = listening()
    if 'find a' in speech:
        rqst = speech.replace('find a ', '')
    elif 'find an' in speech:
        rqst = speech.replace('find a ', '')
    
    
