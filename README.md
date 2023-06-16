한국어 버전은 여기로 → [README-ko.md](README-ko.md)
# How to use
## Clone this repository
```sh
git clone https://github.com/ouor/vits.git
```
## Choose cleaners

- Fill "text_cleaners" in config.json
- Initialy "text_cleaners" is set to 'korean_cleaners'. To use alternative cleaners, revise with following step.
- Edit text/symbols.py
- Remove unnecessary imports from text/cleaners.py
## Create virtual environment
```sh
python -m venv .venv
.\.venv\Scripts\activate
```
## Install pytorch
```sh
pip3 install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cu117
```
## Install requirements
```sh
pip install -r requirements.txt
```
If error occurs while install requirements, Install [visual studio build tools](https://visualstudio.microsoft.com/downloads/?q=build+tools) and try again.
## Build monotonic alignment search
```sh
cd monotonic_align
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
```
## Create datasets
### Single speaker
"n_speakers" should be 0 in config.json
```
path/to/XXX.wav|transcript
```
- Example
```
dataset/001.wav|こんにちは。
```
### Mutiple speakers
Speaker id should start from 0 
```
path/to/XXX.wav|speaker id|transcript
```
- Example
```
dataset/001.wav|0|こんにちは。
```
## Preprocess
If you need random pick from full filelist..
```sh
python random_pick.py --filelist path/to/filelist.txt
```
```sh
# Single speaker
python preprocess.py --text_index 1 --filelists path/to/filelist_train.txt path/to/filelist_val.txt --text_cleaners 'korean_cleaners'

# Mutiple speakers
python preprocess.py --text_index 2 --filelists path/to/filelist_train.txt path/to/filelist_val.txt --text_cleaners 'korean_cleaners'
```
If you have done this, set "cleaned_text" to true in config.json
## Small Tips
- recommand to use pretrained model (you can get pretrained model from huggingface.co)
- If your vram is not enough (less than 40GB)
- do not train with 44100Hz. 22050Hz is good enough.
- make each dataset audio length short. (recommand to use maximum 4 seconds per audio)
## Train
```sh
# Single speaker
python train.py -c <config> -m <folder>

# Mutiple speakers
python train_ms.py -c <config> -m <folder>
```
If you want to train from pretrained model, Place 'G_0.pth' and 'D_0.pth' in destination folder before enter train command.
## Tensorboard
```sh
tensorboard --logdir checkpoints/<folder> --port 6006
```
## Inference
### Jupyter notebook
[infer.ipynb](infer.ipynb)
### Gradio web app
```sh
python server.py --config_path path/to/config.json --model_path path/to/model.pth
```

# Running in Docker

```sh
docker run -itd --gpus all --name "Container name" -e NVIDIA_DRIVER_CAPABILITIES=compute,utility -e NVIDIA_VISIBLE_DEVICES=all "Image name"
```

