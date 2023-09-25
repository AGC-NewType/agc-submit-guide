# AGC-submit-guide
### 개요   
인공지능 그랜드 챌린지 대회 운영 온라인 평가 플랫폼 (이하 평가 플랫폼)은 챌린저의 추론 모델로 만들어진 도커 이미지를 입력으로 합니다.

이 페이지는 챌린저가 평가 플랫폼에 추론 모델을 업로드할 수 있도록, 도커 이미지로 변환하기 위한 가이드를 제공합니다.

본 repository에서 제공하는 세 가지 폴더에 대한 설명은 다음과 같습니다.
     
- dev : python 이미지 기반 도커파일 밎 request POST 예시 main.py    
- framework : tensorflow 및 pytorch 이미지 기반의 코드 구조 예    
  - tf : tensorflow2.0 framework 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드      
  - torch : pytorch framework 이미지 기반 도커파일 및 MNIST inference request 예시 소스코드       
    
아래 구조는 이미지 빌드 디렉토리 구조 예시 입니다.    
```bsh    
├── example   
│   ├── Dockerfile    
│   └── src    
│       └── my_model    
│       └── tmp
│       └── main.py    
```     
     
- 작업된 소스코드는 `/src`에 넣어 빌드를 진행해 주세요. (본 예시에서는 학습한 모델이 저장된 폴더를 my_model로 작성하였습니다.)    
- 추론진행 중, 임시 쓰기(write)가 가능한 경로는 `/src/tmp`로 제공됩니다.(15GB 제한)
- 참가자분들께서는 [**참가자 유의사항**](#참가자-유의사항)을 꼭 확인해주시기 바랍니다.

<!-- - 신규 대회 관련 공지는 [**신규 대회 공지사항**](#신규-대회-공지사항)을 참고해주시기 바랍니다. -->

- 사용하시는 개발 환경이 Apple Slicon(M1,M2)칩을 사용중일경우 [**Apple Slicon 컴퓨터 빌드 관련 공지**](#apple-slicon-컴퓨터-빌드-관련-공지)를 참고하여 이미지를 빌드해주시기 바랍니다.
--------------------------------------------------------    
    
본 가이드 페이지는 아래 4가지 항목으로 구분하여 도커 이미지 빌드 과정을 안내합니다.
- [**1. 제출 파일(도커 이미지) 생성**](#1-제출-파일도커-이미지-생성)
- [**2. 추론코드 작성**](#2-추론코드-작성)
- [**3. 도커 이미지 빌드 & 이미지 추출**](#3-도커-이미지-빌드--이미지-추출)
- [**4.제출 안내 사항**](#4-제출-안내-사항)

## 1. 제출 파일(도커 이미지) 생성   
- 각 환경(tensorflow, pytorch)에 맞는 도커 이미지 예시를 폴더별로 작성했습니다.    
- 도커 이미지 빌드를 위한 도커 파일 이름은 ```Dockerfile``` 로 작성합니다. (recomended).
- 기본적인 도커파일 내부구조는 다음과 같습니다.    
    
```dockerfile    
# dockerfile template   
# ex) pytorch 사용시 : FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime
#     tensorflow 사용시 : FROM tensorflow/tensorflow:latest-gpu
#     ubuntu 사용시 : FROM ubuntu:18.04
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
- 사용할 이미지는 참가자분들께서 구현하려는 환경에 맞는 이미지를 사용하시기를 권장드립니다.
- 본 예시는 /src 폴더와 Dockerfile이 동일한 디렉토리에 있는 경우의 빌드과정을 나타냅니다.    
- 소스코드가 저장된 디렉토리 이름이 ```/src```가 아닐 경우 ```dockerfile```에서 복사할 폴더이름과 해당폴더 이름을 동일하게 맞춰주면 됩니다.     
- 마지막 CMD 명령어에는 실행될 python 파일명이 포함되어야 합니다. 그렇지 않을 경우, 평가 플랫폼에서의 구동이 제한됩니다.         
- public pytorch image를 사용할 경우 도커파일 내부 이미지 선언부 하단에 `RUN apt-get update`를 추가해야 timezone 관련 설정이 정상적으로 작동합니다.     
- 도커파일 작성 참고는 [dev/Dockerfile](https://github.com/AGC-NewType/agc-submit-guide/blob/main/dev/Dockerfile), [framework/tf/Dockerfile](https://github.com/AGC-NewType/agc-submit-guide/blob/main/framework/tf/Dockerfile), [framework/torch/Dockerfile](https://github.com/AGC-NewType/agc-submit-guide/blob/main/framework/torch/Dockerfile) 의 예시를 참고해주시기 바랍니다.

### Apple Slicon 컴퓨터 빌드 관련 공지
- Apple Slicon의 경우 Dockerfile의 이미지 로딩 부분에서 다음과 같이 작성해주시기 바랍니다.
```dockerfile
# --platform을 통한 크로스 플랫폼 빌드
FROM --platform=linux/amd64 {base로 사용할 이미지}    

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
    
----------    
    
## 2. 추론코드 작성    
     
 추론코드 작성시에는 몇가지 유의사항이 존재합니다.     
      
> - 환경변수 단위의 API URL을 입력받기 위한 os package 사용, Request를 위한 urllib 패키지 사용        
> - API 결과값 json dump 및 model inference 결과값 request 과정        
> - 추론 모델 수행 종료 및 채점 요청을 위한 'end of mission' message POST
      
환경변수 설정은 실행될 source code main.py 상단부에 작성해야합니다. 해당 예시는 [dev/src/main.py](https://github.com/AGC-NewType/agc-submit-guide/blob/main/dev/src/main.py), [framework/tf/src/main.py](https://github.com/AGC-NewType/agc-submit-guide/blob/main/framework/tf/src/main.py), [framework/torch/src/main.py](https://github.com/AGC-NewType/agc-submit-guide/blob/main/framework/torch/src/main.py)에서 확인할 수 있습니다. 또한, data_path는 `'/home/agc/dataset'` 으로 작성합니다.    
    
- python 환경변수 로드 예시     
```python    
    # load environment variable
    api_url = os.environ['REST_ANSWER_URL']    
    data_path = '/home/agc/dataset'     
 ```     
- REST API 수신 주소는 추론코드가 구동되는 평가 플랫폼에 환경 변수('REST_ANSWER_URL')로 정의되어 있으며, 챌린저께서는 코드 내에서 위 환경 변수 값을 읽어와 사용하시면 됩니다.
    
추론 과정에서 생성되는 답안 제출은 REST API를 활용하여 온라인 평가 플랫폼 내 채점서버로 전송합니다. 제출은 batch 단위로 진행해야하며, 반드시 세부문제정의서에서 언급한 메시지 구조를 따라야합니다. 다음 예시는 유형별 답안제출 예시 json 입니다. 유형별 제출 방식에 차이가 존재하므로 참가자분들께서는 참고하시기 바랍니다. (상세 메시지 구조 등은 세부문제정의서 참조)     
- **batch단위 답안 제출 예시**
- **"userxx"** 와 **"hash"** 값은 이해를 돕기 위한 예시입니다. 각 팀 단위 id와 hash 값을 기입해 주세요. (팀명이 아닌, 팀ID 입니다.)
```json
# 유형 1 답안 제출 예시:
{
   "id": "userxx",
   "hash": "!@#$%^&*()",
   "report_no": "001",
   "report_part": "1",
   "answer": []
}

# 유형 2 답안 제출 예시:
{
   "id": "userxx",
   "hash": "!@#$%^&*()",
   "report_no": "002",
   "report_part": "2",
   "answer": []
}

# 유형 3 답안 제출 예시:
{
   "id": "userxx",
   "hash": "!@#$%^&*()",
   "report_no": "003",
   "report_part": "3",
   "answer": ""
}

# 유형 4 답안 제출 예시:
{
   "id": "userxx",
   "hash": "!@#$%^&*()",
   "report_no": "004",
   "report_part": "4",
   "answer": "",
   "evidence": []
}
```    
API POST 과정에는 두가지 유의사항이 존재합니다.     
>- json dump 과정에서 'utf-8'로 encoding 형식을 지정합니다.      
>- REST API로의 답안 제출 후, 응답 메시지를 확인할 수 있으며 이 또한 utf8로 디코딩하여 메시지를 확인하실 수 있습니다.       



end of mission은 채점서버에 답안지 제출이 끝남을 알리는 message입니다. 이에 따라 'report_no', 'report_part'를 포함하지 않습니다.         

'end of mission' POST 형식은 다음과 같습니다.    

```json
    {
    "id": "userxx",
    "hash": "!@#$%^&*()",
    "end_of_mission": "true"
    }
```     
         
하단의 예시는 tensorflow기반 MNIST inference 예제 입니다. 본 예시에서는 batch를 1로 설정하여 이미지당 답안을 POST하도록 작성했습니다. 관련 내용은 [framework/tf/src/main.py](https://github.com/AGC-NewType/agc-submit-guide/blob/main/framework/tf/src/main.py), [framework/torch/src/inference.py](https://github.com/AGC-NewType/agc-submit-guide/blob/main/framework/torch/src/inference.py), [framework/torch/src/main.py](https://github.com/AGC-NewType/agc-submit-guide/blob/main/framework/torch/src/main.py)에서 확인할 수 있습니다.    

- 결과값 POST 예시
``` python    
    # model load & predict
    model = tf.keras.models.load_model("./my_model")
    
    for batch,data in enumerate(inference_loader):        
        # define answer template per batch
        template = {
            "id": "userxx",
            "hash": "!@#$%^&*()",
            "report_no": "001",
            "report_part": "1",
            "answer": {}
        }
                
        # get inference result 
        output = model(data)
        
        # extract label from inference output
        batch_label = [int(np.argmax(sample)) for sample in output]
        tmp_answer = {"no" : str(batch+1), "answer" : str(batch_label[0])}
        template['answer'] = tmp_answer
        
        # apply utf-8 to str json data
        data = json.dumps(template).encode('utf-8')

        # request ready
        req =  request.Request(api_url, data=data)
        
        # POST to API server
        resp = request.urlopen(req)
        
        # check POST result
        resp_json = eval(resp.read().decode('utf8'))

        if "OK" == resp_json['status']:
            print("data requests successful!!")
        elif "ERROR" == resp_json['status']:    
            received_message=resp_json['msg']
            raise ValueError(received_message)  
    
    # request end of mission message
    message_structure = {
    "id": "userxx",
    "hash": "!@#$%^&*()",
    "end_of_mission": "true"
    }

    # json dump & encode utf-8
    tmp_message = json.dumps(message_structure).encode('utf-8')
    request_message = request.Request(api_url, data=tmp_message) 
    resp = request.urlopen(request_message) # POST

    resp_json = eval(resp.read().decode('utf-8'))
    if "OK" == resp_json['status']:
        print("data requests successful!!")
    elif "ERROR" == resp_json['status']:    
        received_message=resp_json['msg']
        raise ValueError(received_message)  

```     
### 참가자 유의사항
올바르지 않은 답안 제출이 시도될 경우, 오류 사유(msg)와 함께 status 값은 ERROR를 반환합니다.    
ex)    
```
    {
        "status": "ERROR",
        "msg": "...."
    }
```

ERROR 메시지(msg)의 예는 다음과 같습니다.
- json 포맷이 아닌 다른 형식(혹은 잘못된 형식)의 답안을 제출 했을 때 ("Please check answer format (key-value).")
- 챌린저의 id 값이 올바르지 않을 때 ("id is invalid. Please check your id filed.")
- 챌린저의 hash 값이 올바르지 않을 때 ("Hash value is invalid")


1. 답안 제출 응답 관련
위 예제 코드와 같이 답안 제출 시, 참가자는 답안 제출 요청에 대한 응답으로 status와 해당하는 message를 수신 하여 정상 제출/오류를  판단하는 내용을 작성해야 합니다.     
status가 'OK'일 경우 별도의 message를 return하지 않으며, `ERROR`의 message를 수신후 해당내용을 Error에 출력결과로 지정해야 추론 오류를 확인할 수 있습니다.    
참가자분들께서는 제출 상태 판별 및 `ERROR`상태의 message를 raise하고자 하는 ERROR의 메세지로 출력 하도록 작성해주시기 바랍니다.

<span style="color: red">※ 단, 위 과정은 1회의 추론 횟수가 소모되는 것으로 참가팀 환경에서 충분히 테스트 후 평가 플랫폼에서 진행해 주세요.</span>    

2. 도커 이미지 실행 및 오류 메시지 확인 관련    
참가자가 제출한 도커 이미지는 평가 플랫폼 내의 데이터 셋 마운트, 답안 제출 환경 변수 추가 등 진행에 필요한 내용 추가를 제외하고 그대로 실행됩니다.    
추론 오류 시 확인하실 수 있는 오류 메시지는 실제 코드가 수행 된 이후 발생한 오류 메시지만 확인 가능하며, 참가자가 직접 작성한 쉘 스크립트 수행 과정 등 코드 외 오류들은 확인이 어렵습니다. 이 또한 참가팀 환경에서 충분히 테스트 후 평가 플랫폼에서 진행 부탁드립니다.    

3. end of mission 메세지 미제출 관련    
**답안지를 모두 보낸 후에는 반드시 'end of mission' 메세지를 POST 해야합니다. 해당 메세지가 제출되지 않을 경우, 답안이 제출되었어도, 추론 종료 후 채점이 진행되지 않습니다. 이 점 유의 부탁드립니다.**

4. 추론진행 중, 임시 쓰기 경로 확인
본 대회는 추론진행 과정중 임시로 최대 15GB의 쓰기가 가능한 디렉토리(**`/home/agc/tmp`**)를 제공합니다.   
모델 추론과정에서 쓰기 작업은 해당 폴더에서만 가능하며, 다른 폴더에는 쓰기권한이 부여되지 않습니다. 
------------
               
## 3. 도커 이미지 빌드 & 이미지 추출        
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

### 이미지 빌드 및 저장 예시
```
docker build -f dockerfile_submit -t user:1.0

docker save -o user.tar user:1.0
```
- 도커 빌드 및 이미지 저장과정에서 **참가자ID.tar** 파일 및 **도커 이미지 이름**과 **태그이름**에서 특수문자를 제외하고 저장해주시기 바랍니다.

-------------------------
## 4. 제출 안내 사항

**  참가팀은 추론진행 중, 임시 쓰기(write)가 가능한 아래 경로를 제공합니다. (15GB 제한)
```bsh    
/home/agc/tmp
```
- 해당 경로 내 파일은 추론완료 시 모두 삭제됩니다. 이점 유의해서 작업해주시기 바랍니다.

**  파일 업로드시 참가팀은 '자동 추론 시작' 옵션을 이용할 수 있습니다.
- 자동 추론 시작은 파일 검증이 완료되면, 자동으로 추론을 요청하는 기능입니다. (크레딧 1 소모)
- 제출 파일 오류 등으로 파일 검증이 완료되지 않는다면, 자동 추론 시작은 진행되지 않습니다. (크레딧 소모 X)
- 자동 추론 시작 기능은 파일 업로드 전 선택하며, 업로드 완료 이후에는 변경할 수 없습니다.
