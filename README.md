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
```
## Add config file with your postgres credentials 
You need a config file named as **config.json** like:

```json
{
    "host": "127.0.0.1",
    "user": "",
    "password": "",
    "database": "tutorial_fastapi"
}
```

## Add secrets file 
You need a config file named as **secrets.json** like:

```json
{
    "SECRET_KEY" : "my_secret",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES" : 30
}
```
And you can use the following command to create a secret key:
```
openssl rand -hex 32
```

# Don't forget to start postgres!
```
sudo systemctl start postgresql
```

# Start application in dev mode
```
fastapi dev tutorial_fastapi/app/main.py  
```

## References
https://www.youtube.com/watch?v=0sOvCWFmrtA