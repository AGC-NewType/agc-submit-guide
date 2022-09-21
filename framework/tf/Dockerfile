FROM tensorflow/tensorflow:latest-gpu

LABEL email='bomebug15@keti.re.kr'

RUN apk update && apk add --no-cache tzdata && rm -rf /var/cache/apk/*
RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone
RUN apk del tzdata

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY ./src .

CMD ["python3","main.py"]