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

**Документация** <a href="https://jwtserver.darkdeal.net/" target="_blank">https://jwtserver.darkdeal.net/</a>

**Поддержка кода** <a href="https://github.com/darkdealnet/jwtserver" target="_blank">https://github.com/darkdealnet/jwtserver</a>

---

## Зависимости

* **uvicorn** <a href="https://www.uvicorn.org/" target="_blank" class="external-link">https://www.uvicorn.org/</a>
* **fastapi** <a href="https://fastapi.tiangolo.com/" target="_blank" class="external-link">https://fastapi.tiangolo.com/</a>
* **starlette** <a href="https://www.starlette.io/" target="_blank" class="external-link">https://www.starlette.io/</a>
* **passlib** <a href="https://pypi.org/project/passlib/" target="_blank" class="external-link">https://pypi.org/project/passlib/</a>
* **pydantic** <a href="https://pydantic-docs.helpmanual.io/" target="_blank" class="external-link">https://pydantic-docs.helpmanual.io/</a>
* **aioredis** <a href="https://aioredis.readthedocs.io/" target="_blank" class="external-link">https://aioredis.readthedocs.io/</a>
* **python-jose** <a href="https://pypi.org/project/python-jose/" target="_blank" class="external-link">https://pypi.org/project/python-jose/</a>
* **sqlalchemy** <a href="https://pypi.org/project/SQLAlchemy/" target="_blank" class="external-link">https://pypi.org/project/SQLAlchemy/</a>
* **sqlalchemy_utils** <a href="https://sqlalchemy-utils.readthedocs.io/" target="_blank" class="external-link">https://sqlalchemy-utils.readthedocs.io/</a>
* **asyncpg** <a href="https://pypi.org/project/asyncpg/" target="_blank" class="external-link">https://pypi.org/project/asyncpg/</a>
* **psycopg2-binary** <a href="https://pypi.org/project/psycopg2-binary/" target="_blank" class="external-link">https://pypi.org/project/psycopg2-binary/</a>
* **httpx** <a href="https://www.python-httpx.org/" target="_blank" class="external-link">https://www.python-httpx.org/</a>

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

откройте _Interactive API docs_ <a href="http://localhost:5000/docs" target="_blank" class="external-link">http://localhost:5000/docs</a>

Вы увидите автоматическую интерактивную документацию по API.

### Альтернативная API документация

откройте _Alternative  API redoc_ <a href="http://localhost:5000/redoc" target="_blank" class="external-link">http://localhost:5000/redoc</a>

### Для продукции

* создайте файл `main.py`

```python
from jwtserver.app import app

app.debug = False
```

## Лицензия
Этот проект находится под лицензией Apache 2.0.