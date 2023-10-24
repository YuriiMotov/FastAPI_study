# FastAPI_study
Here I'm practicing using FastAPI while taking [FastAPI online course](https://www.youtube.com/playlist?list=PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS).
Along the way I'm trying to improve the code from the course.

Thanks to [Artem Shumeiko]( https://github.com/artemonsh) for this course!


## Improvements:

### Lesson 5 (user registration and authentification with fastapi-users)

[Watch original lesson on Youtube](https://youtu.be/nfueh3ei8HU?si=2CGerqFNvvFD2PJf)

1. Why do we have to use 2 differend drivers for PostgreSQL (psycopg2 for fastapi, and asyncpg for alembic)? Let's use psycopg3 in both places!

    Commit: [3f22c0b](https://github.com/YuriiMotov/FastAPI_study/compare/6b80518715253e197c1387bfaf9183c63ec57dd4...3f22c0b9031b220bbd952ca0d9222baa3b8ea9de)

2. Getting rid of duplicating `User` database model . In the original lesson's code there are two places where this model is declared (`models.model.py` and `auth.database.py`) and you have to maintain both of these models in the same condition. It's bad and I think we can declare it once in `models.model.py` and inherit from `SQLAlchemyBaseUserTable`.
Also, new version of `fastapi-users` documentation follows the orm style to declare this table. So, let's use the same style in `models.py`.

    Commit: [5034ae2](https://github.com/YuriiMotov/FastAPI_study/compare/3f22c0b9031b220bbd952ca0d9222baa3b8ea9de...5034ae295a89f45b851aa88ba514e0880bce77b6)

3. It's said in course that `SECRETS` for `fastapi-users` should be stored in `.env`. Move them to `.env`.

    Commit: [fa9517c](https://github.com/YuriiMotov/FastAPI_study/compare/5034ae295a89f45b851aa88ba514e0880bce77b6...fa9517cd4cda073169da1c6cd4dc830b11f5206f)

4. I don't like the idea of overriding the `create` method in `UserManager` class just to set default `role_id` value. We can easily do it by specifying the `default` parameter in `User` model and removing `role_id` from the `UserCreate` schema.

    Commit: [8a2269c](https://github.com/YuriiMotov/FastAPI_study/compare/fa9517cd4cda073169da1c6cd4dc830b11f5206f...8a2269c79ca54751892033ea772c71a482545616)

5. In addition to 3 already implemented API endpoints (`register`, `login`, `logout`), let's implement `forgot_password` and `update` endpoints.
    
    Commits: [8890f19 and eee3d60](https://github.com/YuriiMotov/FastAPI_study/compare/943af454ef227aaf565241959339d28398db29e5...eee3d60a8364741d3ad26e4fbe702b4ef8719dd5)

6. `Cookie` transport is useful if you use web-browser. To use this API from mobile apps or from other systems, let's learn how to use `Bearer` transport and `Database` strategy.
    
    Commit: [c9369cb](https://github.com/YuriiMotov/FastAPI_study/compare/560889777d34e7ceccb85f10c8149b4f13a673ac...c9369cbb75c0ad51da94448c6859c010c1c2af63)


### Lesson 6 (routers and project file structure)

[Watch original lesson on Youtube](https://youtu.be/1Ag3RoOjNI0?si=9fCKIKzLjdu5ckBu)

0. Changing project structure and adding `operations` module as it's shown in lesson's source code.

    Commit: [bc4f100](https://github.com/YuriiMotov/FastAPI_study/compare/773a6927511356004b6929cbbd2e028eb434059b...bc4f100ae25f68c46768f9cdf2fdf2c4ddf1072c)

1. Using one metadata object for all database models, using ORM-style to declare `operations` table. Getting rid of depricated `dict` method in `operations.router`. Renaming `base_config` to `backends`.

    Commits: [01e52f5](https://github.com/YuriiMotov/FastAPI_study/compare/bc4f100ae25f68c46768f9cdf2fdf2c4ddf1072c...01e52f57afdf2cfee32352d270d4901ccc22f3ca), [bc7c563](https://github.com/YuriiMotov/FastAPI_study/compare/85168cea877c49caa3a62a2e58c1c11278528d80...bc7c56396c9dfbfdb481199fbf5865df9770c9e9)

2. Grouping `auth` routes into module `router` and include this router in `main`.

    Commit: [6fbd3fd](https://github.com/YuriiMotov/FastAPI_study/compare/01e52f57afdf2cfee32352d270d4901ccc22f3ca...6fbd3fd16904fbf571df266e6ab19bdd26de2076)

3. Configuring the migration file name format to include date and time.

    Commit: [bfb7e1c](https://github.com/YuriiMotov/FastAPI_study/compare/6fbd3fd16904fbf571df266e6ab19bdd26de2076...bfb7e1c5fcdc0cf29d348516e9b1ba5ca6cc917c)


### Lesson 7 (designing a RESTful API)

[Watch original lesson on Youtube](https://youtu.be/-RLXmoQ7iSE?si=l7q2lWuzxhpTp5uY)

0. Implementation of changes made in the lesson #7

    Commit: [c8b1b78](https://github.com/YuriiMotov/FastAPI_study/compare/1930af6a4b905d4780fc41edbeb12f26292d222f...c8b1b78aeb3d72b095dcf294d873d85dec1127ae)

1. Doing lesson's homework #1 (using HTTP PUT and PATCH methods)

    Commit: [27fab33](https://github.com/YuriiMotov/FastAPI_study/compare/c8b1b78aeb3d72b095dcf294d873d85dec1127ae...27fab33a666cd12bafc9a4914c6ca793eabead2b)

2. Doing lesson's homework #2 (standardization of input and output of all the endpoint interfaces).

    Speaking about standartization of endpoints, I don't think that suggested in this lesson approach is good. `Fastapi-users` doesn't follow this approach and we have to modify that endpoints to make them similar.
    
    I don't really understand why we need to add additional fields `status` and `detail` to successful response. At the same time we dont need some of these fields in other types of responses.
    
    We have `HTTP response status code` for passing status and I think it's better to use it instead of additional `status` field. The response to a successful request will contain only data (at the first level, without the additional `data` field), for unsuccessful requests it will contain the `detail` field (as it is done in `fatsapi-users`).

    In addition, let's specify the response schemes for the endpoints of the `operations` module.

    Commits: [1eedb71](https://github.com/YuriiMotov/FastAPI_study/compare/27fab33a666cd12bafc9a4914c6ca793eabead2b...1eedb71149d7dcc13716a04c8dd70e83ffb84f29) and [520b166](https://github.com/YuriiMotov/FastAPI_study/compare/fb0c76772dbd75479884cda21a6a01fb473b6bb8...520b166bb45dc290c0faeb6aa6d00d206bb96600)

3. Doing lesson's homework #3 (pagination of results)

    Commit: [fb0c767](https://github.com/YuriiMotov/FastAPI_study/compare/1eedb71149d7dcc13716a04c8dd70e83ffb84f29...fb0c76772dbd75479884cda21a6a01fb473b6bb8)

4. Catching `database error`, `doesn't exist` and `already exist` errors. Moving the handling of common errors outside of endpoint functions.

    Commit: [a0ecbdd](https://github.com/YuriiMotov/FastAPI_study/compare/520b166bb45dc290c0faeb6aa6d00d206bb96600...a0ecbddb75298ce235da71d09c32920511fa74ae)

5. Let's make the endpoints more RESTful: apply the REST URI construction rules (plural name for collection, `id` in the URI for GET, PUT and PATCH methods).
    It changes the logic of `POST` and `PUT` methods. Now `POST` will not accept `id` (it will be autogenerated) and `PUT` will return error if record with requested `id` doesn't exist (before these changes the `PUT` method created new record if record with requested `id` doesn't exist).

    Commit: [3d2f69e](https://github.com/YuriiMotov/FastAPI_study/compare/8b2cd6d8651f453b54cbc2e382b357b54b0b1b70...3d2f69ed196d9d86e902b5c09ca4e037c492c08d)


### Lesson 8 (caching with Redis)

[Watch original lesson on Youtube](https://youtu.be/t4H25XJG0Uc?si=OQjZL-M3TjIfDp98)

0. Implementation of changes made in the lesson #8

    Commit: [8b28197](https://github.com/YuriiMotov/FastAPI_study/compare/beeec6511485355a96c51581d9e13154457133a1...8b28197da11285a8abbadaae946c455b4d2f447b)

1. Let's try to use `fastapi-cache` with `InMemoryBackend`.
    Note that `InMemoryBackend` store cache data in memory and use lazy delete, which mean if you don't access it after cached, it will not delete automatically.

    Commit: [d4ea3e3](https://github.com/YuriiMotov/FastAPI_study/compare/6996d3b1d0446dedf3193c89034af1deb82e48fa...d4ea3e3ffc43f4c08daf6a3ec5c81a6d322c073a)

2. Let's learn how to manage client-side caching by setting headers.

    Commit: [cb97d4f](https://github.com/YuriiMotov/FastAPI_study/compare/e7b29bde101c0c509820c25372ceab2376eb0887...cb97d4fa4dad3b72f6532dc8d93034e2c6516560)

3. Deeping into `fastapi-cache` library.
    Here are some problems (or potential problems) of this library that I found:
        
    3.1. Caching doesn't work for private endpoints. If I pass a `user` object to my endpoint function and try to use this endpoint by opening in browser, it isn't cached. It's cached only on client side. I'm sure this problem can be solved by implementing custom key-builder, but it looks like a feature that should be by default.

    3.2. For private methods this library generates `cache-control: max-age=N` headers, but it doesn't add `Cache-Control: private`. This can lead to the leakage of personal data if the proxy server caches this data.

    3.3. There is no parameter to disable client-side cache headers in `cache` decorator. And you can't just override it in you function by adding `response.headers["Cache-Control"] = "no-store"` (they are added after the function call and will be overrided). People write middleware to do this, which is not good.

    3.4. There are quite a lot of issues on project's github page and some PRs. It looks like project owner doesn't have enought time to continue developing this project..


### Lesson 9 (background tasks with Celery, Redis and Flower)

[Watch original lesson on Youtube](https://youtu.be/fm4LTvMyiwE?si=Gnl-5Hcn2SC8MuD2)

0. Implementation of changes made in the lesson #9

    Commit: [2d0f98f](https://github.com/YuriiMotov/FastAPI_study/compare/d782fa57272a10d8a0192f62d041aa15cec7f52b...2d0f98fe55a57e41b6c34928c2bb45f1e7a1f5e6)

1. Let's add a background task execution check. If there is a problem during tha task execution then system will call special function.

    1.1. With FastAPI BackgroundTasks we can add try..except block in the background task's function and call our ErrorCallback function if any exceptions occur.

    Commit: [8063d38](https://github.com/YuriiMotov/FastAPI_study/compare/2d0f98fe55a57e41b6c34928c2bb45f1e7a1f5e6...8063d38a1ee6fb2eae89d6dfae8c2dd9f6e26b63)

    1.2. With Celery we can handle task's execution errors different ways:
        
    1.2.1. On the worker's side by using signals or specifying base class for task.

    Commit: [ff65eee](https://github.com/YuriiMotov/FastAPI_study/compare/4abab4a9d828f8d48b34cedb873acd808d8bbe2f...ff65eee9d6212e641e035e7b49eb0600c48057a3)

    1.2.2. On the FastAPI side by adding special async task for monitoring celery's task statuses. You can also implement it with Celery events real-time processing (you should run it in a separate thread), but I prefer first variant. 

    Commit: [c3e3271](https://github.com/YuriiMotov/FastAPI_study/compare/7af91792ccb89116e74fb917078dae353143d805...c3e3271af197190a9b6eb31a89a33ee3c925fafa)

2. The use of FastAPI's `on_startup` and `on_shoutdown` events is deprecated, we should use `lifespan` instead.

    Commit: [fd61e6b](https://github.com/YuriiMotov/FastAPI_study/compare/c3e3271af197190a9b6eb31a89a33ee3c925fafa...fd61e6b08d769861819d85575be6dcb94505127b)

3. Adding task execution monitoring endpoins.

    Commit: [ce7f425](https://github.com/YuriiMotov/FastAPI_study/compare/1d6619017dcd0f81ffe0daece65aa49944005a0b...ce7f4257a782b0439b1749fc0b3e7084af730f3c)

4. Playing with task priorities.

    4.1. Redis priorities. This approach can be used if you use Redis as a backend, your tasks are not long and you do not need very high prioritization.
    It's important to run worker with `--prefetch-multiplier=1` option. Otherwise Celery will preload `(CPU_cores_count)*4` tasks from the queue by one request.
    
    Commit: []()

    4.2. More common approach is to separate queues and run multiple workers for different queues.

    Commit: []()