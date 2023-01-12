FROM python:3.8-slim

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update && pip install --upgrade pip

COPY requirements.txt .
COPY app.py .
COPY model.pkl .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000"]
