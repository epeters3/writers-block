FROM python:3.10.5-slim-buster

WORKDIR /app

COPY requirements/model.txt requirements.txt

RUN pip install -r requirements.txt

COPY writersblock writersblock

ENTRYPOINT ["python", "-m", "writersblock.ai.main"]
