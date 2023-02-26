
# Best Jun`s Project  
  
### Как запустить проект:  
  

 1. Для запуска проекта необходимо клонировать или скачать репозиторий.
 2. Установить все связи из requirements.txt `pip install -r requirements.txt `.
 3. Сделать миграции `python3 manage.py makemigrations`, `python3 manage.py migrate`.
 

### Парсинг csv файла:  

В проекте присутствует парсер csv файла в БД проекта.
Что бы его использовать необходимо выполнить следующую команду:

- `python3 manage.py load_data` - для загрузки всех файлов, находящихся в директории data
- `python3 manage.py load_data -p <file_name>` - здесь необходимо в `<file_name>` указать имя файла.
