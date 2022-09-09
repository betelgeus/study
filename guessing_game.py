from random import *


def n_border_check():
    n_border = input()
    while n_border.isalpha() or 0 > int(n_border):
        print('Вы ошиблись, введите число больше 0')
        n_border = input()
    return int(n_border)


def n_check(n_border):
    n = input()
    cnt = 0
    while n.isalpha() or 0 > int(n) or int(n) > n_border:
        if cnt == 0:
            print(f'Вы ошиблись, введите число от 0 до {n_border}')
            cnt += 1
        else:
            print(f'А может быть все-таки введем целое число от 0 до {n_border}?')
        n = input()
    return int(n)


def numerical_game():
    print('Добро пожаловать в игру "Числовая угадайка". Правила такие: '
          'я загадаю любое число от 0 до того, что вы укажите. А вам нужно будет его отдагать')
    print('Введите любое положительное число.')
    n_border = n_border_check()
    print(f'Теперь вам нужно отгадать число, которое я загадал. '
          f'Напомню, что оно больше 0 и меньше {n_border}. Введите число')
    n = n_check(n_border)
    random_number = randrange(1, n_border)
    attempt_counter = 1
    while n != random_number:
        if n > random_number:
            print('Ваше число больше загаданного, попробуйте еще разок')
        elif n < random_number:
            print('Ваше число меньше загаданного, попробуйте еще разок')
        attempt_counter += 1
        n = n_check(n_border)

    print(f'Вы угадали, поздравляем! Вам потребовалось {attempt_counter} попыток.')
    print('Хотите сыграть еще раз? Напишите да или нет')


numerical_game()
while input() == 'да':
    numerical_game()

print('Еще увидимся')
