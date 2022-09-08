FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

LABEL email='bomebug15@keti.re.kr'

ENV HOME=/home/
ENV resr_url = ${REST_URL}
ENV data_path = $(DATA_PATH)

RUN mkdir -p ${HOME}/agc2022

WORKDIR ${HOME}/agc2022

COPY ./src .

RUN pip install requests
RUN pip install torchsummary
EXPOSE 30000

CMD ["python3","main.py"]
