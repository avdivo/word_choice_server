'''Переменные для проекта'''
from dataclasses import dataclass
import sys, os


class SetingsInit:
    def __init__(self):
        self.WORD_LIST_FILE: str = os.path.join(sys.path[0] +'/init/', 'five_letters_singular.txt')  # Файл со словами
        self.LAST_UPDATE_WORD_LIST = os.path.getmtime(self.WORD_LIST_FILE)  # Unix время последнего обновления файла списка слов
        try:
            self.REDIS_PATH = os.environ['REDIS_PATH']  # Путь к Redis
        except:
            self.REDIS_PATH = 'localhost'

    def is_update(self):
        print(self.LAST_UPDATE_WORD_LIST, '==', os.path.getmtime(self.WORD_LIST_FILE))
        if self.LAST_UPDATE_WORD_LIST == os.path.getmtime(self.WORD_LIST_FILE):
            return False
        self.LAST_UPDATE_WORD_LIST = os.path.getmtime(self.WORD_LIST_FILE)
        return True

SETTINGS = SetingsInit()