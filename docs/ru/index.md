# JWT server

_JWTServer лёгкий и быстрый микросервис JWT._

[![Package version](https://img.shields.io/pypi/v/jwtserver?color=%2334D058&label=pypi%20package)](https://pypi.org/project/jwtserver)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/jwtserver.svg?color=%2334D058)](https://pypi.org/project/jwtserver)

JWT Server является микросервисом для авторизации пользователей. Имеющий гибкие настройки и разные версии API.

## Особенности

* Быстрый старт
* Идеален для тестирование frontend
* Спецификация JWT токенов
* Основан на Fast API framework
* Постоянная поддержка

---

**Документация** [https://jwtserver.darkdeal.net](https://github.com/darkdealnet/jwtserver "JWTServer Documentation"){target=_blank, class="external-link"}

**Поддержка кода** [https://github.com/darkdealnet/jwtserver](https://github.com/darkdealnet/jwtserver "The JWTServer"){target=_blank, class="external-link"}

---

## Зависимости

* **uvicorn** [https://www.uvicorn.org/](https://www.uvicorn.org/ "Go Site"){target=_blank, class="external-link"}
* **fastapi** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/ "Go Site"){target=_blank, class="external-link"}
* **starlette** [https://www.starlette.io/](https://www.starlette.io/ "Go Site"){target=_blank, class="external-link"}
* **passlib** [https://pypi.org/project/passlib/](https://pypi.org/project/passlib/ "Go Site"){target=_blank, class="external-link"}
* **pydantic** [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/ "Go Site"){target=_blank, class="external-link"}
* **aioredis** [https://aioredis.readthedocs.io/](https://aioredis.readthedocs.io/ "Go Site"){target=_blank, class="external-link"}
* **python-jose** [https://pypi.org/project/python-jose/](https://pypi.org/project/python-jose/ "Go Site"){target=_blank, class="external-link"}
* **sqlalchemy** [https://pypi.org/project/SQLAlchemy/](https://pypi.org/project/SQLAlchemy/ "Go Site"){target=_blank, class="external-link"}
* **sqlalchemy_utils** [https://sqlalchemy-utils.readthedocs.io/](https://sqlalchemy-utils.readthedocs.io/ "Go Site"){target=_blank, class="external-link"}
* **asyncpg** [https://pypi.org/project/asyncpg/](https://pypi.org/project/asyncpg/ "Go Site"){target=_blank, class="external-link"}
* **psycopg2-binary** [https://pypi.org/project/psycopg2-binary/](https://pypi.org/project/psycopg2-binary/ "Go Site"){target=_blank, class="external-link"}
* **httpx** [https://www.python-httpx.org/](https://www.python-httpx.org/ "Go Site"){target=_blank, class="external-link"}
* **phonenumbers** [https://pypi.org/project/phonenumbers/](https://pypi.org/project/phonenumbers/ "Go Site"){target=_blank, class="external-link"}

## Установка

```shell
python -m pip install jwtserver 
```

## Примеры:

### Для разработки

* создайте файл `dev.py`

```python
from jwtserver.server import dev

if __name__ == "__main__":
    dev(host="localhost", port=5000, log_level="info")
```

### Интерактивная API документация

откройте _Interactive API docs_ [http://localhost:5000/docs](http://localhost:5000/docs "Go Site"){target=_blank, class="external-link"}

Вы увидите автоматическую интерактивную документацию по API.

### Альтернативная API документация

откройте _Alternative  API redoc_ [http://localhost:5000/redoc](http://localhost:5000/redoc "Go Site"){target=_blank, class="external-link"}

### Для продукции

* создайте файл `main.py`

```python
from jwtserver.app import app

app.debug = False
```

## Лицензия
Этот проект находится под лицензией Apache 2.0.