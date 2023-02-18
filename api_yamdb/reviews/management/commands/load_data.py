import csv
import os

import django
from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import (Title,
                            TitleGenres,
                            Review,
                            Comment,
                            Category,
                            User,
                            Genre)

PATH = os.path.join(BASE_DIR, 'static/data/')
FILES = os.listdir(PATH)


def get_file(file, files):
    if f'{file}.csv' in files:
        return file
    else:
        return None


def get_titles(reader):
    Title.objects.bulk_create(
        [Title(
            id=row[0],
            name=row[1],
            year=row[2],
            category_id=row[3]
        ) for row in reader]
    )
    print('Title записи успешно добавлены.')


def get_category(reader):
    Category.objects.bulk_create(
        [Category(
            id=row[0],
            name=row[1],
            slug=row[2]
        ) for row in reader]
    )
    print('Category записи успешно добавлены.')


def get_users(reader):
    User.objects.bulk_create(
        [User(
            id=row[0],
            username=row[1],
            email=row[2],
            role=row[3],
            bio=row[4],
            first_name=row[5],
            last_name=row[6]
        ) for row in reader]
    )
    print('Users записи успешно добавлены.')


def get_review(reader):
    Review.objects.bulk_create(
        [Review(
            id=row[0],
            title_id=row[1],
            text=row[2],
            author_id=row[3],
            score=row[4],
            pub_date=row[5]
        ) for row in reader]
    )
    print('Review записи успешно добавлены.')


def get_comments(reader):
    Comment.objects.bulk_create(
        [Comment(
            id=row[0],
            review_id=row[1],
            text=row[2],
            author_id=row[3],
            pub_date=row[4]
        ) for row in reader]
    )
    print('Comment записи успешно добавлены.')


def get_genre(reader):
    Genre.objects.bulk_create(
        [Genre(
            id=row[0],
            name=row[1],
            slug=row[2]
        ) for row in reader]
    )
    print('Genre записи успешно добавлены.')


def get_genre_title(reader):
    TitleGenres.objects.bulk_create(
        [TitleGenres(
            id=row[0],
            title_id=row[1],
            genre_id=row[2]
        ) for row in reader]
    )
    print('TitleGenres записи успешно добавлены.')


FILE_FUNC = {
    'users': [get_users, 'users.csv'],
    'genre': [get_genre, 'genre.csv'],
    'category': [get_category, 'category.csv'],
    'titles': [get_titles, 'titles.csv'],
    'genre_title': [get_genre_title, 'genre_title.csv'],
    'review': [get_review, 'review.csv'],
    'comments': [get_comments, 'comments.csv']
}


class Command(BaseCommand):
    help = 'Загружает данные из csv таблицы в sqlite базу проекта.'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--prefix', type=str,
                            help='Название таблицы.', )

    def handle(self, *args, **options):
        prefix = options.get('prefix')
        if prefix:
            try:
                with open(f'{PATH}/{prefix}.csv', 'r', encoding='utf-8') as r_file:
                    reader = csv.reader(r_file, delimiter=',')
                    next(reader)
                    if get_file(prefix, FILES) and prefix in FILE_FUNC:
                        FILE_FUNC.get(prefix)[0](reader)
                    else:
                        return (f'Файл "{prefix}" не найден.'
                                f'\n Выберете файл из списка: '
                                f'{", ".join(FILES).replace(".csv", "")} '
                                f'\nИли воспользуйтесь командой manage.py '
                                f'load_data без префикса, для обработки всех '
                                f'файлов в директории data')
            except Exception as er:
                print(er)
            else:
                return '--Загрузка завершена успешно.--'
        else:
            try:
                for file in FILE_FUNC.values():
                    with open(f'{PATH}{file[1]}') as r_file:
                        reader = csv.reader(r_file, delimiter=',')
                        next(reader)
                        file[0](reader)
            except django.db.utils.IntegrityError as er:
                print(f'Ошибка: {er}')
            else:
                return '--Загрузка завершена успешно.--'
