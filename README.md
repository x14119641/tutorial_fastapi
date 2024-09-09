# Tutorial FastAPI 
## To initialize with poetry
```
cd tutorial_fastapi
poetry init
```

## With pipenv
```
cd tutorial_fastapi
pipenv install -r requirements.txt

## config file with your postgres credentials 
You need a config file named as **config.json** like:
```
{
    "host": "127.0.0.1",
    "user": "",
    "password": "",
    "database": "tutorial_fastapi"
}
```
## References
https://www.youtube.com/watch?v=0sOvCWFmrtA