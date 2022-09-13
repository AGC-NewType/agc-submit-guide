# agc-submit-guide
- 개요   
인공지능 그랜드 챌린지 평가 플랫폼(이하 평가 플랫폼)은 챌린저의 추론 모델을 도커 이미지로 받아 평가합니다.   
이 페이지는 챌린저가 평가 플랫폼에 추론 모델을 업로드할 수 있도록, 도커 이미지로 변환하기 위한 가이드를 제공합니다.   
본 repository에서 제공하는 세가지 폴더에 대한 설명은 다음과 같습니다.   
      
- dev : docker python 이미지 기반 도커파일 밎 request 예시 main.py   
- tf : tensorflow2.0 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드    
- torch : pytorch 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드    
    
이미지 빌드를 위해 폴더구조는  소스코드가 포함된 `/src`, 학습한 모델이 저장된 `/src/{모델 저장폴더}` 가 필요합니다. 본 예시에서는 my_model로 작성하였습니다.       
```    
├── example   
│   ├── Dockerfile    
│   └── src       
│       └── my_model
```   
--------------------------------------------------------    

소스코드 제출을 위한 과정은 다음 3가지로 분류 됩니다      
         
#### 1. 제출 파일(도커 이미지) 생성   
- 각 환경에 맞는 도커 이미지 예시를 폴더별로 작성했습니다. 기본적인 구조는 다음과 같습니다.
```
# dockerfile template
FROM {base로 사용할 이미지}

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc 

WORKDIR ${HOME}/agc # 컨테이너 work dir 정의

COPY ./src . # src 폴더의 소스코드를 도커 컨테이너로 복사

RUN pip install requests # API 사용을 위한 requests 패키지 설치 필수

CMD ["python3","main.py"]
```
- src폴더에는 참가자의 코드가 실행될 소스코드 파일이 포함되어야 합니다.   
- 마지막 CMD 명령어에는 실행될 python 파일명이 포함되어야 합니다. 위의 예시에서는 main.py에 inference 결과 생성 및 API 서버로 결과를 전송하는 내용이 포함되어 있습니다.     
    
#### 2. 추론코드 구조    
 추론코드 작성시에는 몇가지 유의사항이 존재합니다.     
- 환경변수 단위의 data path 및 API URL을 입력받기 위한 os package 사용   
- 모델 결과 전송을 위한 requests 패키지 사용   

위에서 설명한 두가지 부분에 대한 코드 명시는 다음과 같이 해주시기 바랍니다. 각 부분에 대한 코드 예시는 다음과 같습니다.   

```   
    url = os.environ['REST_URL']     
    data_path = os.environ['DATA_PATH']     
 ```   
           
```     
    answer_dict = {'answer' : answer}
    data = json.dumps(answer_dict)
    response = requests.post(url, data=data)

```
#### 3. 도커 이미지 빌드 & 이미지 추출        
- 앞서 정의한 Dockerfile를 통해 이미지를 빌드합니다. 빌드 코드는 다음과 같습니다.
```
docker build -f <Dockerfile 이름> -t <참가자ID>:<버전명>
```      
- 이후 생성한 이미지를 .tar파일로 추출합니다.    
   
```   
docker save -o [참가자ID_answer.tar] [빌드한 이미지 이름(태그포함)]    
```   
- 생성된 이미지 압축파일을 제출하시면 됩니다.
