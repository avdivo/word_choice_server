# Создание групп слов с различными свойствами для Redis

import re
import sys, os

def init_redis(r):
    if r.exists("all"):
        return

    # Чтение слов из файла
    input_file = os.path.join(sys.path[0]+'/init/', 'five_letters_singular.txt')  # Файл ввода
    with open(input_file, 'r', encoding='utf-8') as f:
        all_words = f.readlines()
    all_words = set(map(lambda x: x.rstrip(), all_words))  # Убираем дубликаты слов и перевод строки из них
    r.sadd('all', *all_words)  # Запись в Redis полного словаря

    # Подготовка алфавита
    alphabet = 'аокеритлнсупмбвдзгяышьцчхйфжюэщъё-'

    # Создание групп с точно присутствующей буквой в слове на определенной позиции
    # Создаем ключи для Redis указывающие на список слов в которых
    # в одной из позиций стоит определенная буква. Пример ключа: а....
    # Перебираются все буквы алфавита во всех 5 позициях в слове
    group = set()
    for pos in range(5):
        group_name = '.....'
        for letter in alphabet:
            group_name = group_name[:pos] + letter + '.' * (4 - pos)
            group.clear()
            for word in all_words:
                # Готовим можество слов, в которых заданная буква в нужной позиции
                if re.findall(group_name, word):
                    group.add(word)
            if group:
                r.sadd(group_name, *group)
                # print(set(map(lambda x: x.decode('utf-8'), r.smembers(group_name))))

    # Создание групп слов в которых отсутствует одна из букв алфавита
    # Создаем ключи для Redis указывающие на список слов в которых
    # нет одной из букв. Пример ключа: no_а
    # Перебираются все буквы алфавита
    group = set()
    for letter in alphabet:
        group_name = 'no_' + letter
        group.clear()
        for word in all_words:
            # Готовим можество слов, в которых нет заданной буквы
            if letter not in word:
                group.add(word)
        if group:
            r.sadd(group_name, *group)
            # print(len(group), group_name, set(map(lambda x: x.decode('utf-8'), r.smembers(group_name))))
