FROM tensorflow/tensorflow:latest-gpu

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY . .

CMD ["python3","main.py"]
