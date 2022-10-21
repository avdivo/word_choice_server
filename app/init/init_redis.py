# Создание групп слов с различными свойствами для Redis
import re
from init.settings import SETTINGS

def init_redis(r):
    print(r.exists("all"), '===========================')
    if r.exists("all"):
        print(not SETTINGS.is_update(), '--------------------------')
        if not SETTINGS.is_update():
            return  # Если файл не обновлен, то не нужно обновлять БД Redis
        r.flushdb()  # Очистить БД

    # Чтение слов из файла
    with open(SETTINGS.WORD_LIST_FILE, 'r', encoding='utf-8') as f:
        all_words = f.readlines()
    all_words = set(map(lambda x: x.rstrip(), all_words))  # Убираем дубликаты слов и перевод строки из них
    r.sadd('all', *all_words)  # Запись в Redis полного словаря

    # Подготовка алфавита
    alphabet = 'аокреитлнсупмбвдгзяыьшцчхйфжющэъ-'

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
