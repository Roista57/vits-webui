# VITS
## 레포지토리 가져오기
```
git clone https://github.com/Roista57/VITS.git
```
## 모듈 설치

## 파일들
##### python3.8: https://www.python.org/downloads/release/python-3810/
##### cmake: https://cmake.org/download/
##### visual studio build tools: https://visualstudio.microsoft.com/ko/vs/older-downloads/
##### Cuda Toolkit: https://developer.nvidia.com/cuda-toolkit-archive
##### cuDNN: https://developer.nvidia.com/rdp/cudnn-archive

```
pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cu117
pip install -r requirements.txt
pip install -U pyopenjtalk==0.2.0 --no-build-isolation
```
## monotonic_align 설치
```
cd monotonic_align
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
```
## filelists.txt를 훈련셋과 검증셋으로 나누기
```
python random_pick.py --filelist filelists.txt
```
## 훈련셋과 검증셋을 전처리
### 싱글 스피커
```
python preprocess.py --text_index 1 --filelists filelist_train.txt filelist_val.txt --text_cleaners korean_cleaners
```
### 멀티 스피커
```
python preprocess.py --text_index 2 --filelists filelist_train.txt filelist_val.txt --text_cleaners korean_cleaners
```
## 학습
### 싱글 스피커 학습
checkpoints는 폴더 명
```
python train.py -c config.json -m checkpoints
```
### 멀티 스피커 학습
```
python train_ms.py -c config.json -m checkpoints
```

# Runpod VITS
```
git clone https://github.com/Roista57/VITS.git
cd VITS
pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cu117
pip install -r requirements.txt
pip install -U pyopenjtalk==0.2.0 --no-build-isolation

cd monotonic_align
rm -rf ./monotonic_align
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..

```
