# JWT server
<p align="center">
    <em>JWTServer лёгкий и быстрый микросервис JWT.</em>
</p>
<p align="center">
<a href="https://pypi.org/project/jwtserver" target="_blank">
    <img src="https://img.shields.io/pypi/v/jwtserver?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/jwtserver" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/jwtserver.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

JWT Server является микросервисом для авторизации пользователей. Имеющий гибкие настройки и разные версии API.

## Особенности

* Быстрый старт
* Идеален для тестирование frontend
* Спецификация JWT токенов
* Основан на Fast API framework
* Постоянная поддержка

---

**Документация** [https://jwtserver.darkdeal.net [↪]](https://github.com/darkdealnet/jwtserver "JWTServer Documentation")

**Поддержка кода** [https://github.com/darkdealnet/jwtserver [↪]](https://github.com/darkdealnet/jwtserver "The Fast JWTServer")

---

## Зависимости

* **uvicorn** [https://www.uvicorn.org/ [↪]](https://www.uvicorn.org/)
* **fastapi** [https://fastapi.tiangolo.com/ [↪]](https://fastapi.tiangolo.com/)
* **starlette** [https://www.starlette.io/ [↪]](https://www.starlette.io/)
* **passlib** [https://pypi.org/project/passlib/ [↪]](https://pypi.org/project/passlib/)
* **pydantic** [https://pydantic-docs.helpmanual.io/ [↪]](https://pydantic-docs.helpmanual.io/)
* **aioredis** [https://aioredis.readthedocs.io/ [↪]](https://aioredis.readthedocs.io/)
* **python-jose** [https://pypi.org/project/python-jose/ [↪]](https://pypi.org/project/python-jose/)
* **sqlalchemy** [https://pypi.org/project/SQLAlchemy/ [↪]](https://pypi.org/project/SQLAlchemy/)
* **sqlalchemy_utils** [https://sqlalchemy-utils.readthedocs.io/ [↪]](https://sqlalchemy-utils.readthedocs.io/)
* **asyncpg** [https://pypi.org/project/asyncpg/ [↪]](https://pypi.org/project/asyncpg/)
* **psycopg2-binary** [https://pypi.org/project/psycopg2-binary/ [↪]](https://pypi.org/project/psycopg2-binary/)
* **httpx** [https://www.python-httpx.org/ [↪]](https://www.python-httpx.org/)
* **phonenumbers** [https://pypi.org/project/phonenumbers/ [↪]](https://pypi.org/project/phonenumbers/)

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

откройте _Interactive API docs_ [http://localhost:5000/docs [↪]](http://localhost:5000/docs){target=_blank}

Вы увидите автоматическую интерактивную документацию по API.

### Альтернативная API документация

откройте _Alternative  API redoc_ [http://localhost:5000/redoc [↪]](http://localhost:5000/redoc){target=_blank}

### Для продукции

* создайте файл `main.py`

```python
from jwtserver.app import app

app.debug = False
```

## Лицензия
Этот проект находится под лицензией Apache 2.0.