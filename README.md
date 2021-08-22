# Телеграм-бот ассистент, проверяющий статус домашней работы в Яндекс.Практикум

Телеграм-бот, который:
обращается к API сервиса Практикум.Домашка;
узнает, взята ли ваша домашка в ревью, проверена ли она, провалена или принята;
отправляет результат в мой Телеграм-чат.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Andrey-A-K/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
