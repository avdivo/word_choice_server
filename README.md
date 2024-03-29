О программе
https://avdivo.ru/5letters/

Программа создана специально для помощи в известной игре "5 букв". 
С мая 2022 года на сайте Тинькофф можно получить бонусы за угадывание слов в этой игре 5bukv.tinkoff.ru 
Также в игру можно поиграть тут https://wordlegame.org/ru/5-letter-words-wordle. 
Там же можно ознакомиться с правилами игры.
В отличие от большинства сервисов для подбора слов и помощников кроссвордистов в этой программе есть возможность 
использовать фильтры, специально подобранные под правила игры, а также некоторые дополнительные возможности, 
облегчающие поиск слова.

Как пользоваться программой
Есть несколько фильтров, которые позволяют отбрасывать слова, не подходящие по критериям. В основном, 
используется фильтр "Черный список" и фильтры по позициям букв (5 клеточек снизу). В "Черном списке" нужно указать 
буквы, которые отсутствуют в слове. А в позиционных клеточках буквы, которые есть в слове, но не в этой 
позиции (не отмеченные флажком под буквой) и те, которые стоят на своем месте (отмеченные флажком под буквой и имеющие 
зеленый фон).
При выводе слов они собираются в группы таким образом, что группы, находящиеся вверху страницы, имеют набор букв, 
имеющий больше шансов встретиться в искомом слове. Кроме того, нужно стараться использовать наиболее употребляемые 
слова, они чаще оказываются загадвнными (хотя набор слов зависит от автора конкретной игры).
Если программа возвращает много слов, можно воспользоваться переключателем "Запрет дублей", в этом случае будут 
предлагаться слова, не имеющие одинаковых букв, что позволяет проверить большее количество букв за одну попытку. 
Не забывайте выключить этот фильтр на заключительных этапах, иначе нужного слова может не оказаться в конечном списке.

Благодарю за интерес, проявленный к этой программе. 
Присылайте свои отзывы, пожелания и недостающие слова по электронной почте или в Телеграмм. Удачной игры.


Программа написана на языке программирования Python.
В разработке использованы:
Python, FastAPI, Redis, Docker, Docker-Compose, HTML, CSS, JQuery, JavaScript, AJAX, REST, JSON


Разворачивание на сервере
1. Установка Docker CE, Docker-compose, GIT
2. Скачать образ Redis: docker pull redis
3. Загрузить проект: git clone https://github.com/avdivo/word_choice_server/tree/master/app
4. Перейти в каталог проекта: cd word_choice_server
5. sudo docker-compose build
6. sudo docker-compose up -d
7. В браузере открыть: 127.0.0.1/5letters/ или <IP адрес сервера (сайт)>/5letters/



Для запуска без контейнера после п.3 выполнить следующее.

Запустить Redis в контейнере:

cd word_choice_server/redis

docker-compose up -d

cd ..

Установить зависимости:

pip install -r requirements.txt

Запустить сервер:

cd app

uvicorn main:app --reload
