FROM python:3.8.8-slim

LABEL email='bomebug15@keti.re.kr'

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get install -y tzdata

ENV HOME=/home/agc2022

RUN mkdir -p ${HOME}/agc2022

RUN pip install flask

WORKDIR ${HOME}

COPY ./src .

CMD ["python3", "rest-host.py"]