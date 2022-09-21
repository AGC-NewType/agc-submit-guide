# AGC-submit-guide
- 개요   
인공지능 그랜드 챌린지 평가 플랫폼(이하 평가 플랫폼)은 챌린저의 추론 모델을 도커 이미지로 받아 평가합니다.   
이 페이지는 챌린저가 평가 플랫폼에 추론 모델을 업로드할 수 있도록, 도커 이미지로 변환하기 위한 가이드를 제공합니다. 본 repository에서 제공하는 세 가지 폴더에 대한 설명은 다음과 같습니다.   
      
- dev : python 이미지 기반 도커파일 밎 request POST 예시 main.py   
- tf : tensorflow2.0 framework 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드    
- torch : pytorch framework 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드    
    
이미지 빌드를 위해 폴더구조는  소스코드가 포함된 `/src`에 소스코드를 저장하는 구조를 사용했습니다. 해당폴더에 실행할 소스코드를 넣어서 빌드해주시기 바랍니다. 하단의 디렉토리 구조는 이해를 돕기위한 예시이며, 본 예시에서는 학습한 모델이 저장된 폴더를 my_model로 작성하였습니다.       
```bsh    
├── example   
│   ├── Dockerfile    
│   └── src    
│       └── my_model    
│       └── main.py    
```   
--------------------------------------------------------    

본 가이드 페이지에서 제공하는 소스코드 제출을 위한 과정은 다음 3가지로 분류 됩니다.      
         
#### 1. 제출 파일(도커 이미지) 생성   
- 각 환경에 맞는 도커 이미지 예시를 폴더별로 작성했습니다.    
- 도커파일의 이름을 별도로 지정하지 않을경우 ```Dockerfile``` 로 작성해야 빌드가 정상적으로 이루어 집니다.     
- 다른이름으로 생성한 도커파일을 사용할 경우에는 ```docker build -f <생성한 도커파일 이름> -t ...``` 을 사용하시기 바랍니다.    
- 기본적인 도커파일 내부구조는 다음과 같습니다.    
    
```dockerfile    
# dockerfile template   
FROM {base로 사용할 이미지}   

# 한국 시간대 설정
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get install -y tzdata

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc 

WORKDIR ${HOME}/agc # 컨테이너 work dir 정의

COPY ./src . # src 폴더의 소스코드를 도커 컨테이너로 복사

CMD ["python3","main.py"] # 실행할 main.py 코드.
```    

- 본 예시는 /src 폴더와 Dockerfile이 동일한 디렉토리에 있는 경우의 빌드과정을 나타냅니다.    
- 소스코드가 저장된 디렉토리 이름이 ```/src```가 아닐 경우 ```dockerfile```에서 복사할 폴더이름과 해당폴더 이름을 동일하게 맞춰주면 됩니다.     
- 마지막 CMD 명령어에는 실행될 python 파일명이 포함되어야 합니다. 파일명은 main.py로 작성해야합니다. main.py가 아닐경우 점수산정에 어려움이 있습니다.     
- tensorflow, pytorch의 경우 base이미지의 버전에 따라 코드실행 여부가 결정됩니다.     
----------    
#### 2. 추론코드 구조    
 추론코드 작성시에는 몇가지 유의사항이 존재합니다.     
> - 환경변수 단위의 API URL을 입력받기 위한 os package 사용, Request를 위한 urllib 패키지 사용   
> - API 결과값 json dump 및 model inference 결과값 request 과정

환경변수 설정은 [framework/tf/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/tf/src/main.py), [framework/torch/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/torch/src/main.py)에서 확인할 수 있습니다. 

- "REST_URL" 환경변수 로드 예시
```python   
    # load environment variable
    url = os.environ['REST_URL']     
 ```   
    
API request는 배치가 끝날때마다 시행이 되도록 코드를 작성해야 합니다. API Request 과정은 inference 과정에서 매 배치마다 API server로 request하도록 코드작성을 해야합니다. API서버에 모델의 결과값을 전달할때는 json형식으로 변환이 필요합니다. json dump 과정에서 'unicode-escape'로 encoding 형식을 지정해야하며, request return값을 출력하는 부분에서는 unicode를 UTF-8로 디코딩을 통해 python으로 출력이 되도록 코드를 작성해야합니다.         
- 해당부분은 [framework/tf/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/tf/src/main.py), [framework/torch/src/inference.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/torch/src/inference.py)에서 확인할 수 있습니다.    

- API request 예시    
``` python    
    batch_answer = {'answer': batch_label}
    
    # apply unicode to str json data
    data = json.dumps(batch_answer).encode('unicode-escape')
    # request ready
    req =  request.Request(url, data=data)
    
    # POST to API server
    resp = request.urlopen(req)
    
    # check POST result
    status = resp.read().decode('utf8')
    if "OK" in status:
        print("batch : "+str(batch+1)+"'s result requests successful!!")
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
- 생성된 이미지 압축파일 [참가자ID_answer.tar]을 제출하시면 됩니다.
