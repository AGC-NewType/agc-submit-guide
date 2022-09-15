# agc-submit-guide
- 개요   
인공지능 그랜드 챌린지 평가 플랫폼(이하 평가 플랫폼)은 챌린저의 추론 모델을 도커 이미지로 받아 평가합니다.   
이 페이지는 챌린저가 평가 플랫폼에 추론 모델을 업로드할 수 있도록, 도커 이미지로 변환하기 위한 가이드를 제공합니다.   
본 repository에서 제공하는 세 가지 폴더에 대한 설명은 다음과 같습니다.   
      
- dev : python 이미지 기반 도커파일 밎 request POST 예시 main.py   
- tf : tensorflow2.0 framework 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드    
- torch : pytorch framework 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드    
    
이미지 빌드를 위해 폴더구조는  소스코드가 포함된 `/src`에 소스코드를 저장하는 구조를 사용했습니다. 해당폴더에 실행할 소스코드를 넣어서 빌드해주시기 바랍니다. 하단의 디렉토리 구조는 이해를 돕기위한 예시이며, 본 예시에서는 학습한 모델이 저장된 폴더를 my_model로 작성하였습니다.       
```    
├── example   
│   ├── Dockerfile    
│   └── src       
│       └── my_model
│       └── main.py
```   
--------------------------------------------------------    

본 가이드 페이지에서 제공하는 소스코드 제출을 위한 과정은 다음 3가지로 분류 됩니다      
         
#### 1. 제출 파일(도커 이미지) 생성   
- 각 환경에 맞는 도커 이미지 예시를 폴더별로 작성했습니다.    
- 도커파일의 이름을 별도로 지정하지 않을경우 ```Dockerfile``` 로 작성해야 빌드가 정상적으로 이루어 집니다.     
- 다른이름으로 생성한 도커파일을 사용할 경우에는 ```docker build -f <생성한 도커파일 이름> -t ...``` 을 사용하시기 바랍니다.    
- 기본적인 도커파일 내부구조는 다음과 같습니다.    
    
```    
# dockerfile template   
FROM {base로 사용할 이미지}   

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc 

WORKDIR ${HOME}/agc # 컨테이너 work dir 정의

COPY ./src . # src 폴더의 소스코드를 도커 컨테이너로 복사

CMD ["python3","main.py"] # 실행할 main.py 코드. 파일명이 다를경우 해당 파일명 기재
```    

- 본 예시는 /src 폴더와 Dockerfile이 동일한 디렉토리에 있는 경우의 빌드과정을 나타냅니다.    
- 소스코드가 저장된 폴드 이름이 ```/src```가 아닐 경우 ```dockerfile```에서 복사할 폴더이름과 해당폴더 이름을 동일하게 맞춰주면 됩니다.     
- 마지막 CMD 명령어에는 실행될 python 파일명이 포함되어야 합니다. 본 저장소의 각 폴더별 main.py에 inference 결과 생성 및 API 서버로 결과를 전송하는 내용이 포함되어 있습니다.     
- tensorflow, pytorch의 경우 base이미지의 버전에 따라 코드실행 여부가 결정됩니다. 확인하고 빌드에 참고해주시기 바랍니다.    
    
#### 2. 추론코드 구조    
 추론코드 작성시에는 몇가지 유의사항이 존재합니다.     
- 환경변수 단위의 data path 및 API URL 및 Header를 입력받기 위한 os package 사용   
- API Call을 위한 결과값 json dump 및 request 과정


위에서 설명한 두가지 부분에 대한 코드 명시는 다음과 같이 작성바랍니다. 각 부분에 대한 코드 예시는 다음과 같으며, 해당 내용은 [tf/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/tf/src/main.py), [torch/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/torch/src/main.py)에서 확인할 수 있습니다.   

```   
    # load environment variable
    url = os.environ['REST_URL']     
    data_path = os.environ['DATA_PATH']     
    headers = os.environ['API_HEADER']
 ```   
    
API서버에 모델의 결과값을 전달할때는 json형식으로 변환이 필요합니다.            
    
```     
    answer_dict = {'answer' : answer}    
    data = json.dumps(temp).encode('utf8')    
    req =  request.Request(url, data=data, headers=headers)        
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
