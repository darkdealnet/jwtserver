# API версия 1

* `/api/v1/auth/login/` - authentication.
* `/api/v1/auth/send_code/` - send SMS or Call.

## Login

`jwtserver.api.v1.views.login.py`

Read more [here](./src/jwtserver.api.v1.views.login.py)

Самая важная часть нашего API - это авторизация пользователя, наша задача - получить логин и пароль,
вернуть токен доступа и установить токен обновления в cookie.

1. Проверяем Recaptcha v3 action и минимальные требования из файла настроек
    * Если recaptcha success, идем дальше
    * Иначе возвращаем 
2. Проверяем пару логин и пароль
3. Fourth item


```Python hl_lines="8-9  11  14"
{!../src/jwtserver.api.v1.views.login.py!}
```