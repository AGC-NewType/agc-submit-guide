# agc-submit-guide
- 개요   
인공지능 그랜드 챌린지 평가 플랫폼(이하 평가 플랫폼)은 챌린저의 추론 모델을 도커 이미지로 받아 평가합니다.   
이 페이지는 챌린저가 평가 플랫폼에 추론 모델을 업로드할 수 있도록, 도커 이미지로 변환하기 위한 가이드를 제공합니다.   
본 repository에서 제공하는 세가지 폴더에 대한 설명은 다음과 같습니다.   
   
      
- dev : docker python 이미지 기반 도커파일 밎 request 예시 main.py   
- tf : tensorflow2.0 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드    
- torch : pytorch 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드    
    
디렉토리 구조는 다음과 같습니다.    
```
├── dev    
│   ├── Dockerfile    
│   └── src    
│       ├── main.py    
│       └── requirements.txt    
├── tf    
│   ├── Dockerfile    
│   └── src       
│       ├── dataloader.py    
│       ├── main.py    
│       └── my_model    
│           ├── checkpoint    
│           ├── epoch_001.data-00000-of-00001    
│           ├── epoch_001.index    
│           ├── keras_metadata.pb    
│           ├── saved_model.pb    
│           └── variables    
│               ├── variables.data-00000-of-00001    
│               └── variables.index    
└── torch    
    ├── Dockerfile    
    └── src    
        ├── dataloader.py    
        ├── inference.py    
        ├── main.py    
        ├── model.py    
        └── my_model    
            └── mnist_net.pth    
```            
--------------------------------------------------------    
    
1. 제출 파일(도커 이미지) 생성   
- 각 환경에 맞는 도커 이미지 예시를 폴더별로 작성했습니다. 기본적인 구조는 다음과 같습니다.
```
# dockerfile template
FROM {base로 사용할 이미지}

ENV HOME=/home/
ENV resr_url = ${REST_URL}
ENV data_path = $(DATA_PATH)

RUN mkdir -p ${HOME}/agc

WORKDIR ${HOME}/agc

COPY ./src .

RUN pip install requests

CMD ["python3","main.py"]
```
- src폴더에는 참가자의 코드가 실행될 소스코드 파일이 포함되어야 합니다.   
- 마지막 CMD 명령어에는 실행될 python 파일명이 포함되어야 합니다. 위의 예시에서는 main.py에 inference 결과 생성 및 API 서버로 결과를 전송하는 내용이 포함되어 있습니다.     
    
2. 추론코드 구조    
- TBD      
