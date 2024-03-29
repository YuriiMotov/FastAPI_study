# FastAPI_study
Here I'm practicing using FastAPI while taking [FastAPI online course](https://www.youtube.com/playlist?list=PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS).
Along the way I'm trying to improve the code from the course.

Thanks to [Artem Shumeiko]( https://github.com/artemonsh) for this course!


## Table of contents:

1. [Lesson 5 (user registration and authentification with fastapi-users)](#lesson-5-user-registration-and-authentification-with-fastapi-users)

2. [Lesson 6 (routers and project file structure)](#lesson-6-routers-and-project-file-structure)

3. [Lesson 7 (designing a RESTful API)](#lesson-7-designing-a-restful-api)

4. [Lesson 8 (caching with Redis)](#lesson-8-caching-with-redis)

5. [Lesson 9 (background tasks with Celery, Redis and Flower)](#lesson-9-background-tasks-with-celery-redis-and-flower)

6. [Lesson 10 (testing with PyTest)](#lesson-10-testing-with-pytest)

7. [Lesson 11 (Linking Frontend and Backend. Cors and Middleware)](#lesson-11-linking-frontend-and-backend-cors-and-middleware)

8. [Lesson 12 (Jinja templates)](#lesson-12-jinja-templates)

9. [Lesson 13 (Websockets)](#lesson-13-websockets)

10. [Lesson 14 (How to use Depends)](#lesson-14-how-to-use-depends)

11. [Lesson 15 (Docker and Docker Compose)](#lesson-15-docker-and-docker-compose))

12. [Lesson 16 (Software deployment on render.com)](#lesson-16-software-deployment-on-rendercom)

13. [Layered architecture style](#layered-architecture-style)

14. [UnitOfWork pattern with FastAPI](#unit-of-work-pattern-with-fastapi)

15. [Reading Fast API documentation and practicing new things](#reading-fast-api-documentation-and-practicing-new-things)

    15.1. [OAuth scopes](#1-oauth-scopes)

    15.2. [Sub Applications - Mounts](#2-sub-applications---mounts)

    15.3. [Testing WebSockets](#3-testing-websockets)

    15.4. [OAuth2 with refresh tokens + rotation](#4-oauth2-with-refresh-tokens--rotation)

    15.5. [Request rate limit](#5-request-rate-limit)

    15.6. [SQLModel](#6-sqlmodel)

    15.7. [Monitoring FastAPI with Prometheus and Grafana](#7-monitoring-fastapi-with-prometheus-and-grafana)

    15.8. [Authentication with Keycloak](#8-authentication-with-keycloak)
    

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

3. Delving into `fastapi-cache` library.
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

3. Adding celery-task execution monitoring endpoins.

    Commit: [ce7f425](https://github.com/YuriiMotov/FastAPI_study/compare/1d6619017dcd0f81ffe0daece65aa49944005a0b...ce7f4257a782b0439b1749fc0b3e7084af730f3c)

4. Playing with celery-task priorities.

    4.1. Redis priorities. This approach can be used if you use Redis as a backend, your tasks are not long and you do not need very high prioritization.
    It's important to run worker with `--prefetch-multiplier=1` option. Otherwise Celery will preload `(CPU_cores_count)*4` tasks from the queue by one request.
    
    Commit: [fdca370](https://github.com/YuriiMotov/FastAPI_study/compare/4bfa7f24f4491f93b6c9a6c5eb59701dc8ab7fad...fdca37094623f85dfc642922527f3e09e1bac7a6)

    4.2. More common approach is to separate queues and run multiple workers for different queues.

    Commit: [f0d87c3](https://github.com/YuriiMotov/FastAPI_study/compare/fdca37094623f85dfc642922527f3e09e1bac7a6...f0d87c3ef0b8a7d5362a64633a030fb45825b5fb)


### Lesson 10 (testing with PyTest)

[Watch original lesson on Youtube](https://youtu.be/4xJGQKfN3ZM?si=AxZQ6V4xIRBVz6B8)

0. Implementation of changes made in the lesson #10

    Commit: [ff80cfe](https://github.com/YuriiMotov/FastAPI_study/compare/e4dc2c08233a945f09ed77e39b452069ee4e2edd...ff80cfe8438c9aaffa3440f603aa48aeeb5f99bb)

1. Understanding the neccessety of the `event_loop` fixture.

    As I learned from the `python-asyncio` documentation, we need to override default `event_loop` fixture if we use fixtures with the scope different to `function` wich is the default scope.
    So, since we use fixtures with `session` scope, we need to override `event_loop` fixture with the same scope (it might be any scope that is equal to or wider than others).

2. Testing endpoints, that use '@cache' decorator.

    As `httpx.AsyncClient` doesn't implement the `lifespan` protocol, it doesn't use (evoke) `lifespan` context where `fastapi-cache` is initialized.
    The solution is to add just one line of code in the `ac` fixture.

    Commit: [6b10367](https://github.com/YuriiMotov/FastAPI_study/compare/0d5f77ed541631edb78f8e612bf69016807420dc...6b1036760d090aea412855e2c119c58a3880aeff)

3. Is it possible and beneficial to run asynchronous tests in parallel?

    Yes. We can use `pytest-asyncio-cooperative` plugin to achieve it.

    It seems as if it doesn't make sence to run tests in cooperative mode if you have a lot of light (fast) tests. But if your tests require long I/O, it will definitely benefit.

    Commit: [c5abf7b](https://github.com/YuriiMotov/FastAPI_study/compare/6c9e6266888d7c82df567636715995eb8bb59768...c5abf7bba6e662856dfc85113a545bdb14b1fbdd)


### Lesson 11 (Linking Frontend and Backend. Cors and Middleware)

[Watch original lesson on Youtube](https://youtu.be/h0eTzi5Geo8?si=htNdLZnxlCcYyINx)

0. Implementation of changes made in the lesson #11

    Commit: [c7aa64d](https://github.com/YuriiMotov/FastAPI_study/compare/9080c4284c3f1e4340d395999bce142bde9ae160...c7aa64dd1cb9578249922b98f2094ee54dd28fbc)

1. Checking how it works.

    Since I don't have the Frontend's code that was demonstrated in video, I used browser's console and fetch to check how it works.

    I set origins in `main.py` as: `origins = ["https://fastapi.tiangolo.com"]`, opened `https://fastapi.tiangolo.com` in browser, then opened `inspect` -> `console`.

    Add operation:

        fetch(
            'http://localhost:8000/operations/',
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({"quantity": "10", "figi": "string", "instrument_type": "BTC", "date": "2023-10-26T08:29:31.139Z", "type": "sell"})
            }
        ).then(resp => resp.text()).then(console.log)
    
    Get operations:

        fetch(
        'http://localhost:8000/operations/?operation_type=sell',
        {
            method: 'GET'
        }
        ).then(resp => resp.text()).then(console.log)
    
    Authorization via Bearer:

        fetch(
        'http://127.0.0.1:8000/auth/bdb/login',
        {
            method: 'POST',
            credentials: "include",
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: "username=EMAIL&password=PWD"
        }
        ).then(resp => resp.text()).then(console.log)

        fetch(
        'http://127.0.0.1:8000/auth/me',
        {
            method: 'GET',
            credentials: "include",
            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer TOKEN_RECEIVED_IN_PREVIOUS_STEP' }
        }
        ).then(resp => resp.text()).then(console.log)

    I could not check authorization via Cookies.. I'll try to figure out later.

### Lesson 12 (Jinja templates)

[Watch original lesson on Youtube](https://youtu.be/AKLzDJ6XLCc?si=1royCvzG45zaqqWZ)

0. Implementation of changes made in the lesson #12

    Commit: [3e96cf7](https://github.com/YuriiMotov/FastAPI_study/compare/8064a11ea006962026c0c5e7940cfae465f9d780...3e96cf71e36696266d79155d2532076550bc5d41)

1. Thoughts about error handling.

    What happens if an exception occurs during request processing?

    This exception will be handled by FastAPI exception handlers that we set. And it will be the same handler for all requests (API calls all webpage requests).

    I want to separate these requests and show html-page for web requests and json for API requests.

    It turned out that you can't set different exception handlers for different routers. After doing some research I decided that the best way to implement that is to run two different ASGI-applications: first (API-server) will include routers for API requests, second (WEB-server) will include routers for WEB requests. And both of them will have their own exception handlers. You can run these servers separately (in two different terminal sessions) or write a script which will run two servers in one event loop.

    Commit: [f104992](https://github.com/YuriiMotov/FastAPI_study/compare/3e96cf71e36696266d79155d2532076550bc5d41...f1049923b21312cd2316afc41469dbc2aee7f020)

2. Getting rid of `src/` in paths.

    When I tried to integrate lesson's 12 code to my code, it didn't work until I added `src/` to the beginning of the paths to static files and templates. 

    It happened because I ran code from current project's directory, not from `src` directory. To run code properly you just need to change dirrectory in terminal before you run server.

        cd src
    
    Now it works without `src/` in paths.

    Commit: [a929c00](https://github.com/YuriiMotov/FastAPI_study/compare/f1049923b21312cd2316afc41469dbc2aee7f020...a929c00dae8dd2ee899896a1161e3c5d6cdbfa85)


### Lesson 13 (Websockets)

[Watch original lesson on Youtube](https://youtu.be/uWSdWJEFd0Y?si=lunF-nbLSfOLm5gZ)

0. Implementation of changes made in the lesson #13

    Commit: [c098aec](https://github.com/YuriiMotov/FastAPI_study/compare/85bf2af1bfe4409cc3295678c18e32b52d496442...c098aec35daaa944140364de33980f2c3f880e47)

1. Some code refinements:

    - Move `ConnectionManager` to separate file, rename it to `ChatManager`

    - I think the "ChatManager" should encapsulate all `chat` logic, let's move all database operations to its methods and pass `session` as a parameter.

    - Getting rid of underscores in URL (it's recomended to use dashes instead)

    Commit: [f3201b9](https://github.com/YuriiMotov/FastAPI_study/compare/c098aec35daaa944140364de33980f2c3f880e47...f3201b98efa0417c203c328a73c575d6df654971) and fix: [7d4ced6](https://github.com/YuriiMotov/FastAPI_study/compare/f3201b98efa0417c203c328a73c575d6df654971...7d4ced6481cd605786460c79702cbb222348aef9)

2. Error handling.

    Now websocket endpoint is running under WEB-server and if this endpoint fails server will answer with HTML-page. That's not correct, because javascript expets json answer.

    We could add TRY..EXCEPT blocks to the endpoints that return JSON. Or we can move these endpoints to the API-server. I've chosen second variant.
    And after that it's needed to add error handling in JavaScript code, but it's not my job :)

    Commit: [90e7015](https://github.com/YuriiMotov/FastAPI_study/compare/7d4ced6481cd605786460c79702cbb222348aef9...90e70151cb28cc62d7956ac52f23360f5adfec52)

3. In FastAPI documentation it's recomended to use [encode/broadcaster](https://github.com/encode/broadcaster) for more complex tasks. Let's implement the same functional with this library.

    It turned out that there is a problem: this library doesn't support message history. And it looks like nobody is going to add this support in the near future..

    But it can be useful if you are developing a multiservice application and you need all instances to have a common message queue.

    Commit: [71ed85b](https://github.com/YuriiMotov/FastAPI_study/compare/90e70151cb28cc62d7956ac52f23360f5adfec52...71ed85b9591bf6dc0d7cf12711cb576ba4b65fec)

4. Alternatives of Websockets.

    [nice article](https://ably.com/topic/websocket-alternatives)


### Lesson 14 (How to use Depends)

[Watch original lesson on Youtube](https://youtu.be/qvzQWBEBHYw?si=kTCgwshHT0tVxCC_)

0. Implementation of changes made in the lesson #14

    Commit: [f4b6d11](https://github.com/YuriiMotov/FastAPI_study/compare/a148a155d0f3d865fca23e5f7769c0b3fb318c56...f4b6d111fdbea557c37b20fe880f31f4208958e9)

1. It's recommended in the FastAPI documentation to use `Annotated` instead of passing `Depends` as a default attribute value.

    Commit: [00734e4](https://github.com/YuriiMotov/FastAPI_study/compare/f4b6d111fdbea557c37b20fe880f31f4208958e9...00734e4a31f213a5c51e07dc4b407830014236c8)

2. Let's make oauth2 example more secure by following the FastAPI documentation

    Commit: [5003291](https://github.com/YuriiMotov/FastAPI_study/compare/00734e4a31f213a5c51e07dc4b407830014236c8...50032916b0784e6f14a660f59be7f15606db7b2f)

3. Figuring out the dependencies execution order.

    When somebody call the endpoint which has dependencies, FastAPI builds the tree of dependencies and call them in right order. Results are cached, so if you have several instances of one dependancy, it will be called once (see the `operation-with-dependencies-1` endpoint).

    Dependancies with `yield` are executed till the `yield`.

    After that the endpoint function is executed.

    If any exception occures during this process (till the moment then Response is sent), this exception will be passed to the dependencies with `yield`. You can catch it and raise other exception, including HTTPException (although, it's better not to do this), which changes HTTP-Response.

    After the endpoint's function has executed successfully and Response has sent to the client, background task starts.

    **[Depricated]** If any exception occures during the background task execution, this exception will be passed to the dependencies with `yield`. You can catch it and do whatever you want except raising HTTPException (it doesn't make sence since the Respons has sent and it will couse another exception (RuntimeError: Caught handled exception, but response already started)).

    Commit: [f805aea](https://github.com/YuriiMotov/FastAPI_study/compare/319e75f9282cf1a655f9b37d8ca25c9a5afc3b1c...f805aeaa8239277d1055d76e223661a69b4f0cbf), fix: [8c7b46d](https://github.com/YuriiMotov/FastAPI_study/compare/507ffd1bda54c7eb88559e728b6c1eb9c3c9d6fc...8c7b46d58cb7f96bc1b5eecbc2b2d137595ac559)

     **Update:** From version 0.106.0 using resources from dependencies with `yield` in background tasks is no longer supported. And now it's OK to raise `HTTPException` in dependencies after yield.

     Commit: [73a36eb](https://github.com/YuriiMotov/FastAPI_study/compare/79983568d77098fc66aec9b1c932e3ed24f8c2e0...73a36ebfe7e6aca423ded5b2bdfd005d4ee92fc5)


### Lesson 15 (Docker and Docker Compose)

[Watch original lesson on Youtube](https://youtu.be/_1H1qsNqxwM?si=EqLN4IzGoua13r98)

0. Implementation of changes made in the lesson #15

    Commit: [0b1edeb](https://github.com/YuriiMotov/FastAPI_study/compare/ebe585423ab19a8a452547cf476cf5b3a88488f8...0b1edeb486866ff644eacf2522a8a6585376c9ae)

1. User registration via `fastapi-users` doesn't work for now, because there are no any roles in DB yet.

    Let's add script wich will insert initial data into DB.

    Commit: [b1401a2](https://github.com/YuriiMotov/FastAPI_study/compare/0b1edeb486866ff644eacf2522a8a6585376c9ae...b1401a2a719f82c5f7665ef014e30c73b6bb3b55)

2. At the moment, all the data is stored in the container and will be deleted if you delete the container. Let's add `volume` to make DB data persistent.

    Now DB data is stored separately from container in `/var/lib/docker/volumes` and won't be deleted if you delete container.

    Commit: [4ee7e29](https://github.com/YuriiMotov/FastAPI_study/compare/b1401a2a719f82c5f7665ef014e30c73b6bb3b55...4ee7e290c152a0e27115006267bca98401ed2fd8)

3. This version of docker-compose file runs only api-server. But we need to run web-server too.

    Commit: [595ac10](https://github.com/YuriiMotov/FastAPI_study/compare/4ee7e290c152a0e27115006267bca98401ed2fd8...595ac10443fc9c34dd55f1e18e722253dc69ce4e)


### Lesson 16 (Software deployment on render.com)

[Watch original lesson on Youtube](https://youtu.be/OxE2UGHPOA0?si=W80lkOnWJerZCX_2)

0. Implementation of changes made in the lesson #16

    Commits: [79d4a9d](https://github.com/YuriiMotov/FastAPI_study/compare/daa8cf877d5ba2658b86c1fb19a3bc7c7d337cf1...79d4a9d94202c87dd6936f4d052c593ec610ff98) and [cfd6b0a](https://github.com/YuriiMotov/FastAPI_study/compare/79d4a9d94202c87dd6936f4d052c593ec610ff98...cfd6b0ace816c81f8ae2e9278083fcb137375b88)

1. It's not good that we had to override Dockerfile to deploy our app on render.com. By doing that our docker-compose solution was broken.

    Render.com allows to specify the directory where it will look for Dockerfile.

    Just copy Dockerfile to `docker/render_com/` in the github-repository and change in the web-app settings on render.com `Dockerfile Path` from `./Dockerfile` to `./docker/render_com/Dockerfile`. Then trigger the deployment hook.

    Revert changes of `Dockerfile` placed in the root directory of the repository to make `docker-compose` solution work again.

    Commit: [662899b](https://github.com/YuriiMotov/FastAPI_study/compare/cfd6b0ace816c81f8ae2e9278083fcb137375b88...662899b12008e182361c935b41151addfbb1a74b)

2. Let's also run our web-server.

    To do that just create one more app with the same configuration as first web-app (api-server). And set in it's settings `Docker Command`: `gunicorn main:web_app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000`.

    And I had to make some changes in source codes to use right protocols, hosts and ports.

    Commit: [c186719](https://github.com/YuriiMotov/FastAPI_study/compare/b40b72b7484f2dc6fed4e6134ff659e7140eb1de...c186719cb6f6d56d2ecba54a4f2f0be018bcc203)


### Layered architecture style

[Watch original lesson on Youtube](https://youtu.be/8Im74b55vFc?si=chm6CGhxGADsc_uh)

0. Implementation of changes made in the video

    I decided to use postgres instead of sqlite and store config in .env file. So, my implementation is a little different from original code.

    Commit: [f48cc25](https://github.com/YuriiMotov/FastAPI_study/compare/afaa60f83d288e90a231702d5631cc26d1b3d9bf...f48cc250379f6b8640dc82223e6d1f8dca1fa739)

1. A few code corrections (wrong type-hint for argument in TasksService.__init__(), SQL models and tables naming (should be singular)):

    It turned out that it's not an easy task to make alembic migration if you need to rename a table with PK, FK and sequence.. I didn't manage to find solution. So, my migration will recreate table and all data will be lost.

    Commit: [9c6c449](https://github.com/YuriiMotov/FastAPI_study/compare/79f0567c487c5c8ecc4af79b21c86dfc4fdb7bf7...9c6c449b9ae6cbb1e1d4b3450d3a5b290c13d114)


2. One of the advantages of repository pattern is decoupling from database and the possibility to quickly change the data store method. For example we want to write unit-tests and store our data in memory instead of using SQLAlchemy.

    Let's check it.
    
    To do that we have to implement `utils.repository.InMemoryRepository` class which will substitude `utils.repository.SQLAlchemyRepository`.
    But we also have to implement `repositories.tasks.TasksInMemoryRepository` class which will substitude `repositories.tasks.TasksRepository`, because
    `repositories.tasks.TasksRepository` descendant of the `utils.repository.SQLAlchemyRepository` class.
    
    I wouldn't say it looks beautiful..
    
    Commit: [2b7591d](https://github.com/YuriiMotov/FastAPI_study/compare/9c6c449b9ae6cbb1e1d4b3450d3a5b290c13d114...2b7591d846d640dc7eeacafb8c80992ad0d0c99a)
    
    
### UnitOfWork pattern with FastAPI

[Watch original lesson on Youtube](https://youtu.be/TaYg23VkCRI?si=Z8eSVQgUHS_E8Xfo)

0. Implementation of changes made in the video

    Commit: [5306df7](https://github.com/YuriiMotov/FastAPI_study/compare/fdf27d06ae78683e464fce298114408226ea5b81...5306df7df196e2b503e46b843c936b825b1877e9)

1. Fix some mistakes:

    Wrong attributes type: [23f891a](https://github.com/YuriiMotov/FastAPI_study/compare/5306df7df196e2b503e46b843c936b825b1877e9...23f891a0325a7181c13693fb085220f9082e1b32)
    
    Delete the extra field `author_id` in the `TaskSchemaEdit`: [33b4867](https://github.com/YuriiMotov/FastAPI_study/compare/23f891a0325a7181c13693fb085220f9082e1b32...33b4867a70740b37abd9eb64b00b32273d666233)
    
    Add missing methods to `AbstractRepository`: [27bb74b](https://github.com/YuriiMotov/FastAPI_study/compare/33b4867a70740b37abd9eb64b00b32273d666233...27bb74b622200ea0e5844cc3472ca806982d9d92)
    
2. Make some improvements:

    Rename implementations that related to `SQLAlchemy`, add `SQLA` prefix to make things clearer: [4105d83](https://github.com/YuriiMotov/FastAPI_study/compare/27bb74b622200ea0e5844cc3472ca806982d9d92...4105d837a7ad8097b13613dfb37b26c432059bd3)
    
    Let's hide `UnitOfWork` under the hood (we don't have to create `TasksService` instance and pass `uow` to each method anymore): [a107cec](https://github.com/YuriiMotov/FastAPI_study/compare/4105d837a7ad8097b13613dfb37b26c432059bd3...a107cec7c2a2a4a4c61cab03f795ce1f490476b7)

    Reducing code duplication in schema declarations: [2da4f96](https://github.com/YuriiMotov/FastAPI_study/compare/a107cec7c2a2a4a4c61cab03f795ce1f490476b7...2da4f9615d3acc4d246d781eb574bcea3945423a)


### Reading Fast API documentation and practicing new things

#### 1. OAuth scopes

Article: [https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/)

Let's add scopes to authorization methods, [implemented before](https://github.com/YuriiMotov/FastAPI_study/compare/00734e4a31f213a5c51e07dc4b407830014236c8...50032916b0784e6f14a660f59be7f15606db7b2f) 

Commits: [c80df85](https://github.com/YuriiMotov/FastAPI_study/compare/13f4c0634913b122afa10d9a9712a1f0523ee45a...c80df857c70c6dcec78bb5117a252c74a931246e), [ca56b21](https://github.com/YuriiMotov/FastAPI_study/compare/c80df857c70c6dcec78bb5117a252c74a931246e...ca56b2100d09a5c88b904476b3d8fca2ace4401b)


#### 2. Sub Applications - Mounts

Article: [https://fastapi.tiangolo.com/advanced/sub-applications/](https://fastapi.tiangolo.com/advanced/sub-applications/)

I have 2 applications (`web_app` and `api_app`) and have to run them separately. It's not very convenient.

Let's mount `api_app` to `web_app` with path `/api`!

FastAPI doesn't use `lifespan` for subapplications, so I combined initialization steps in one `lifespan` and use them for both apps.

Now we can run these applications either separately or together depends on settings (if `host` and `port` is the same for `web_app` and `api_app`, then `api_app` will be mounted as subapp).

Commit: [c2e5583](https://github.com/YuriiMotov/FastAPI_study/compare/4697006a3d09399a41ce76c09f66d507d842b449...c2e5583f70b6eacf4f31f005c971d95a38a39179)


#### 3. Testing WebSockets

Article: [https://fastapi.tiangolo.com/advanced/testing-websockets/](https://fastapi.tiangolo.com/advanced/testing-websockets/)

Let's test our chat. Commit: [2bb68de](https://github.com/YuriiMotov/FastAPI_study/compare/7084d30cb1c98d76dd3879f66b8163cee753aa50...2bb68def065a815f605fc5b70e7f72198032dca5)

There is a problem. If something is wrong in your route function and server doesn't send anything to client, test will be blocked in a deadloop. Commit: [77d3000](https://github.com/YuriiMotov/FastAPI_study/compare/2bb68def065a815f605fc5b70e7f72198032dca5...77d300058c867ca619864658b0a41bf3d39f8633) (Here we forward text only to client, who sent this message, but don't forward it to other connected clients).
To solve this problem it's needed to set timeout when `self._send_queue.get()` is called in `starlette.testclient.WebSocketTestSession.receive()`. I'll add an issue to `starlette` repository.

#### 4. OAuth2 with refresh tokens + rotation

Article: [https://stateful.com/blog/oauth-refresh-token-best-practices](https://stateful.com/blog/oauth-refresh-token-best-practices)

To make app more sequre it's better to set short lifetime for access tokens and user refresh token to get new access token. Along with refresh token rotetion to make it even more secure.

Commit: [056395e](https://github.com/YuriiMotov/FastAPI_study/compare/33ec4ecf8988db2ec410d77c924f2a9c6d6d0b96...056395efa8f5666cb036598501e7e7dbf5f77bea)

Several known disadvantages of this implementation: 1) it will work if only each user use one connection, 2) if malicious user steal the refresh token, they can block the ability of user to work with system until stolen token expired.

I think that writing your own authorization methods is not the best solution. It's better to use proven library instead. I'm going to try integration FastAPI with [keycloak](https://www.keycloak.org/) later. **Update:** [Done](#8-authentication-with-keycloak)


#### 5. Request rate limit

Article: [https://www.moesif.com/blog/technical/rate-limiting/Best-Practices-for-API-Rate-Limits-and-Quotas-With-Moesif-to-Avoid-Angry-Customers/](https://www.moesif.com/blog/technical/rate-limiting/Best-Practices-for-API-Rate-Limits-and-Quotas-With-Moesif-to-Avoid-Angry-Customers/)

Rate limit with `slowapi`: [commit 868887f](https://github.com/YuriiMotov/FastAPI_study/compare/f36064b9331031da7e451f5b22754bfe4451f9e8...868887f3253dd7d8f17c34111634e87a7729009a)


#### 6. SQLModel

Article: [https://sqlmodel.tiangolo.com/](https://sqlmodel.tiangolo.com/)

Let's practice using SQLModel library and refactor oauth2 methods to use SQLModel. Commit: [581ff8f](https://github.com/YuriiMotov/FastAPI_study/compare/7bdda3eee5cb7d5aac47204597bfc3a2f14ca96a...581ff8fa98e93ab1a7e776a8a9d993660067b2b8)

And let's add more complex models: Hero and Team with m2m relations. Commit: [148b8fd](https://github.com/YuriiMotov/FastAPI_study/compare/581ff8fa98e93ab1a7e776a8a9d993660067b2b8...148b8fd3660a364ccbd712fb53b0ec495b26d99b)


#### 7. Monitoring FastAPI with Prometheus and Grafana

Article: [https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn](https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn)

Commit: [450e979](https://github.com/YuriiMotov/FastAPI_study/compare/47200a94fa9cfc254fa4bc40de6e6776cd5559a5...450e9795f47f5a804ca5d7581943549fd9cbebdc)

There is a problem: when you run app with `guvicorn` then counters will be broken (every worker will have their own counter variables).

To solve this problem you should create in your app work folder empty folder with name `tmp_multiproc` before starting your app (or clear this folder if it already exists) and add enviroument variable `PROMETHEUS_MULTIPROC_DIR=/tmp_multiproc`. This looks bad but it's official solution.

Commit: [103f958](https://github.com/YuriiMotov/FastAPI_study/compare/bc440230a77bfc06f03fc5628d5dd48073628e45...103f9589023f855bc3fa3b94955de3f0d7f7360c)


#### 8. Authentication with **Keycloak**

Implementation of `direct access grants` flow. User (front-end) authenticates on Keycloak server and uses token to access protected FastAPI endpoints.

The main advantage of this approach is that we don't need to create any user managment endpoints, we delegate all of this stuff to Keycloak (which does it securely and provides a user-friendly and flexible UI).

Commit: [ff6770](https://github.com/YuriiMotov/FastAPI_study/compare/81ac4e5bf3c4bf9142cd9eacbb1f4172dbb6cdcd...ff67701fd100de35e5e6a75cfb077cfc8b661604)

