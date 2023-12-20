FROM python:3.10.13-slim-bullseye

COPY src/ /src/app/src
COPY main.py /src/app
COPY __init__.py /src/app

COPY requirements.txt /src/app
WORKDIR /src/app
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
