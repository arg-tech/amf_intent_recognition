FROM python:3.12-slim@sha256:9e01bf1ae5db7649a236da7be1e94ffbbbdd7a93f867dd0d8d5720d9e1f89fab

RUN mkdir -p /home/intent_recognition
WORKDIR /home/intent_recognition
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD app app
ADD boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP=app

EXPOSE 5050
ENTRYPOINT ["./boot.sh"]
