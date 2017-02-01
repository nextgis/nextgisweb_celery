# nextgisweb_celery

## How to use

* Install to venv  
```bash
./env/bin/pip install -e ./nextgisweb-celery
```

* Create config for celery  
_celery.ini example:_
```ini
[celery]
BROKER_URL = redis://localhost:6379/1
RESULT_BACKEND = redis://localhost:6379/2
ACCEPT_CONTENT = ['application/json']
TASK_SERIALIZER = 'json'
RESULT_SERIALIZER = 'json'
```

* Add path to ngw config  
_config.ini example:_
```ini
...
[celery]
celery_conf_file = /my/path/celery.ini
...
```

* Create your task in your component  
 _tasks.py example:_
```python
from nextgisweb_celery.app import celery_app as app

@app.task(reject_on_worker_lost=True, soft_time_limit=60*60)
def add(x, y):
    return x+y
```

* Import your tasks in your component init (DO IT!)  
 _\_\_init\_\_.py example:_
```python
...
from .tasks import add
...
```

* Use your task in your component  
 _view.py example:_
```python
from .tasks import add

...
add.delay(7,5)
...
```

* Start celery
```bash
./env/bin/celery -A nextgisweb_celery.app.celery_app --ngw-config /my/path/config.ini
```

