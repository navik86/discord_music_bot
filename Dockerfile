FROM python:3.9
FROM openjdk:17-slim-bullseye

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app/music_bot

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
COPY ./ ./

CMD ["java", "-jar", "/config/Lavalink.jar"]
CMD ["python3", "start.py"]