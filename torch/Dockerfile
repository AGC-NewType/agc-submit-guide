FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

LABEL email='bomebug15@keti.re.kr'

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY ./src .

RUN pip install requests
EXPOSE 30000

CMD ["python3","main.py"]
