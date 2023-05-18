import speech_recognition as sr
import pyttsx3
import time
import requests
import random
import webbrowser


# Сколько определений слова показывать и называть
choice = int(input('How many definitions should NIKRA show you( enter a number or zero (0) to show all defenitions):\n'))
engine = pyttsx3.init()
newVoiceRate = 176
voices = engine.getProperty('voices')
engine.setProperty('voices', 'en')

for voice in voices:
    if voice.name == 'Shelley (English (UK))':
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', newVoiceRate)


def talk(say):
    engine.say(say)
    engine.runAndWait()


def greetings():
    '''
    Приветствие ассистента
    '''
    talk('Hello, My name is NIKRA, I am your personal voice assistant.')
    talk('My goal is to help you find everything about every word')
    talk('I can open a webpage of the word on the WikiDictionary, play the proper pronunciation, tell you the meaning of the word or example of its usage.')
    talk('Just tell me: find a word. For example, find a bike, find an apple.' )


r = sr.Recognizer()


def listening():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('Listening...')
            voice = r.listen(source)
            command = r.recognize_google(voice)

    except:
            return
    return command


def asking_commands():
    '''
    Получение команд для нашего слова
    '''
    talk('Do you want to open the webpage, listen the pronunciation,  get a meaning or  an example?')
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
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
        if 'exit' or 'stop' in command:
            return 5
    except:
        pass


def getting_the_word():
    while True:
        speech = listening()
        if speech == None:
            continue
        if 'exit' in speech:
            exit()
        if 'find an' in speech:
            return speech.replace('find an ', '')
        elif 'find a' in speech:
            return speech.replace('find a ', '')

def NIKRA(choice):
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
                talk('Playing the pronunciation and showing the transcription')
                print(trnscr)
                webbrowser.open_new_tab(url)
        case 3:
            # Случай, когда в API выдает информацию о слове (которое может быть и глаголом, и существительным)
            # В виде списка с информацией о нескольких паронимах
            if defnmbr > 1:
                # Цикл для того, чтобы была возможность узнать каждое значение
                while True:
                    talk(f'The word "{rqst}" has {defnmbr} meaning(s)')
                    option = int(input(f'Enter one (number from 1 to {defnmbr}) you want to know about:\n')) - 1
                    # Иногда слово может быть представлено разными частями речи, при разных определениях.
                    # Поэтому необходим доп. цикл
                    for j in range(len(meanings[option])):
                        dfnts = meanings[option][j]["definitions"]
                        talk(f'Definitions of the word "{rqst}" as a {meanings[option][j]["partOfSpeech"]}')
                        if choice == 0:
                            choice = len(dfnts)
                        for i in range(choice):
                            print(f'**', dfnts[i]["definition"], '**' + '\n')
                            talk(dfnts[i]["definition"])
                            time.sleep(0.5)
                    # Чтобы человек мог узнать все значения слова
                    talk('Want to hear another meaning (Yes or Not)?')
                    rpl = listening()
                    if rpl == None:
                        pass
                    elif 'yes' in rpl:
                        NIKRA(choice)
                    elif 'not' in rpl:
                        break
            # Случай, когда у слова нет значения
            elif len(meanings) == 0:
                talk("Sorry, couldn't find the definition")
            # Случай, когда слово имеет одно значение
            else:
                if choice == 0:
                    choice = len(meanings[0])
                print(choice)
                for j in range(len(meanings[0])):
                    dfnts = meanings[0][j]["definitions"]
                    talk(f'Definitions of the word "{rqst}" as a {meanings[0][j]["partOfSpeech"]}')
                    for i in range(0, choice):
                        print(f'**', dfnts[i]["definition"], '**' + '\n')
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
            if len(example) == 0:
                talk('Sorry, couldn\'t find an example')
            else:
                # Берем случайный пример
                exmnb = random.randint(0, len(example)-1)
                print(f'\n{example[exmnb]}\n')
                talk(example[exmnb])
        case 5:
            quit()
        
              
#greetings()
while True:
    talk('To stop this programm, say exit' )
    rqst = getting_the_word()
    NIKRA(choice)
    while True:
        talk('Want to try another option (Yes or Not)?')
        answr = listening()
        if answr == None:
            pass
        elif 'yes' in answr:
            NIKRA(choice)
        elif 'not' in answr:
            break
