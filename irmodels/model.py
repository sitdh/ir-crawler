from peewee import *
from playhouse.db_url import connect

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

db = MySQLDatabase(config.get('DATABASE', 'dbname', fallback='test'),
        host=config.get('DATABASE', 'localhost', fallback='localhost'),
        user=config.get('DATABASE', 'user', fallback='user'),
        password=config.get('DATABASE', 'password', fallback='password'),
        )

class Course(Model):
    course_id = BigIntegerField(primary_key=True)
    course_description = TextField()
    language = CharField()
    level = CharField()
    overall_rating = DecimalField()

    class Meta:
        database = db
        db_table = 'course'

class Document(Model):
    document_id = BigIntegerField(primary_key=True)
    document_title = CharField()

    class Meta:
        database = db
        db_table = 'document'

class Review(Model):
    review_id = BigIntegerField(primary_key=True)
    reviewer = CharField()
    rating = IntegerField()
    comment = TextField()
    course = ForeignKeyField(Course, related_name='reviews')

    class Meta:
        database = db
        db_table = 'review'


if __name__ == '__main__':
    if not Course.table_exists():
        Course.create_table()

    if not Document.table_exists():
        Document.create_table()

    if not Review.table_exists():
        Review.create_table()


