import os
import json
import subprocess
import sys
import time
import webbrowser
import gradio as gr
import torch
from text.symbols import cleaner_symbols
from transcript import run_whisper, run_whisper_tqdm


class Config:
    def __init__(self, speaker=None, eval_interval="1000", epoch="10000", batch="16", train=None, val=None,
                 cleaners=None, sampling="22050", n_speaker="0", name=None):
        self.speaker = speaker
        self.eval_interval = eval_interval
        self.epoch = epoch
        self.batch = batch
        self.train = train
        self.val = val
        self.cleaners = cleaners
        self.sampling = sampling
        self.n_speaker = n_speaker
        self.name = name


python = sys.executable


def language_cleaner(speaker, lang):
    if speaker == 'Single':
        my_config.speaker = '1'
    elif speaker == 'Multi':
        my_config.speaker = '2'
    if lang == 'ko':
        my_config.cleaners = "korean_cleaners"
    elif lang == 'ja':
        my_config.cleaners = "japanese_cleaners2"


# 대본 추출 버튼을 누르면 transcript에서 대본 작성을 진행합니다.
def run_write_script(speaker, lang, tqdm_bool):
    print(f"{speaker}, {lang}")
    if speaker is None or lang is None:
        print("Speaker 또는 lang을 선택해주세요.")
        return "Speaker 또는 lang을 선택해주세요."
    try:
        command = f'start cmd /c {python} transcript.py --speaker {speaker} --language {lang} --tqdm {tqdm_bool}'
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            print("대본 작성 완료!")
            return "대본 작성 완료!"
        else:
            print("외부 명령 실행 중 오류가 발생했습니다.", result.returncode)
            return f"외부 명령 실행 중 오류가 발생했습니다. {result.returncode}"

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


# Preprocess 실행 버튼을 누르면 random_pick을 이용하여
# filelists.txt 파일을 filelist_train.txt와 filelist_val.txt로 나눕니다.
# 이후 preprocess.py를 이용하여 각 train파일과 val파일을 전처리 해줍니다.
def run_preprocess(speaker, lang, rand, filelist_path):
    if speaker is None or lang is None:
        return "Speaker 또는 lang을 선택해주세요."
    if rand:
        result = subprocess.run(
            [python, "random_pick.py", "--filelist", filelist_path],
            stdout=sys.stdout,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
        )
        if result.stderr:
            print(result.stderr)
            return f"Error: {result.stderr}"

        print("random_pick을 성공적으로 완료했습니다.!")

        filelists_train = os.path.join(os.path.dirname(filelist_path), "filelist_train.txt")
        filelists_val = os.path.join(os.path.dirname(filelist_path), "filelist_val.txt")

    language_cleaner(speaker, lang)
    if my_config.speaker == 1:
        my_config.n_speaker = 0
    result = subprocess.run(
        [python, "preprocess.py", "--text_index", my_config.speaker, "--filelists", filelists_train, filelists_val,
         "--text_cleaners", my_config.cleaners],
        stdout=sys.stdout,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
    )
    my_config.train = "".join(filelists_train.split(".")[:-1]) + "_cleaned." + filelists_train.split(".")[-1]
    my_config.val = "".join(filelists_val.split(".")[:-1]) + "_cleaned." + filelists_val.split(".")[-1]
    print("Preprocess을 성공적으로 완료되었습니다!")
    return "random_pick을 성공적으로 완료했습니다!\nPreprocess을 성공적으로 완료되었습니다!"


# 새로 고침을 누르면 my_config에 있던 값들을 반환합니다.
def run_config_json():
    return (
        my_config.eval_interval,
        my_config.epoch,
        my_config.batch,
        my_config.train,
        my_config.val,
        my_config.cleaners,
        my_config.sampling,
        my_config.n_speaker
    )


