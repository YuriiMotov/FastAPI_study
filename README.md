# FastAPI_study
Here I'm practicing using FastAPI while taking [FastAPI online course](https://www.youtube.com/playlist?list=PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS).
Along the way I'm trying to improve the code from the course.

Thanks to [Artem Shumeiko]( https://github.com/artemonsh) for this course!


## Improvements:

### Lesson 5

1) Why do we have to use 2 differend drivers for PostgreSQL (psycopg2 for fastapi, and asyncpg for alembic)? Let's use psycopg3 in both places!

    Commit: [3f22c0b](https://github.com/YuriiMotov/FastAPI_study/compare/6b80518715253e197c1387bfaf9183c63ec57dd4...3f22c0b9031b220bbd952ca0d9222baa3b8ea9de)

2) Get rid of duplicating `User` database model . In the original lesson's code there are two places where this model is declared (`models.model.py` and `auth.database.py`) and you have to maintain both of these models in the same condition. It's bad and I think we can declare it once in `models.model.py` and inherit from `SQLAlchemyBaseUserTable`.
Also, new version of `fastapi-users` documentation follows the orm style to declare this table. So, let's use the same style in `models.py`.

    Commit: [5034ae2](https://github.com/YuriiMotov/FastAPI_study/compare/3f22c0b9031b220bbd952ca0d9222baa3b8ea9de...5034ae295a89f45b851aa88ba514e0880bce77b6)

3) It's said in course that `SECRETS` for `fastapi-users` should be stored in `.env`. Move them to `.env`.

    Commit: [fa9517c](https://github.com/YuriiMotov/FastAPI_study/compare/5034ae295a89f45b851aa88ba514e0880bce77b6...fa9517cd4cda073169da1c6cd4dc830b11f5206f)

4) I don't like the idea of overriding the `create` method in `UserManager` class just to set default `role_id` value. We can easily do it by specifying the `default` parameter in `User` model.

    Commit: 

