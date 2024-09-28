FROM python:3.12.4

WORKDIR /tutorial_fastapi

COPY . . 


RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 8000

# CMD ["fastapi", "run", "tutorial_fastapi/app/main.py", "--proxy-headers", "--port", "80"]

# DEV
CMD ["uvicorn", "tutorial_fastapi.app.main:app", "--reload", "--host", "0.0.0.0"] 