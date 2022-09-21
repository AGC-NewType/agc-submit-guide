FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

LABEL email='bomebug15@keti.re.kr'

RUN apt-get update

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get install -y tzdata

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY ./src .

CMD ["python3","main.py"]
