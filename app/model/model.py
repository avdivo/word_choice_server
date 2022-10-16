from pydantic import BaseModel, root_validator
from typing import Dict
import re


class Filter(BaseModel):
    black_list: str = ''  # Этих букв не должно быть в слове
    white_list: str = ''  # Эти буквы должны быть в слове
    existing_letters: Dict[int, str] = {0: '', 1: '', 2: '', 3: '', 4: ''}  # Ключи 0, 1, 2, 3, 4
    # соответствуют позициям букв в слове. Значения - строки:
    # заглавная буква - она в этой позиции;
    # одна или есколько маленьких - эти буквы есть в слове, но в другой позиции
    double_letter: str = ''  # Какие буквы должны повторяться ('*' - любые)
    ban: bool = False  # Запретить слова в которых буква встречается больше 1 раза (True), False - разрешено

# uvicorn main:app --reload

    @root_validator()
    def verify_password_match(cls, filter):
        """Проверка согласованности данных фильтра"""

        # Перевод входных данных к нижнему регистру и удаление дубликатов
        filter['black_list'] = ''.join(set(filter.get("black_list").lower()))
        filter['white_list'] = ''.join(set(filter.get("white_list").lower()))
        filter['double_letter'] = ''.join(set(filter.get("double_letter").lower()))
        existing_letters = ''
        for k, v in filter['existing_letters'].items():
            filter['existing_letters'][k] = ''.join(set(v))
            existing_letters += filter['existing_letters'][k]

        mes = ''
        if not re.fullmatch(r'[а-я]+', filter['black_list']) and filter['black_list']:
            mes = 'Hедопустимые символы в Черном списке. '

        if not re.fullmatch(r'[а-я]+', filter['white_list']) and filter['white_list']:
            mes += 'Hедопустимые символы в Белом списке. '

        if not re.fullmatch(r'[а-я\*]+', filter['double_letter']) and filter['double_letter']:
            mes += 'Hедопустимые символы в списке Дублей. '

        if not re.fullmatch(r'[А-Яа-я]+', existing_letters) and existing_letters:
            mes += 'Hедопустимые символы в позициях. '

        if set(filter['black_list']) & set(filter['white_list']):
            mes += 'Одинаковые буквы в Черном и Белом списках. '

        if set(filter['black_list']) & set(filter['double_letter']):
            mes += 'Буква, которая в слове должна дублироваться занесена в Черный список. '

        if filter['ban'] and filter['double_letter']:
            mes += 'Дублирование букв в слове запрещено, однако ведется поиск с дублируемой буквой. '

        if set(filter['black_list']) & set([x.lower() for x in filter['existing_letters'].values()]):
            mes += 'В Черном списке указаны буквы которые должны писутствовать в слове.'

        if mes:
            raise ValueError(mes)

        return filter
