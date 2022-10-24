# AGC-submit-guide
- 개요   
인공지능 그랜드 챌린지 대회 운영 온라인 평가 플랫폼 (이하 평가 플랫폼)은 챌린저의 추론 모델로 만들어진 도커 이미지를 입력으로 합니다.     
이 페이지는 챌린저가 평가 플랫폼에 추론 모델을 업로드할 수 있도록, 도커 이미지로 변환하기 위한 가이드를 제공합니다. 본 repository에서 제공하는 세 가지 폴더에 대한 설명은 다음과 같습니다.      
     
- dev : python 이미지 기반 도커파일 밎 request POST 예시 main.py    
- framework : tensorflow 및 pytorch 이미지 기반의 코드 구조 예    
  - tf : tensorflow2.0 framework 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드      
  - torch : pytorch framework 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드       
    
아래 구조는 이미지 빌드를 위한 디렉토리 구조 예시 입니다.    
```bsh    
├── example   
│   ├── Dockerfile    
│   └── src    
│       └── my_model    
│       └── main.py    
```     
     
- 작업된 소스코드는 `/src`에 넣어 빌드를 진행해 주세요. (본 예시에서는 학습한 모델이 저장된 폴더를 my_model로 작성하였습니다.)    
    
- 3차 대회 관련 공지는 [3차대회 공지사항](#3차-대회-관련-공지)을 참고해주시기 바랍니다.    

--------------------------------------------------------    
    
본 가이드 페이지에서 제공하는 도커 이미지 빌드를 위한 과정은 다음 3가지로 분류 됩니다.      
         
### 1. 제출 파일(도커 이미지) 생성   
- 각 환경(tensorflow, pytorch)에 맞는 도커 이미지 예시를 폴더별로 작성했습니다.    
- 도커 이미지 빌드를 위한 도커 파일의 이름은 ```Dockerfile``` 로 작성합니다. (recomended).
- 기본적인 도커파일 내부구조는 다음과 같습니다.    
    
```dockerfile    
# dockerfile template   
FROM {base로 사용할 이미지}   

# 한국 시간대 설정
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get install -y tzdata

ENV HOME=/home/

RUN mkdir -p ${HOME}/agc/dataset

WORKDIR ${HOME}/agc # 컨테이너 work dir 정의

COPY ./src . # src 폴더의 소스코드를 도커 컨테이너로 복사

CMD ["python3","main.py"] # 실행할 main.py 코드.
```    

- 본 예시는 /src 폴더와 Dockerfile이 동일한 디렉토리에 있는 경우의 빌드과정을 나타냅니다.    
- 소스코드가 저장된 디렉토리 이름이 ```/src```가 아닐 경우 ```dockerfile```에서 복사할 폴더이름과 해당폴더 이름을 동일하게 맞춰주면 됩니다.     
- 마지막 CMD 명령어에는 실행될 python 파일명이 포함되어야 합니다. 그렇지 않을 경우, 평가 플랫폼에서의 구동이 제한됩니다.         
- public pytorch image를 사용할 경우 도커파일 내부 이미지 선언부 하단에 'RUN apt-get update'를 추가해야 timezone 관련 설정이 정상적으로 작동합니다.     
    
----------    
    
### 2. 추론코드 작성    
     
 추론코드 작성시에는 몇가지 유의사항이 존재합니다.     
      
> - 환경변수 단위의 API URL을 입력받기 위한 os package 사용, Request를 위한 urllib 패키지 사용        
> - API 결과값 json dump 및 model inference 결과값 request 과정        
      
환경변수 설정은 실행될 source code main.py 상단부에 작성해야합니다. 해당 예시는 [dev/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/dev/src/main.py), [framework/tf/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/framework/tf/src/main.py), [framework/torch/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/framework/torch/src/main.py)에서 확인할 수 있습니다. 또한, data_path는 '/home/agc2022/dataset' 으로 작성합니다.    
    
- python 환경변수 로드 예시     
```python    
    # load environment variable
    url = os.environ['REST_ANSWER_URL']    
    data_path = '/home/agc2022/dataset'     
 ```     
- REST API 수신 주소는 추론코드가 구동되는 평가 플랫폼에 환경 변수('REST_ANSWER_URL')로 정의되어 있습니다.     
    
추론 과정에서 답안 제출은 REST API를 활용하여 온라인 평가 플랫폼에 전송합니다. 제출은 batch 단위로 진행해야하며, 세부문제정의서에서 언급한 메시지 구조를 따라야합니다. 다음 예시는 batch_size를 1, 전체 데이터가 20개라고 가정했을때 batch 단위 답안제출 예시 json 입니다. (상세 메시지 구조 등은 세부문제정의서 참조)    
- **batch단위 답안 제출 예시**
```json
{
    "team_id": "userxx",
    "secret": "!@#$%^&*()",
    "answer_sheet": 
        {
            "no": "1",
            "answer": "4"
        }
}
```    
API POST 과정에는 두가지 유의사항이 존재합니다.    
>- json dump 과정에서 'unicode-escape'로 encoding 형식을 지정합니다.     
>- 제출 성공 여부를 판별하기 위해 request return값을 출력하는 부분에서는 unicode를 UTF-8로 디코딩을 통해 python으로 출력이 되도록 코드를 작성합니다.     
     
하단의 예시는 tensorflow기반 MNIST inference 예제 입니다. 본 예시에서는 batch를 1로 설정하여 이미지당 답안을 POST하도록 작성했습니다. 관련 내용은 [framework/tf/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/tf/src/main.py), [framework/torch/src/inference.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/torch/src/inference.py)에서 확인할 수 있습니다.    

- 결과값 POST 예시
``` python    
    # model load & predict
    model = tf.keras.models.load_model("./my_model")
    
    for batch,data in enumerate(inference_loader):        
        # define answer template per batch
        template = {
            "team_id": "userxx",
            "secret": "!@#$%^&*()",
            "answer_sheet": {}
        }
                
        # get inference result 
        output = model(data)
        
        # extract label from inference output
        batch_label = [int(np.argmax(sample)) for sample in output]
        tmp_answer = {"no":str(batch+1), "answer" : str(batch_label[0])}
        template['answer_sheet'] = tmp_answer
        
        # apply unicode to str json data
        data = json.dumps(template).encode('unicode-escape')

        # request ready
        req =  request.Request(api_url, data=data)
        
        # POST to API server
        resp = request.urlopen(req)
        
        # check POST result
        status = resp.read().decode('utf8')
        if "OK" in status:
            print("batch : "+str(batch+1)+"'s result requests successful!!")
```     
    
               
### 3. 도커 이미지 빌드 & 이미지 추출        
- 앞서 정의한 Dockerfile를 통해 이미지를 빌드합니다.     
- 도커 이미지를 정의한 파일명이 Dockerfile일 경우 `-f <Dockerfile 이름>` 부분을 제외하고 명령어를 입력하면 빌드가 진행됩니다.    
- 그렇지 않을 경우 `-f <Dockerfile 이름>` 을 꼭 명시해주시기 바랍니다.    
- 빌드 코드는 다음과 같습니다.      
```
docker build -f <Dockerfile 이름> -t <참가자ID>:<태그명> .
```      
- 이후 생성한 이미지를 .tar파일로 추출합니다.    
   
```   
docker save -o [참가자ID.tar] [빌드한 이미지 이름(태그포함)]    
```   
- 생성된 이미지 압축파일 [참가자ID.tar]을 온라인 평가 플랫폼에 제출하시면 됩니다.

-------------------------
### 3차 대회 관련 공지    

#### 3차대회 참가팀은 ROS 사용을 위해 {특정 디렉토리}의 Dockerfile ros_entrypoint.sh user_command.sh main.py를 참고하시면 됩니다.    

-  3차 대회 관련 추가 폴더 내부구조

```
├── Dockerfile
└── src
    ├── main.py
    ├── requirements.txt
    ├── ros_entrypoint.sh
    └── user_command.bash
```

#### 수정 필요 사항    
- Dockerfile : ROS_MASTER_URI, ROS_HOST_NAME 등 수정    
- main.py : MESSAGE_MISSION_START의 "team_id" 수정    
- main.py : (TODO) main 함수 내 참가팀 모델로부터 답안 생성 및 제출하는 부분 수정    

#### 수정 금지 사항    
- main.py : 미션 시작 메시지 전송을 위한 MissionStart 클래스 및 main 함수 내 호출 부분 수정 금지    