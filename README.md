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
│       └── main.py    
```     
     
- 작업된 소스코드는 `/src`에 넣어 빌드를 진행해 주세요. (본 예시에서는 학습한 모델이 저장된 폴더를 my_model로 작성하였습니다.)    

- 참가자분들꼐서는 [**참가자 유의사항**](#참가자-유의사항)을 꼭 확인해주시기 바랍니다.

- 신규 대회 관련 공지는 [**신규 대회 공지사항**](#신규-대회-관련-공지)을 참고해주시기 바랍니다.    

--------------------------------------------------------    
    
본 가이드 페이지에서 제공하는 도커 이미지 빌드를 위한 과정은 다음 3가지로 분류 됩니다.      
- [**1. 제출 파일**](#1-제출-파일도커-이미지-생성)
- [**2. 추론코드 작성**](#2-추론코드-작성)
- [**3. 도커 이미지 빌드 & 이미지 추출**](#3-도커-이미지-빌드--이미지-추출)

## 1. 제출 파일(도커 이미지) 생성   
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

RUN mkdir -p ${HOME}/agc2022/dataset

WORKDIR ${HOME}/agc2022 # 컨테이너 work dir 정의

COPY ./src . # src 폴더의 소스코드를 도커 컨테이너로 복사

CMD ["python3","main.py"] # 실행할 main.py 코드.
```    

- 본 예시는 /src 폴더와 Dockerfile이 동일한 디렉토리에 있는 경우의 빌드과정을 나타냅니다.    
- 소스코드가 저장된 디렉토리 이름이 ```/src```가 아닐 경우 ```dockerfile```에서 복사할 폴더이름과 해당폴더 이름을 동일하게 맞춰주면 됩니다.     
- 마지막 CMD 명령어에는 실행될 python 파일명이 포함되어야 합니다. 그렇지 않을 경우, 평가 플랫폼에서의 구동이 제한됩니다.         
- public pytorch image를 사용할 경우 도커파일 내부 이미지 선언부 하단에 'RUN apt-get update'를 추가해야 timezone 관련 설정이 정상적으로 작동합니다.     
    
----------    
    
## 2. 추론코드 작성    
     
 추론코드 작성시에는 몇가지 유의사항이 존재합니다.     
      
> - 환경변수 단위의 API URL을 입력받기 위한 os package 사용, Request를 위한 urllib 패키지 사용        
> - API 결과값 json dump 및 model inference 결과값 request 과정        
> - 최종 제출 상태를 의미하는 'end of mission' message POST
      
환경변수 설정은 실행될 source code main.py 상단부에 작성해야합니다. 해당 예시는 [dev/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/dev/src/main.py), [framework/tf/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/framework/tf/src/main.py), [framework/torch/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/framework/torch/src/main.py)에서 확인할 수 있습니다. 또한, data_path는 `'/home/agc2022/dataset'` 으로 작성합니다.    
    
- python 환경변수 로드 예시     
```python    
    # load environment variable
    url = os.environ['REST_ANSWER_URL']    
    data_path = '/home/agc2022/dataset'     
 ```     
- REST API 수신 주소는 추론코드가 구동되는 평가 플랫폼에 환경 변수('REST_ANSWER_URL')로 정의되어 있습니다.     
    
