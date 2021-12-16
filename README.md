```python
from jwtserver.server import dev

if __name__ == "__main__":
    dev(host="localhost", port=5000, log_level="info")
```

```python
# main.py
from jwtserver.app import app
app.debug = False
```


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