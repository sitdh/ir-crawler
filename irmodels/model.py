from peewee import *
from playhouse.db_url import connect

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

database = MySQLDatabase(config.get('DATABASE', 'dbname', fallback='test'),
            host=config.get('DATABASE', 'localhost', fallback='localhost'),
            user=config.get('DATABASE', 'user', fallback='user'),
            password=config.get('DATABASE', 'password', fallback='password'),
            )

class BaseModel(Model):
    class Meta:
        database = database
        db_table = 'course'

class Course(BaseModel):
    course_id = UUIDField(primary_key=True)
    course_title = CharField()
    course_description = TextField()
    language = CharField()
    level = CharField()
    student_enrolled = IntegerField()
    ratings = IntegerField()
    overall_rating = DecimalField()
    course_url = CharField()
    cover_image = CharField()
    source = CharField()

# class Document(BaseModel):
#     document_id = BigIntegerField(primary_key=True)
#     document_title = CharField()
# 
# class Review(BaseModel):
#     review_id = BigIntegerField(primary_key=True)
#     reviewer = CharField()
#     rating = IntegerField()
#     comment = TextField()
#     course = ForeignKeyField(Course, related_name='reviews')

if __name__ == '__main__':
    if not Course.table_exists():
        Course.create_table()

    # if not Document.table_exists():
    #     Document.create_table()
    # if not Document.table_exists():
    #     Document.create_table()
    # if not Review.table_exists():
    #     Review.create_table()
