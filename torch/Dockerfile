FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

ENV HOME=/home/
ENV resr_url = ${REST_URL}

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY . .
EXPOSE 30000

CMD ["python3","main.py"]
