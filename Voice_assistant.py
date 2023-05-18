import speech_recognition as sr
import pyttsx3
import time
import requests
import random
import webbrowser

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
        talk("Sorry, I could not recognize what you said.")
    return command



def asking_commands():
    talk('Do you want to open the webpage, listen the pronunciation,  get a meaning or  an example?')
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            time.sleep(1.5)
            print('Waiting for the command...')
            voice = r.listen(source)
            command = r.recognize_google(voice)
        if 'webpage' in command:
            return 1
        if 'pronunciation' in command:
            return 2
        if 'meaning' in command:
            return 3
        if 'example' in command:
            return 4
    except:
        pass


def NIKRA():
    # Вызов API
    api = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + rqst
    answer = requests.get(api).json()
    # На случай ввода неправильного слова
    try:
        a = answer["title"]
    except TypeError:
        pass
    else:
        talk(f'Cannot find the word "{rqst}". Try another one.')
        return
    # Значение слова
    meanings = []
    defnmbr = len(answer)
    for word in answer:
        meanings.append(word["meanings"])
    a = asking_commands()
    match a:
        case 1:
            # Ссылка на страницу слова в словаре
            url = answer[0]["sourceUrls"][0]
            webbrowser.open_new_tab(url)
        case 2:
            # Транскрипция и произношение слова 
            trnscr = answer[0]["phonetic"]
            # На случай отсутсвия транскрипции
            phntcs = answer[0]["phonetics"]
            # Нахождение url аудиозаписи
            for i in range(len(phntcs)):
                url = phntcs[i]["audio"]
                if url != "":
                    break
            # На случай отсутствия аудиозаписи
            if url == "":
                talk('Sorry, audio is not available.')
            else:
                talk('Playing the pronuciation')
                time.sleep(1)
                webbrowser.open_new_tab(url)
        case 3:
            # Случай, когда в API выдает информацию о слове (которое может быть и глаголом, и существительным)
            # В виде списка с информацией о нескольких паронимах
            if defnmbr > 1:
                talk(f'The word "{rqst}" has {defnmbr} meaning(s)')
                option = int(input(f'Сhoose the one (number from 1 to {defnmbr}) you want to know about:\n')) - 1
                # Иногда слово может быть представлено разными частями речи, при разных определениях.
                # Поэтому необходим доп. цикл
                for j in range(len(meanings[option])):
                    dfnts = meanings[option][j]["definitions"]
                    talk(f'Definitions of the word "{rqst}" as a {meanings[option][j]["partOfSpeech"]}')
                    for i in range(0, len(dfnts)):
                        talk(dfnts[i]["definition"])
                        time.sleep(0.5)
            # Случай, когда у слова нет значения
            elif len(meanings) == 0:
                talk("Sorry, couldn't find the definition")
            # Случай, когда слово имеет одно разные значения 
            else:
                for j in range(len(meanings[0])):
                    dfnts = meanings[0][j]["definitions"]
                    talk(f'Definitions of the word "{rqst}" as a {meanings[0][j]["partOfSpeech"]}')
                    for i in range(0, len(dfnts)):
                        talk(dfnts[i]["definition"])
        case 4:
            example = []
            # Создаем массив со всеми примерами
            for word in answer:
                for definitions in word["meanings"]:
                    for definition in definitions["definitions"]:
                        try:
                                example.append(definition["example"])
                        except:
                            continue
            # Берем случайный пример
            exmnb = random.randint(0, len(example)-1)
            talk(example[exmnb])
        

                
greetings()
while True:
    speech = listening()
    if 'find a' in speech:
        rqst = speech.replace('find a ', '')
    elif 'find an' in speech:
        rqst = speech.replace('find a ', '')
    if rqst == '':
        talk(f'Did not hear the word. Say again.')
        continue
    else:
        NIKRA()

