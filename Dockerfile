FROM python:3

RUN mkdir -p /home/intent_recognition
WORKDIR /home/intent_recognition

RUN pip install --upgrade pip
RUN pip install tensorflow==2.12.*
RUN pip install torch
RUN pip install transformers
RUN pip install -U scikit-learn

ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD app app
ADD boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]