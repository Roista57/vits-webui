# 사용 방법

## 레포지토리 클론
```sh
git clone https://github.com/ouor/vits.git
```
## 텍스트 클리너 선택
- config.json 파일의 "text_cleaners"에 사용할 텍스트 클리너를 적어줍니다.
- 별도로 수정하지 않으면 'korean_cleaners'라는 한국어 텍스트 클리너를 사용합니다.
- 사용할 심볼도 수정해줍니다. [symbols.py](text/symbols.py)에서 수정할 수 있습니다.
## 가상환경을 만들고 활성화합니다.
```sh
python -m venv .venv
.\.venv\Scripts\activate
```

## 파이토치 설치
```sh
pip3 install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cu117
```

## 필요한 라이브러리 설치
```sh
pip install -r requirements.txt
```
설치 중 'subprocess exited with error' 같은 에러가 발생하면, [visual studio build tools](https://visualstudio.microsoft.com/downloads/?q=build+tools)를 설치하고 재부팅 후 다시 시도해보세요.

## monotonic alignment 라이브러리 설치
```sh
cd monotonic_align
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
```
역시 설치 중 'subprocess exited with error' 같은 에러가 발생하면, [visual studio build tools](https://visualstudio.microsoft.com/downloads/?q=build+tools)를 설치하고 재부팅 후 다시 시도해보세요.

## 데이터셋 준비

### 단일 화자
config.json 에서 'n_speakers'는 0으로 설정해줍니다.
- Example
```
dataset/001.wav|6월 17일의 기상예보입니다.
dataset/002.wav|오늘 날씨는 맑고 화창할 것으로 예상됩니다.
dataset/003.wav|낮 최고 기온은 25도, 새벽 최저 기온은 15도로 예상됩니다.
...
```
이와 같이 텍스트 파일을 만들어줍니다. 학습 데이터와 검증 데이터는 각각 'filelist_train.txt'와 'filelist_val.txt'처럼 다른 파일로 만들어줍니다.

### 다중 화자
config.json에서 'n_speakers'는 1 이상으로 설정해줍니다.\
config.json에서 'speakers'에 사용할 화자 이름을 리스트로 적어줍니다.

- Example
```
dataset/001.wav|0|6월 17일의 기상예보입니다.
dataset/002.wav|1|오늘 날씨는 맑고 화창할 것으로 예상됩니다.
dataset/003.wav|2|낮 최고 기온은 25도, 새벽 최저 기온은 15도로 예상됩니다.
...
```
역시 학습 데이터와 검증 데이터는 각각 'filelist_train.txt'와 'filelist_val.txt'처럼 다른 파일로 만들어줍니다.

## 텍스트 전처리
```sh
### 단일 화자
python preprocess.py --text_index 1 --filelists path/to/filelist_train.txt path/to/filelist_val.txt --text_cleaners 'korean_cleaners'

### 다중 화자
python preprocess.py --text_index 2 --filelists path/to/filelist_train.txt path/to/filelist_val.txt --text_cleaners 'korean_cleaners'
```
- 텍스트 전처리가 완료되면.. 
- config.json 파일의 'training_files'을 전처리한 학습 텍스트 파일의 경로로, 
- 'validation_files'을 전처리한 검증 텍스트 파일의 경로로, 
- 'cleaned_text'를 true로 수정해줍니다.

복잡하게 보이지만 [filelists](example/filelists), [configs](example/configs) 폴더의 전처리 결과를 참고하면 쉽게 이해할 수 있습니다.

## 학습 팁
- 빠른 학습을 위해 사전학습 모델을 사용할 수 있습니다. (사전학습 모델은 허깅페이스에서 찾을 수 있습니다.)
- 만약 그래픽카드의 vram이 24GB 미만이라면..
- 22,050Hz로 학습해도 결과가 좋습니다. 22,050Hz로 학습하는 것을 추천합니다.
- 각각의 데이터셋 오디오의 길이가 5초를 넘지 않도록 합니다.

## 학습 시작
```sh
### 단일 화자
python train.py -c <config> -m <folder>

### 다중 화자
python train_ms.py -c <config> -m <folder>
```
사전학습 모델을 사용하려면, 학습을 시작하기 전에 'G_0.pth'와 'D_0.pth'를 학습된 모델이 생성될 폴더에 미리 넣어줍니다.

### 학습 현황 확인
```sh
tensorboard --logdir checkpoints/<folder> --port 6006
```
## 추론
### 주피터 노트북
[infer.ipynb](infer.ipynb)
### Gradio WebUI
```sh
python server.py --config_path path/to/config.json --model_path path/to/model.pth
```