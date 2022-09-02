FROM tensorflow/tensorflow:latest-gpu

ENV HOME=/home/
ENV resr_url = ${REST_URL}

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY . .
EXPOSE 30000

CMD ["python3","main.py"]
