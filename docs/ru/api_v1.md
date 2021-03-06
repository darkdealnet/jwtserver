# API версия 1

Как взаимодействовать с API нужно смотреть в **docs** [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs "Go JWT Server docs"){target=_blank, class="external-link"}


### Authorization
* [/api/v1/auth/login/](#_1) - авторизация.
* [/api/v1/auth/logout/](#_5) - уничтожение токенов.
* [/api/v1/auth/update_token/](#_7) - регистрация пользователя.

### Registration
* [/api/v1/auth/phone_status/](#_2) - проверка, доступен ли номер.
* [/api/v1/auth/send_code/](#_3) - звонок или смс.
* [/api/v1/auth/check_code/](#_4) - проверка отправленного кода.
* [/api/v1/auth/signup/](#_6) - регистрация пользователя.

## Авторизация

**POST:** `/api/v1/auth/login/` application/json

**Recaptcha Action** `LoginPage/LoginButton`

Самая важная часть нашего API - это авторизация пользователя, наша задача - получить пару логин и
пароль, вернуть токен доступа и установить refresh_token в cookie.

1. Проверяем [**Recaptcha greenlight**](recaptcha_v3.md#greenlight)
2. Проверяем пару логин и пароль
3. Создаём пару `access_token` и `refresh_token`
4. Устанавливаем _cookie_ `refresh_token` _httponly secure_

**Response:**

```json
{
  "access_token": "string",
  "token_type": "JSv1"
}
```

Не удивляйтесь, что `token_type` имеет название не `JWT`, а `JSv1` (`JWT Server version 1`).

## Проверка, доступен ли номер

**POST:** `/api/v1/auth/phone_status/` application/json

**Recaptcha Action** `SignUpPage/PhoneStatus`

Перед регистрацией пользователя нужно убедиться, что номер телефона для учётной записи свободен

1. Проверяем [**Recaptcha greenlight**](recaptcha_v3.md#greenlight).
2. Проверяем наличие номера в базе.
3. Проверяем, были ли запросы на [получение кода](#_3).

**Response**

```json
{
  "free": true,
  "telephone": "string",
  "sent": true,
  "time": 0
}
```

## Звонок или смс

**POST:** `/api/v1/auth/send_code/` application/json

Настройки по умолчанию в `config.ini` 

```ini
;не учитывать попытки звонков и смс
ignore_attempts = False

;допустимое количество попыток звонка на конкретный номер в течении {block_time_minutes}
try_call = 2

;допустимое количество отправки СМС на конкретный номер в течении {block_time_minutes}
try_sms = 2

;время блокировки, когда попытки звонков и смс закончатся
block_time_minutes = 180
```

Перед регистрацией пользователя по _номеру телефона_ нужно проверить, является ли пользователь
его владельцем. Поэтому вначале попробуем на него позвонить и если пользователь не получит звонок,
пробуем на него отправить СМС.

Каждая попытка отправки обновляет время блокировки на {block_time_minutes}.


**Successful Response**

```json
{
  "send": true,
  "time": 0,
  "method": "string"
}
```

## Проверка отправленного кода

[http://127.0.0.1:5000/docs#/default/check_code_api_v1_auth_check_code__post](http://127.0.0.1:5000/docs#/default/check_code_api_v1_auth_check_code__post)

**POST:** `/api/v1/auth/check_code/` application/json

**Recaptcha Action** `SignUpPage/CheckCode`

**Request body**

```json
{
  "telephone": "string",
  "code": 0,
  "recaptcha_token": "string"
}
```

Для проверки отправленного кода, нужно отправить сюда вместе с номером для регистрации.
JWTServer всегда сохраняет метод предыдущей отправки кода.

1. Проверяем [**Recaptcha greenlight**](recaptcha_v3.md#greenlight)

**Successful Response**

```json
{
  "telephone": "string",
  "code": 0,
  "recaptcha_token": "string"
}
```