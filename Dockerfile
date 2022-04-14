FROM python:3.9

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app/music_bot

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
COPY ./ ./

CMD ["python3", "-m", "src.main"]