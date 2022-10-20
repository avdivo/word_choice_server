'''Переменные для проекта'''
import sys, os
WORD_LIST_FILE = os.path.join(sys.path[0] +'/init/', 'five_letters_singular.txt')  # Файл со словами
LAST_UPDATE_WORD_LIST = os.path.getmtime(WORD_LIST_FILE)  # Unix время последнего обновления файла списка слов

try:
    REDIS_PATH = os.environ['REDIS_PATH']  # Путь к Redis
except:
    REDIS_PATH = 'localhost'

REDIS_PATH = 'localhost'