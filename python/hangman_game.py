import random
with open('/Users/mitya/Downloads/russian_nouns_v2/russian_nouns.txt') as file:
    words = [i.strip('\n') for i in file.readlines()]
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
guessed_letters = ''
print('Привет!')
print('Давай сыграем в игру "Висилица"?')
print('Правила такие:')
print('1. Я загадываю слово, говорю сколько в нем букв')
print('2. Ты называешь букву')
print('3. Если буква встречается в слове, я ее открываю (как в Поле Чудес)')
print('4. Если буквы нет, рисую часть тела человечка')
print('5. Если ты угадаешь слово быстрее, чем я нарисую человечка — ты выиграл')
print('6. Если быстрее буду я, то победа моя!')
print('')
print('Готов? (напиши да/нет)')


def word_generator(answer):
    while answer != 'да' and answer != 'нет':
        print('Ты ошибся! Напиши "да", чтобы сыграть или "нет", чтобы выйти')
        answer = input().lower()
    if answer == 'да':
        word = random.choice(words)
        return word
    elif answer == 'нет':
        print('Как передумаешь — возвращайся')
        return 'До скорого'


def open_letter(def_letter):
    for i in range(len(hidden_word)):
        if hidden_word[i] == def_letter:
            guessed_word[i] = hidden_word[i]


def display_hangman(def_tries):
    stages = [  # финальное состояние: голова, торс, обе руки, обе ноги
        '''
           --------
           |      |
           |      O
           |     /|\\
           |      |
           |     / \\
           -
        ''',
        # голова, торс, обе руки, одна нога
        '''
           --------
           |      |
           |      O
           |     /|\\
           |      |
           |     / 
           -
        ''',
        # голова, торс, обе руки
        '''
           --------
           |      |
           |      O
           |     /|\\
           |      |
           |      
           -
        ''',
        # голова, торс и одна рука
        '''
           --------
           |      |
           |      O
           |      |\\
           |      |
           |     
           -
        ''',
        # голова и торс
        '''
           --------
           |      |
           |      O
           |      |
           |      |
           |     
           -
        ''',
        # голова
        '''
           --------
           |      |
           |      O
           |    
           |      
           |     
           -
        ''',
        # начальное состояние
        '''
           --------
           |      |
           |      
           |    
           |      
           |     
           -
        '''
    ]
    return stages[def_tries]


def play_game(def_letter, def_tries):
    if def_letter in guessed_word:
        print(f'Буква {def_letter.upper()} уже открыта')
    elif def_letter in guessed_letters:
        print(f'Ты уже называл(а) букву {def_letter.upper()}')
    elif def_letter in hidden_word:
        open_letter(def_letter)
        print('Верно')
        print('=' * len(hidden_word))
        print(*guessed_word, sep='')
        print('=' * len(hidden_word))
    elif def_letter not in alphabet:
        print('Такой буквы не существует, попробуй еще раз')
    else:
        def_tries -= 1
        print(display_hangman(def_tries))
        if def_tries != 0:
            print('Не угадал! Попробуй еще раз')
        print('=' * len(hidden_word))
        print(*guessed_word, sep='')
        print('=' * len(hidden_word))
    return def_letter, def_tries


hidden_word = word_generator(input().lower())
guessed_word = ['□' for i in range(len(hidden_word))]
tries = 6
can_open = len(hidden_word) // 3

print(f'Теперь тебе нужно отгадать слово. В слове {len(hidden_word)} букв.')
print(f'Можешь открыть любые {can_open} буквы')
print()
print('=' * len(hidden_word))
print(*guessed_word, sep='')
print('=' * len(hidden_word))
print()

while can_open > 0:
    print('Назови номер буквы в слове')
    letter_number = int(input())
    if letter_number > len(hidden_word):
        print(f'Номер буквы не может быть более {len(hidden_word) + 1}')
        continue
    if hidden_word[letter_number - 1] == guessed_word[letter_number - 1]:
        print('Эта буква уже открыта')
        continue
    for i in range(len(hidden_word)):
        if hidden_word[i] == hidden_word[letter_number - 1]:
            guessed_word[i] = hidden_word[i]
    print('=' * len(hidden_word))
    print(*guessed_word, sep='')
    print('=' * len(hidden_word))
    print()
    can_open -= 1

print(f'Поздравляю! ты смог открыть {len(guessed_word) - guessed_word.count("□")} букв')

while tries > 0:
    print('Назови букву в слове')
    letter, tries = play_game(input().lower(), tries)
    guessed_letters += letter
    if '□' not in guessed_word:
        print()
        print('ТЫ ПОБЕДИЛ')
        break
if tries == 0:
    print()
    print('ТЫ ПРОИГРАЛ')
    print(f'Я загадал слово {hidden_word.upper()}')
