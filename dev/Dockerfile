FROM python:3.8.8

LABEL email='bomebug15@keti.re.kr'

ENV HOME=/home/
ENV resr_url = ${REST_URL}

RUN mkdir -p ${HOME}/agc2022
RUN pip install -r requirements.txt

WORKDIR ${HOME}/agc2022

COPY . .

EXPOSE 30000

CMD ["python3", "main.py"]