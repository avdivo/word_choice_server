import re
import redis
import time
from init.init_redis import init_redis
from init.settings import SETTINGS

def word_choice(filter):
    """
    Фильтрация слов по заданным параметрам

        ---------------------- Фильтры --------------------------------
    Запретить слова в которых буква встречается больше 1 раза
    filter.ban = False  # False - разрешено
    Какая буква должна повторяться ('*' - любая)
    filter.double_letter = ''
    Черный список букв
    filter.black_list = ''
    Белый список букв (эти буквы объязательны в слове)
    filter.white_list = ''

    Буквы, которые есть в слове
    Если словарь или значение его элемента пустые, значит еще нет букв которые точно есть в слове.
    Если буквы есть, соварь будет содержать описание известных позиций в слове, позиции обозначаются ключами 0 - 4:
    Буква в верхнем регистре строки значения обозначает что в этой позиции точно стоит эта буква.
    В нижнем регистре буквы обозначают что в этой позиции этаи буквы не стоит (но она есть в слове в дргой позиции)
    filter.existing_letters = {0: '', 1: '', 2: '', 3: '', 4: ''}
    """

    # ------------------- Время выполнения ----------------------
    start_time = time.time()
    # ------------------- Время выполнения ----------------------

    # Подготовка алфавита
    alphabet = 'аокеритлнсупмбвдзгяышьцчхйфжюэщъё-'

    # Для запуска вне докера  сети с контейнером redis использовать подключение Localhost
    try:
        r = redis.Redis(host=SETTINGS.REDIS_PATH, port=6379, db=0)  # Подключаемся к Redis
    except:
        raise ValueError('Нет подключения к Redi')

    # Проверяем, обновлена ли база данных, если нет - обновляем
    init_redis(r)

    # ------------------------ Фильтр слов ---------------------------------
    # Отсев слов которые содержат буквы из Черного списка
    # Запрашиваем в Redis слова, в которых нет букв из черного списка
    # Слова записаны в группы 'no_x' где x отсутствующая буква
    if filter.black_list:
        # Запрашиваем у Redis пересечение множеств.
        list_group_name = [f'no_{letter}' for letter in filter.black_list]
        all_words = set(map(lambda x: x.decode('utf-8'), r.sinter(*list_group_name)))
    else:
        # Если Черный список пуст, читаем множество со всеми словами
        all_words = set(map(lambda x: x.decode('utf-8'), r.smembers('all')))



    # if filter.existing_letters[0] == '':
    #     for i in range(1500000):
    #         all_words = list(all_words)
    #         all_words = set(all_words)
    #         if i % 1000 == 0:
    #             print(filter.existing_letters[1])
    #



    # Отсев слов в которых нет букв из Белого списка
    # Суммируем множества слов в которых нет объязательных букв и отнимаем его от слов, оставшихся после Черного списка
    if filter.white_list:
        # Запрашиваем у Redis сумму множеств
        list_group_name = [f'no_{letter}' for letter in filter.white_list]
        all_words -= set(map(lambda x: x.decode('utf-8'), r.sunion(*list_group_name)))

    # Подготовка фильтров на основе присутствующих в слове букв
    # Готовим список ключей множеств Redis
    # Работа фильтров:
    # Имеются группы слов в каждой из которых одна из букв алфавита стоит в одой из пяти позици в слове
    # Для каждой буквы алфавита и каждой позиции. Они имеют имена по шаблону: а.... или ..о..
    # 1. Для нахождения слов с известными буквами в известных позициях (приходят как заглавные)
    #    включаем соответствующую группу в список, и находим пересечение (средствами Redis)
    #    всех списков. Запоминаем полученное множество в Python.
    # 2. Для случаев когда известно, что буква есть в слове и позиция
    #    где эта буква не стоит. Получаем множества (суммируем) где бука есть на всех дпугих
    #    местах кроме запрещенного. Отнимаем от него множество с этой буквой в запрещенной позиции,
    #    чтобы избежать попадания такого слова, когда нужных букв в слове не одна.
    #    Запоминаем это множкство в python для первй буквы.
    #    Для остальных букв находим пересечение с запомненным множеством и сохраняем туда же.
    # 3. Находим пересечение множеств после п.1 и п.2
    if filter.existing_letters:
        exist_in_position = set()
        exist_out_of_position = set()
        exist_out_of_position_inverse = set()
        filter_work_exist_in_position = False  # Если фильтр работал, то применяем его результаты к списку,
        filter_work_exist_out_of_position = False  # даже еси результат пустой
        first = True
        for pos, val in filter.existing_letters.items():
            if val:
                if val.islower():
                    filter_work_exist_out_of_position = True
                    for letter in val:
                        # Добавляем имена групп с данной буквой, кроме того, где она стоит в рассматриваемой
                        # позиции, слова где эта буква в этой позиции не включаются
                        for i in range(5):
                            if i != pos:
                                # Ключи множеств, где буква находится в не запрещенных местах
                                exist_out_of_position_inverse.add(f'....{letter}....'[4 - i:9 - i])
                        if first:
                            first = False
                            exist_out_of_position = set(map(lambda x: x.decode('utf-8'),
                                                            r.sunion(exist_out_of_position_inverse)))
                        else:
                            exist_out_of_position &= set(map(lambda x: x.decode('utf-8'),
                                                             r.sunion(exist_out_of_position_inverse)))
                        # При 2 искомых буквах в слове. Слово будет включно в список, поскольку имеет
                        # нужную букву там где она не запрещена, однако оно же может иметь букву в позиции
                        # где она запрещена. Поэтому очистим список от слов имеющих букву в запрещенной позиции
                        exist_out_of_position -= set(map(lambda x: x.decode('utf-8'),
                                                         r.sunion('.....'[:pos] + letter + '.' * (4 - pos))))
                        exist_out_of_position_inverse.clear()
                else:
                    # Для букв которые стоят на своих позициях
                    exist_in_position.add('.....'[:pos] + val[0].lower() + '.' * (4 - pos))
                    filter_work_exist_in_position = True
        if exist_in_position or filter_work_exist_in_position:
            exist_in_position = set(map(lambda x: x.decode('utf-8'), r.sinter(exist_in_position)))
            all_words &= exist_in_position
        if exist_out_of_position or filter_work_exist_out_of_position:
            all_words &= exist_out_of_position

    # Разбивка на группы и сортировка перед выводом
    # Слова для вывода разбиваем по группам.
    # Группы формируются по принципу частотности использования групп в 5-буквенных словах
    # Для этого определяем для каждого слова, какая его буква стоит ниже всех в списке частотности букв
    # По индексу этой буквы назначаем номер группы для вывода

    number_group = dict()
    summ = 0
    for word in all_words:
        # Исключаем слова, с дублированием букв
        if filter.ban and re.findall(r'(\w).*\1+', word):
            continue
        # Исключаем слово, если заданные буквы не встречаются в нем более 1 раза
        if filter.double_letter:
            if filter.double_letter != '*':
                stop = False
                for letter in filter.double_letter:
                    if word.count(letter) < 2:
                        stop = True
                        break
                if stop:
                    continue
            else:
                # Исключаем слово, если в нем нет дубля любой буквы
                if not re.findall(r'(\w).*\1+', word):
                    continue

        number = max([alphabet.index(letter) for letter in word])
        try:
            number_group[number] += [word]
        except:
            number_group[number] = [word]
        summ += 1
    number_group = sorted(number_group.items(), key=lambda x: x[0])

    out_words = []
    for i, l in enumerate(number_group):
        if l:
            out_words.append(sorted(l[1]))
    t = f"{(time.time() - start_time) * 1000} миллисекунд"
    # ------------------- Время выполнения ----------------------
    print(t)
    # ------------------- Время выполнения ----------------------

    return out_words, t
