from random import choice
answers = ['Бесспорно', 'Мне кажется - да', 'Пока неясно, попробуй снова', 'Даже не думай',
'Предрешено', 'Вероятнее всего', 'Спроси позже', 'Мой ответ - нет',
'Никаких сомнений', 'Хорошие перспективы', 'Лучше не рассказывать', 'По моим данным - нет',
'Определённо да', 'Знаки говорят - да', 'Сейчас нельзя предсказать', 'Перспективы не очень хорошие',
'Можешь быть уверен в этом', 'Да', 'Сконцентрируйся и спроси опять', 'Весьма сомнительно']
repeat = ''


def magic_ball():
    if repeat.lower() != 'да':
        print('Привет! Я магический шар судьбы и умею прдсказывать будущее. Как тебя зовут?')
        user_name = input()
        print(f'{user_name}, что ты хочешь узнать?')
    else:
        print('Спрашивай')
    question = input()
    print(choice(answers))


magic_ball()
print('Хочешь узнать что-то еще? Напиши да или нет')
repeat = input()
while repeat.lower() == 'да':
    magic_ball()
    print('Хочешь узнать что-то еще? Напиши да или нет')
    repeat = input()
print('До скорого')
