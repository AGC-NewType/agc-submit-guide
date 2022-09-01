FROM python:3.8.8

LABEL email='bomebug15@keti.re.kr'

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
