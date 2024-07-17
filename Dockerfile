FROM python:3.11

RUN mkdir -p /home/intent_recognition
WORKDIR /home/intent_recognition

RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD app app
ADD boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app

EXPOSE 5050
ENTRYPOINT ["./boot.sh"]