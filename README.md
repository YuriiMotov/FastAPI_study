# FastAPI_study
Here I'm practicing using FastAPI while taking online course (https://www.youtube.com/playlist?list=PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS).
Along the way I'm trying to improve the code from the course.

Thanks to Artem Shumeiko (@artemonsh) for this course!


Improvements:

1) Why do we have to use 2 differend drivers for PostgreSQL (psycopg2 for fastapi, and asyncpg for alembic)? Let's use psycopg3 in both places!

2) Get rid of duplicating `User` database model . In the original lesson's code there are two places where this model is declared (`models.model.py` and `auth.database.py`) and you have to maintain both of these models in the same condition. It's bad and I think we can declare it once in `models.model.py` and inherit from `SQLAlchemyBaseUserTable`.
Also, new version of `fastapi-users` documentation follows the orm style to declare this table. So, let's use the same style in `models.py`.


