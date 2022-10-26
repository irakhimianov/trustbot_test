FROM python:3.10

WORKDIR /home/bot

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY /bot .
COPY main.py .
