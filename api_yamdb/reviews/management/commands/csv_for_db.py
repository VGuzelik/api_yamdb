import csv
import logging
import sys

from django.apps import apps
from django.core.management.base import BaseCommand


# вынести в отдельный файл (проблема - не импортируется)
class NotValidDataForModelError(Exception):
    """Ошибка, если  данные в CSV-файле невалидные или неверный путь к файлу"""
    pass


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(name)s, %(message)s',
)
handler.setFormatter(formatter)


RELATIONSHIP_FIELDS = ('category', 'author')


class Command(BaseCommand):
    help = 'Импорт объектов в БД из CSV файлов'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help="Путь к файлу")
        parser.add_argument(
            'app_name',
            type=str,
            help="Наименование приложения, в котором находится модель"
        )
        parser.add_argument('model_name', type=str, help="Наименование модели")

    def handle(self, *args, **options):
        file_path = options['path']
        model = apps.get_model(options['app_name'], options['model_name'])
        try:
            with open(file_path, encoding='utf8') as csv_file:
                obj_list = []
                reader = csv.DictReader(csv_file)
                for row in reader:
                    for field in RELATIONSHIP_FIELDS:
                        if field in row:
                            row[f'{field}_id'] = row[field]
                            del row[field]
                    obj_list.append(model(**row))
                model.objects.bulk_create(obj_list)
            logger.info('Данные успешно записаны в БД')
        except NotValidDataForModelError as error:
            logger.error(error, exc_info=True)
