<p align="center">
    <em>JWTServer is very light, fast. Simple setup.</em>
</p>
<p align="center">
<a href="https://pypi.org/project/jwtserver" target="_blank">
    <img src="https://img.shields.io/pypi/v/jwtserver?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/jwtserver" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/jwtserver.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Wiki** [https://github.com/darkdealnet/jwtserver/wiki](https://github.com/darkdealnet/jwtserver "JWTServer Wiki")

**Source Code** [https://github.com/darkdealnet/jwtserver](https://github.com/darkdealnet/jwtserver "The Fast JWTServer")

---

```shell
pip install jwtserver
```

### start development server
This project can make life easier for front-end development, or it can act as a full-fledged
authorization microservice based on tokens.

```python
# dev.py
from jwtserver.server import dev

if __name__ == "__main__":
    dev(host="localhost", port=5000, log_level="info")
```

### production server

```python
# main.py
from jwtserver.app import app

app.debug = False
```

### system.d

```ini
# jwtserver.service
[Unit]
Description = jwtserver daemon
After = network.target

[Service]
User = {username}
Group = {username_group}
WorkingDirectory = /home/{username}/{project_folder}/jwtserver
ExecStart = /home/{username}/.venvs/jwtserver/bin/gunicorn -c jwtserver/functions/gunicorn.py main:app
Restart = on-failure

[Install]
WantedBy = multi-user.target
```

In the root of the project, you need to create a **config.ini** file. If you omit any sections or
keys, they will be replaced with default values.

```ini
[server]
debug = True
clear_redis_before_send_code = True
host = 0.0.0.0
port = 8000
max_requests = 1000

[token]
;additional salt to make it harder to crack the token
sol = 1234567890987654321

;minutes
access_expire_time = 90
refresh_expire_time = 10800

;jwt algorithm, decode or encode token.
algorithm = HS256
;secret key for algorithm
secret_key =

[db]
sync_url =
async_url =
sync_test_url =
async_test_url =

[redis]
url = redis://localhost
max_connections = 10

[google]
;secret key for RecaptchaV3
secret_key =

[sms]
;if debug, then there is an imitation of sending SMS messages.
debug = True

;smsc.ru
provider = smsc
;class responsible for the logic of sending SMS and calls
init_class = jwtserver.functions.SMSC
login =
password =

;blocking time before resending
time_sms = 120
time_call = 90
```