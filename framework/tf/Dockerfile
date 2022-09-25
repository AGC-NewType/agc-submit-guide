FROM tensorflow/tensorflow:latest-gpu

LABEL email='bomebug15@keti.re.kr'

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get install -y tzdata

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc2022/data

WORKDIR ${HOME}/agc2022

COPY ./src .
COPY ./template.json ${HOME}/agc2022/data

CMD ["python3","main.py"]