추론 과정에서 답안 제출은 REST API를 활용하여 온라인 평가 플랫폼에 전송합니다. 제출은 batch 단위로 진행해야하며, 세부문제정의서에서 언급한 메시지 구조를 따라야합니다. 다음 예시는 유형별 답안제출 예시 json 입니다. 유형별 제출 방식에 차이가 존재하므로 참가자분들께서는 참고하시기 바랍니다. (상세 메시지 구조 등은 세부문제정의서 참조)     
- **batch단위 답안 제출 예시**
```json
# 유형 1 답안 제출 예시:
{
   "team_id": "userxx",
   "hash": "!@#$%^&*()",
   "problem_no": "001",
   "task_no": "1",
   "answer": []
}

# 유형 2 답안 제출 예시:
{
   "team_id": "userxx",
   "hash": "!@#$%^&*()",
   "problem_no": "002",
   "task_no": "2",
   "answer": []
}

# 유형 3 답안 제출 예시:
{
   "team_id": "userxx",
   "hash": "!@#$%^&*()",
   "problem_no": "003",
   "task_no": "3",
   "answer": ""
}

# 유형 4 답안 제출 예시:
{
   "team_id": "userxx",
   "hash": "!@#$%^&*()",
   "problem_no": "004",
    "task_no": "4",
    "answer": "",
    "evidence": []
}
```    
API POST 과정에는 두가지 유의사항이 존재합니다.     
>- json dump 과정에서 'utf-8'로 encoding 형식을 지정합니다.      
>- REST API로의 답안 제출 후, 응답 메시지를 확인할 수 있으며 이 또한 utf8로 디코딩하여 메시지를 확인하실 수 있습니다.       
         
        

end of mission은 채점서버에 답안지 제출이 끝남을 알리는 message입니다. 이에 따라 'problem_no', 'task_no'를 포함하지 않습니다.         


    

'end of mission' POST 형식은 다음과 같습니다.    

```json
    {
    "team_id": "userxx",
    "hash": "!@#$%^&*()",
    "end_of_mission": "true"
    }
```     
         
