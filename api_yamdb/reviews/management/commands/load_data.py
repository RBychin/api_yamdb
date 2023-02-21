import csv
import os

from django.core.management.base import BaseCommand
from django.db import DatabaseError, IntegrityError

from api_yamdb.settings import BASE_DIR
from reviews.models import (Title,
<<<<<<< HEAD
                            #TitleGenres,
=======
>>>>>>> develop
                            Review,
                            Comment,
                            Category,
                            User,
                            Genre)

PATH = os.path.join(BASE_DIR, 'static/data/')
<<<<<<< HEAD
FILES = os.listdir(PATH)
=======
>>>>>>> develop


FILE_FUNC = {
    'users': [User, 'users.csv'],
    'genre': [Genre, 'genre.csv'],
    'category': [Category, 'category.csv'],
    'titles': [Title, 'titles.csv'],
<<<<<<< HEAD
    #'genre_title': [TitleGenres, 'genre_title.csv'],
=======
    'genre_title': [Title, 'genre_title.csv'],
>>>>>>> develop
    'review': [Review, 'review.csv'],
    'comments': [Comment, 'comments.csv']
}

REPLACE_VALUE = {
    'author': 'author_id',
    'category': 'category_id',
}


def create_obj(reader, model):
    model.objects.bulk_create(
        [model(**{REPLACE_VALUE.get(k, k): v for k, v in row.items()}) for row
         in reader]
    )


class Command(BaseCommand):
    help = (f'Загружает данные из csv таблицы по адресу "{PATH}" '
            'в sqlite базу проекта Django, перед использованием,'
            'необходимо описать модели и сделать миграции.')

    def handle(self, *args, **options):
        for model, file in FILE_FUNC.values():
            try:
<<<<<<< HEAD
                with open(f'{PATH + file}', 'r', encoding="utf-8") as r_file:
=======
                with open(f'{PATH + file}', 'r', encoding='utf-8') as r_file:
>>>>>>> develop
                    reader = csv.DictReader(r_file, delimiter=',')
                    try:
                        create_obj(reader, model)
                    except IntegrityError:
                        print(f'- Ошибка | {file} | '
<<<<<<< HEAD
                              f'Проверьте уникальность полей.')
=======
                              f'Проверьте уникальность полей '
                              f'модели "{str(model.__name__)}".')
>>>>>>> develop
                    except DatabaseError as er:
                        print(f'- Ошибка | {file} | {er}.')
                    else:
                        print(f'+ Успех | {file} | '
<<<<<<< HEAD
                              f'Записей добавлено: {reader.line_num - 1}')
=======
                              f'Записей модели "{str(model.__name__)}" '
                              f'добавлено: {reader.line_num - 1}')
>>>>>>> develop
            except FileNotFoundError:
                print(f'- Ошибка | {file} | Файл не найден.')
