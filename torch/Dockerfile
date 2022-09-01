FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY . .

CMD ["python3","main.py"]