하단의 예시는 tensorflow기반 MNIST inference 예제 입니다. 본 예시에서는 batch를 1로 설정하여 이미지당 답안을 POST하도록 작성했습니다. 관련 내용은 [framework/tf/src/main.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/framework/tf/src/main.py), [framework/torch/src/inference.py](https://github.com/agc2022-new/agc-submit-guide/blob/main/framework/torch/src/inference.py)에서 확인할 수 있습니다.    

- 결과값 POST 예시
``` python    
    # model load & predict
    model = tf.keras.models.load_model("./my_model")
    
    for batch,data in enumerate(inference_loader):        
        # define answer template per batch
        template = {
            "team_id": "userxx",
            "hash": "!@#$%^&*()",
            "problem_no": "001",
            "task_no": "1",
            "answer": {}
        }
                
        # get inference result 
        output = model(data)
        
        # extract label from inference output
        batch_label = [int(np.argmax(sample)) for sample in output]
        tmp_answer = {"no":str(batch+1), "answer" : str(batch_label[0])}
        template['answer'] = tmp_answer
        
        # apply utf-8 to str json data
        data = json.dumps(template).encode('utf-8')

        # request ready
        req =  request.Request(api_url, data=data)
        
        # POST to API server
        resp = request.urlopen(req)
        
        # check POST result
        resp_json = eval(resp.read().decode('utf8'))
        print("received message: "+resp_json['msg'])

        if "OK" == resp_json['status']:
            print("data requests successful!!")
        elif "ERROR" == resp_json['status']:    
            raise ValueError("Receive ERROR status. Please check your source code.")    
    
    # request end of mission message
    message_structure = {
    "team_id": "userxx",
    "hash": "!@#$%^&*()",
    "end_of_mission": "true"
    }

    # json dump & encode utf-8
    tmp_message = json.dumps(message_structure).encode('utf-8')
    request_message = request.Request(api_url, data=tmp_message) 
    resp = request.urlopen(request_message) # POST

    resp_json = eval(resp.read().decode('utf-8'))
    print("received message: "+resp_json['msg'])

    if "OK" == resp_json['status']:
        print("data requests successful!!")
    elif "ERROR" == resp_json['status']:    
        raise ValueError("Receive ERROR status. Please check your source code.") 

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


제출파일에서 다음과 같은 사항에서 오류가 발생할 수 있습니다.
- json 형식이 올바르지 않은 경우
- team_id 및 secret이 올바르지 않은 경우
- json 내 key-value가 올바르지 않은 경우


1. 답안 제출 응답 관련
위 예제 코드와 같이 답안 제출 시, 참가자는 답안 제출 요청에 대한 응답으로 'ERROR'를 수신 하여 오류를 발생 시킴으로 평가 플랫폼에서 오류 메시지(답안 제출 상태)를 확인할 수 있습니다.     

<span style="color: red">※ 단, 위 과정은 1회의 추론 횟수가 소모되는 것으로 참가팀 환경에서 충분히 테스트 후 평가 플랫폼에서 진행해 주세요.</span>    


2. 도커 이미지 실행 및 오류 메시지 확인 관련    
참가자가 제출한 도커 이미지는 평가 플랫폼 내의 데이터 셋 마운트, 답안 제출 환경 변수 추가 등 진행에 필요한 내용 추가를 제외하고 그대로 실행됩니다.    
추론 오류 시 확인하실 수 있는 오류 메시지는 실제 코드가 수행 된 이후 발생한 오류 메시지만 확인 가능하며, 참가자가 직접 작성한 쉘 스크립트 수행 과정 등 코드 외 오류들은 확인이 어렵습니다. 이 또한 참가팀 환경에서 충분히 테스트 후 평가 플랫폼에서 진행 부탁드립니다.    

3. end of mission 메세지 미제출 관련    
**답안지를 모두 보낸 후에는 반드시 'end of mission' 메세지를 POST 해야합니다. 해당 메세지가 제출되지 않을 경우 추론이 정상적으로 이뤄지지 않습니다. 이 점 유의 부탁드립니다.**
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

-------------------------
## 신규 대회 공지사항

신규 대회에서는 두 가지 부분에 대한 변경점이 존재합니다.
1. 답안지 template
2. end of mission template
    
### 기존의 답안지 template에 대한 변경점    
     
기존 답안지 템플릿에서 몇 가지 변경점이 존재합니다. 변경점은 다음과 같습니다.    
1. 'secret' -> 'hash' key 값 수정     
2. 'problem_no', 'task_no' key 추가 (문제지 제공)    
3. 유형별 답안 템플릿 변경    

- 기존 답안 템플릿
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

- 변경 답안 템플릿
```json
# case1
{
   "team_id": "userxx",
   "hash": "!@#$%^&*()",
   "problem_no": "001",
   "task_no": "1",
   "answer": []
}

# case2
{
   "team_id": "userxx",
   "hash": "!@#$%^&*()",
   "problem_no": "002",
   "task_no": "2",
   "answer": []
}

# case3
{
   "team_id": "userxx",
   "hash": "!@#$%^&*()",
   "problem_no": "003",
   "task_no": "3",
   "answer": ""
}

# case4
{
   "team_id": "userxx",
   "hash": "!@#$%^&*()",
   "problem_no": "004",
    "task_no": "4",
    "answer": "",
    "evidence": []
}
```    
    
 > 'problem_no', 'task_no'의 경우 신규 대회에서 제공하는 문제지에 해당 key에 맞는 value를 기입해주시면 됩니다.    
 > 'problem_no'의 경우 3자리 숫자로 구성된 string이며, 'task_no'의 경우 문제지에 반영된 숫자를 기입하시면 됩니다.        
 > 유형별로 'answer'의 스키마에 대한 차이가 존재합니다. 스키마는 다음과 같습니다.    
 1. 유형 1 : list     
 2. 유형 2 : list     
 3. 유형 3 : string     
 4. 유형 4 : string     
 > 유형 4의 evidence는 세부문제 정의서에 정의된 부분이 추가되었습니다. 이 점 참고하시기 바랍니다.    

 ### end of mission 템플릿 key 값 변경점    
     
기존 end of mission 템플릿에서 'secret' key 값이 'hash'로 변경되었습니다.     변경된 template을 참고하여 제출해주시기 바랍니다.    
     

 - 기존 end of mission 템플릿
```json
{
    "team_id": "userxx",
    "secret": "!@#$%^&*()",
    "end_of_mission": "true"
}
```

 - 변경 end of mission 템플릿
```json
{
    "team_id": "userxx",
    "hash": "!@#$%^&*()",
    "end_of_mission": "true"
}
```

 