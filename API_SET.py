import requests
import webbrowser
import random


rqst = input('Enter your word:\n')
# Вызов API
api = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + rqst
answer = requests.get(api).json()

# На случай ввода неправильного слова
try:
    a = answer["title"]
except TypeError:
    pass
else:
    print(f'Cannot find the word "{rqst}". Try another one.')
    quit()

# Значение слова
meanings = []
defnmbr = len(answer)
for word in answer:
    meanings.append(word["meanings"])

a = int(input('What are you looking for(Enter a number): 1 - dictionary webpage, 2 - transcription and pronunciation, 3 - meaning, 4 - example:\n'))
match a:
    case 1:
        # Ссылка на страницу слова в словаре
        url = answer[0]["sourceUrls"][0]
        webbrowser.open_new_tab(url)
    case 2:
        # Транскрипция и произношение слова (требует доработки)
        trnscr = answer[0]["phonetic"]
        # На случай отсутсвия транскрипции
        if trnscr == "":
            print('Sorry, transcription is not available.')
        else:
            print(f'\nТranscription: {trnscr}')
        phntcs = answer[0]["phonetics"]
        # Нахождение url аудиозаписи
        for i in range(len(phntcs)):
            url = phntcs[i]["audio"]
            if url != "":
                break
        # На случай отсутствия аудиозаписи
        if url == "":
            print('Sorry, audio is not available.')
        else:
            webbrowser.open_new_tab(url)
    case 3:
        # Случай, когда в API выдает информацию о слове (которое может быть и глаголом, и существительным)
        # В виде списка с информацией о нескольких паронимах
        if defnmbr > 1:
            print(f'The word "{rqst}" has {defnmbr} meaning(s):')
            option = int(input(f'Сhoose the one (number from 1 to {defnmbr}) you want to know about:\n')) - 1
            # Иногда слово может быть представлено разными частями речи, при разных определениях.
            # Поэтому необходим доп. цикл
            for j in range(len(meanings[option])):
                dfnts = meanings[option][j]["definitions"]
                print(f'\nDefinitions of the word "{rqst}" as a {meanings[option][j]["partOfSpeech"]}:\n')
                for i in range(0, len(dfnts)):
                    print(f'**', dfnts[i]["definition"], '**' + '\n')
        # Случай, когда у слова нет значения
        elif len(meanings) == 0:
            print("Sorry, couldn't find the definition")
        # Случай, когда слово имеет одно разные значения 
        else:
            print(f'Definitions of the word "{rqst}":\n')
            for j in range(len(meanings[0])):
                dfnts = meanings[0][j]["definitions"]
                print(f'Definitions of the word "{rqst}" as a {meanings[0][j]["partOfSpeech"]}:\n')
                for i in range(0, len(dfnts)):
                    print(f'**', dfnts[i]["definition"], '**' + '\n')
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
        print(example[exmnb])