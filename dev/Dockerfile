FROM python:3.8.8

LABEL email='bomebug15@keti.re.kr'

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get install -y tzdata

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY ./src .

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]