# example/configs/config.json를 불러온 뒤 아래의 값을 수정하고 filelists/config.json으로 저장합니다.
def run_create_config(interval, epoch, batch, train, val, cleaners, sampling, n_speaker, names):
    with open('example/configs/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    config["train"]["eval_interval"] = int(interval)
    config["train"]["epochs"] = int(epoch)
    config["train"]["batch_size"] = int(batch)
    config["data"]["training_files"] = train
    config["data"]["validation_files"] = val
    config["data"]["text_cleaners"] = [cleaners]
    config["data"]["sampling_rate"] = int(sampling)
    config["data"]["n_speakers"] = int(n_speaker)
    config["speakers"] = [name.strip() for name in names.split(',')]

    choice_symbols = cleaner_symbols[cleaners]
    symbols = [choice_symbols['_pad']] + list(choice_symbols['_punctuation']) + list(choice_symbols['_letters'])

    config["symbols"] = symbols

    with open('filelists/config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=True, indent=2)
    return "filelists/config.json 이 생성되었습니다."


# text/symbols.py의 symbols를 사용자의 데이터에 맞게 변경하기 위해 setting.json이라는 파일을 사용하고 있습니다.
# filelists/config.json 파일의 text_cleaners 값을 읽은 뒤 setting.json 파일의 text_cleaners 값에 저장합니다.
# text/symbols.py 에서는 setting.json 의 text_cleaners 값을 읽어 symbols를 만듭니다.
def text_cleaners_change(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    cleaners = config['data']["text_cleaners"][0]
    with open('setting.json', 'r') as f:
        setting = json.load(f)
    setting['text_cleaners'] = [cleaners]
    with open('setting.json', 'w') as f:
        json.dump(setting, f, ensure_ascii=True, indent=2)


# 학습 실행 버튼을 누르면 실행되는 함수입니다.
def run_train(speaker, config_path, model_path):
    text_cleaners_change(config_path)
    if speaker == 'Single':
        command = f'start cmd /k {python} train.py -c {config_path} -m {model_path}'
        subprocess.run(command, shell=True)
        return ("단일 화자 학습이 시작되었습니다.\n"
                "학습은 자동으로 종료되지 않습니다.\n"
                "원하는 Step에서 Ctrl + C 를 눌러 학습을 종료할 수 있습니다.\n"
                "학습은 eval interval 마다 모델을 저장합니다.")
    else:
        command = f'start cmd /k {python} train_ms.py -c {config_path} -m {model_path}'
        subprocess.run(command, shell=True)
        return ("다중 화자 학습이 시작되었습니다.\n"
                "학습은 자동으로 종료되지 않습니다\n."
                "원하는 Step에서 Ctrl + C 를 눌러 종료할 수 있습니다.\n"
                "학습은 eval interval 마다 모델을 저장합니다.")


# Tensorboard 실행을 누르면 동작하는 함수입니다.
def run_tensorboard(model_path):
    if os.path.isdir(model_path):
        command = rf'start cmd /k venv\scripts\tensorboard.exe --logdir="{model_path}" --host 0.0.0.0 --port 6006'
        subprocess.run(command, shell=True)
        time.sleep(2)
        webbrowser.open("http://localhost:6006/")
        return "텐서보드가 실행되었습니다."
    else:
        return "모델의 경로가 잘못되었습니다."


# 추론 Webui 실행을 누르면 동작하는 함수입니다.
def run_infer_server(config_path, model_path):
    text_cleaners_change(config_path)
    command = rf'start cmd /k {python} server.py --config_path {config_path} --model_path {model_path}'
    subprocess.run(command, shell=True)
    time.sleep(2)
    webbrowser.open("http://localhost:7870/")


# 아래는 Gardio를 사용한 Webui 코드입니다.
with gr.Blocks(title="VITS-WebUI") as app:
    with gr.Tab("학습"):
        gr.Markdown(f'## 현재 사용자의 torch.cuda.is_available() == {torch.cuda.is_available()}\n'
                    f'- torch.cuda.is_available()이 True라면 그래픽카드를 사용할 수 있음\n'
                    f'- torch.cuda.is_available()이 Flase라면 그래픽카드를 사용할 수 없음')
        with gr.Column(scale=1):
            gr.Markdown(
                """
                ## Step 1: Faster-Whisper를 이용하여 음성 파일들의 대본를 작성합니다.
                - 단일 화자라면 filelists/SP 폴더 안에 음성 파일을 넣어주세요.
                - 다중 화자라면 filelists/MP 폴더 안에 각 화자별로 폴더를 나누어 넣어주세요.
                """
            )
            with gr.Row():
                speaker_choice = gr.Radio(
                    choices=["Single", "Multi"],
                    label="화자 선택",
                    value="Single",
                    interactive=True,
                    info="화자가 한 명인 경우 Single, 화자가 여러명이라면 Multi를 선택해주세요."
                )
                language_choice = gr.Radio(
                    choices=["ko", "ja"],
                    label="언어 선택",
                    value="ko",
                    interactive=True,
                    info="어떤 언어로 대본을 작성할 것인지 선택해주세요."
                )
                tqdm_choice = gr.Checkbox(
                    label="작업시간만 출력",
                    value=True,
                    info="tqdm 라이브러리를 사용하여 작업 종료 시간을 보여줍니다.\n선택하면 번역된 문장들은 보이지 않습니다."
                )
            with gr.Row():
                speaker_button = gr.Button(value="대본 추출", variant="primary")
                speaker_output = gr.Textbox(label="결과창")
            speaker_button.click(
                fn=run_write_script,
                inputs=[speaker_choice, language_choice, tqdm_choice],
                outputs=[speaker_output]
            )

        with gr.Column(scale=1):
            gr.Markdown(
                """
                ## Step 2: Preprocess
                """
            )
            with gr.Row():
                preprocess_speaker_choice = gr.Radio(
                    choices=["Single", "Multi"],
                    label="화자 선택",
                    value="Single",
                    interactive=True,
                    info="화자가 한 명인 경우 Single, 화자가 여러명이라면 Multi를 선택해주세요."
                )
                preprocess_language_choice = gr.Radio(
                    choices=["ko", "ja"],
                    label="언어 선택",
                    value="ko",
                    interactive=True,
                    info="어떤 언어로 대본을 전처리할 것인지 선택해주세요."
                )
                preprocess_filelist = gr.Textbox(
                    label="filelists.txt 경로",
                    value="filelists/filelists.txt",
                    info = "filelists.txt의 경로를 작성해주세요.",
                    interactive=True
                )
                preprocess_checkbox = gr.Checkbox(
                    label="random_pick 실행",
                    value=True,
                    info="대본를 train.txt와 val.txt로 나누어 주는 과정입니다."
                )
            with gr.Row():
                preprocess_button = gr.Button(value="Preprocess 실행", variant="primary")
                preprocess_textbox = gr.Textbox(label="결과창")
                preprocess_button.click(
                    fn=run_preprocess,
                    inputs=[preprocess_speaker_choice, preprocess_language_choice, preprocess_checkbox, preprocess_filelist],
                    outputs=[preprocess_textbox]
                )

        with gr.Column(scale=1):
            gr.Markdown(
                """
                ## Step 3: config.json 작성
                """
            )
            with gr.Column():
                refresh_button = gr.Button(value="새로 고침", variant="primary")
                config_eval_interval = gr.Textbox(
                    label="eval_interval",
                    value="1000",
                    interactive=True,
                    info="학습을 진행할 때 몇 step 마다 저장할 것인지에 설정하는 값"
                )
                config_epochs = gr.Textbox(
                    label="epochs",
                    value="10000",
                    interactive=True,
                    info="전체 데이터셋을 몇 번 반복하여 학습할 것인지 설정하는 값"
                )
                config_batch_size = gr.Textbox(
                    label="batch_size",
                    value="16",
                    interactive=True,
                    info="뭐라 설명할지 모르겠네"
                )
                config_training_files = gr.Textbox(
                    label="training_files",
                    value="filelists/filelist_train_cleaned.txt",
                    interactive=True,
                    info="filelists_train.txt.cleaned 파일의 경로"
                )
                config_validation_files = gr.Textbox(
                    label="validation_files",
                    value="filelists/filelist_val_cleaned.txt",
                    interactive=True,
                    info="filelists_val.txt.cleaned 파일의 경로"
                )
                config_text_cleaners = gr.Textbox(
                    label="text_cleaners",
                    interactive=True,
                    info="어떤 언어를 사용하여 학습할 것인지 설정하는 값"
                )
                config_sampling_rate = gr.Dropdown(
                    label="sampling_rate",
                    choices=["22050", "44100"],
                    value="22050",
                    interactive=True,
                    info="학습할 오디오들의 sampling rate를 설정하는 값"
                )
                config_n_speakers = gr.Textbox(
                    label="n_speakers",
                    value="0",
                    interactive=True,
                    info="학습할 화자의 수를 설정하는 값"
                )
                config_speakers_name = gr.Textbox(
                    label="speakers_name",
                    interactive=True,
                    info="학습하는 화자의 이름을 설정하는 값"
                )
                with gr.Row():
                    config_button = gr.Button(value="Create config.json", variant="primary")
                    config_result = gr.Textbox(label="결과창")
                refresh_button.click(
                    fn=run_config_json,
                    outputs=[
                        config_eval_interval,
                        config_epochs,
                        config_batch_size,
                        config_training_files,
                        config_validation_files,
                        config_text_cleaners,
                        config_sampling_rate,
                        config_n_speakers
                    ]
                )
                config_button.click(
                    fn=run_create_config,
                    inputs=[
                        config_eval_interval,
                        config_epochs,
                        config_batch_size,
                        config_training_files,
                        config_validation_files,
                        config_text_cleaners,
                        config_sampling_rate,
                        config_n_speakers,
                        config_speakers_name
                    ],
                    outputs=[config_result]
                )

        with gr.Column(scale=1):
            gr.Markdown(
                """
                ## Step 4: VITS 학습
                """
            )
            with gr.Column():
                with gr.Row():
                    train_speakers = gr.Radio(
                        choices=["Single", "Multi"],
                        label="화자 선택",
                        value="Single",
                        interactive=True
                    )
                    train_config_path = gr.Textbox(
                        label="config.json 경로",
                        value="filelists/config.json",
                        interactive=True
                    )
                    train_model_path = gr.Textbox(
                        label="모델 이름",
                        value="model",
                        interactive=True,
                        info="model로 입력한 경우 checkpoints/model 폴더에 저장됩니다."
                    )
                with gr.Row():
                    train_button = gr.Button(value="학습 실행", variant="primary")
                    train_textbox = gr.Textbox(label="결과창")
                    train_button.click(
                        fn=run_train,
                        inputs=[train_speakers, train_config_path, train_model_path],
                        outputs=[train_textbox]
                    )
        with gr.Column(scale=1):
            gr.Markdown(
                """
                ## Step 5: Tensorboard 실행하기
                """
            )
            with gr.Row():
                folder_path = gr.Textbox(
                    label="모델 경로",
                    value="checkpoints/model",
                    info="모델을 저장한 경로를 입력해주세요."
                )
                tensorboard_on_button = gr.Button(
                    value="Tensorboard 실행",
                    variant="primary"
                )
            tensorboard_result = gr.Textbox(label="결과창")
            tensorboard_on_button.click(
                fn=run_tensorboard,
                inputs=[folder_path],
                outputs=[tensorboard_result]
            )
        with gr.Column(scale=1):
            gr.Markdown(
                """
                ## Step 6: VITS 추론
                """
            )
            with gr.Row():
                infer_config_path = gr.Textbox(
                    label="config.json 경로",
                    value="checkpoints/model/config.json",
                    info="config.json 경로를 입력해주세요."
                )
                infer_model_path = gr.Textbox(
                    label="모델 경로",
                    value="checkpoints/model/G_*.pth",
                    info="G_*.pth의 경로를 입력해주세요."
                )
                infer_on_button = gr.Button(
                    value="추론 Webui 실행",
                    variant="primary"
                )
                infer_on_button.click(
                    fn=run_infer_server,
                    inputs=[infer_config_path, infer_model_path]
                )
        gr.Markdown(
            "Source Reference \n\n"
            "- [https://github.com/ouor/vits](https://github.com/ouor/vits)\n\n"
            "- [https://github.com/litagin02/vits-japros-webui](https://github.com/litagin02/vits-japros-webui)\n\n"
            "- [https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)\n\n"
        )

if __name__ == "__main__":
    my_config = Config()
    # filelists/SP와 filelists/MP 중 하나라도 없는 경우 폴더를 만듭니다.
    if not os.path.isdir("filelists/SP") or not os.path.isdir("filelists/MP"):
        os.makedirs("filelists/SP", exist_ok=True)
        os.makedirs("filelists/MP", exist_ok=True)
    webbrowser.open("http://localhost:7860")
    app.launch()
