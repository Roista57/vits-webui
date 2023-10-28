import faster_whisper
from faster_whisper import WhisperModel
import os
import torch
import argparse
from tqdm import tqdm
import sys


# faster_whisper를 사용하여 음성 파일을 읽은 뒤 대사를 반환합니다.
def whisper_script(model, path, lang):
    segments, info = model.transcribe(path, language=lang, beam_size=5)
    text = ""
    for segment in segments:
        text += segment.text
    if text[0] == ' ':
        return text[1:]
    else:
        return text


# 추출된 대사를 보여주지만 예측하는 작업 종료시간을 보여주지 않습니다.
def run_whisper(speaker, lang):
    model_size = "large-v2"
    if torch.cuda.is_available():
        # Run on GPU with FP16
        print('GPU 모델 사용')
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
    else:
        # or run on CPU with INT8
        print('CPU 모델 사용')
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

    transcript_path = "filelists/filelists.txt"

    if speaker == 'Single':
        print("단일 화자 대사 작업 시작")
        folder_path = "filelists/SP/"
        # 해당 폴더 내의 .wav 파일들의 경로 리스트 생성
        wav_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.wav')]
        # 결과 출력
        with open(transcript_path, "w", encoding="utf-8") as output:
            for wav in wav_files:
                text = whisper_script(model, wav, lang)
                print(f"{wav}|{text}")
                output.write(f"{wav}|{text}\n")

    elif speaker == 'Multi':
        print("다중 화자 대사 작업 시작")
        base_path = "filelists/MP/"
        speakers = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        with open(transcript_path, "w", encoding="utf-8") as output:
            for idx, speaker in enumerate(speakers):
                speaker_path = os.path.join(base_path, speaker)
                subdirs = [d for d in os.listdir(speaker_path) if os.path.isdir(os.path.join(speaker_path, d))]

                # speaker 폴더 안에 하위 폴더가 없으면, 바로 wav 파일 리스트를 가져옴
                if not subdirs:
                    wav_files = [f for f in os.listdir(speaker_path) if f.endswith('.wav')]
                    for wav in wav_files:
                        full_wav_path = os.path.join(speaker_path, wav)
                        text = whisper_script(model, full_wav_path, lang)
                        print(f"{speaker_path}/{wav}|{idx}|{text}")
                        output.write(f"{speaker_path}/{wav}|{idx}|{text}\n")

                # speaker 폴더 안에 하위 폴더가 있으면, 각 폴더마다 wav 파일 리스트를 가져옴
                else:
                    for subdir in subdirs:
                        subdir_path = os.path.join(speaker_path, subdir)
                        for root, dirs, files in os.walk(subdir_path):
                            # 현재 폴더가 하위 폴더를 가지고 있지 않은 경우 (즉, 가장 깊은 수준의 폴더)
                            if not dirs:
                                wav_files = [f for f in files if f.endswith('.wav')]
                                for wav in wav_files:
                                    full_wav_path = os.path.join(root, wav)
                                    text = whisper_script(model, full_wav_path, lang)  # whisper_script는 음성 파일을 처리하는 함수로 가정합니다.
                                    print(f"{root}/{wav}|{idx}|{text}")
                                    output.write(f"{root}/{wav}|{idx}|{text}\n")


# tqdm을 사용하여 작업 종료시간을 예측해주지만 추출된 대사를 보여주지 않습니다.
def run_whisper_tqdm(speaker, lang):
    model_size = "large-v2"
    if torch.cuda.is_available():
        # Run on GPU with FP16
        print('GPU 모델 사용')
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
    else:
        # or run on CPU with INT8
        print('CPU 모델 사용')
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

    transcript_path = "filelists/filelists.txt"

    if speaker == 'Single':
        print("단일 화자 대사 작업 시작")
        folder_path = "filelists/SP/"
        # 해당 폴더 내의 .wav 파일들의 경로 리스트 생성
        wav_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.wav')]
        # 결과 출력
        with open(transcript_path, "w", encoding="utf-8") as output:
            for wav in tqdm(wav_files):
                text = whisper_script(model, wav, lang)
                # print(f"{wav}|{text}")
                output.write(f"{wav}|{text}\n")

    elif speaker == 'Multi':
        print("다중 화자 대사 작업 시작")
        base_path = "filelists/MP/"
        speakers = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        print(f"files total: {len(speakers)}")
        with open(transcript_path, "w", encoding="utf-8") as output:
            for idx, speaker in enumerate(speakers):
                speaker_path = os.path.join(base_path, speaker)
                subdirs = [d for d in os.listdir(speaker_path) if os.path.isdir(os.path.join(speaker_path, d))]

                # speaker 폴더 안에 하위 폴더가 없으면, 바로 wav 파일 리스트를 가져옴
                if not subdirs:
                    wav_files = [f for f in os.listdir(speaker_path) if f.endswith('.wav')]
                    for wav in tqdm(wav_files, desc=speaker_path):
                        full_wav_path = os.path.join(speaker_path, wav)
                        text = whisper_script(model, full_wav_path, lang)
                        # print(f"{speaker_path}/{wav}|{idx}|{text}")
                        output.write(f"{speaker_path}/{wav}|{idx}|{text}\n")

                # speaker 폴더 안에 하위 폴더가 있으면, 각 폴더마다 wav 파일 리스트를 가져옴
                else:
                    for subdir in subdirs:
                        subdir_path = os.path.join(speaker_path, subdir)
                        for root, dirs, files in os.walk(subdir_path):
                            # 현재 폴더가 하위 폴더를 가지고 있지 않은 경우 (즉, 가장 깊은 수준의 폴더)
                            if not dirs:
                                wav_files = [f for f in files if f.endswith('.wav')]
                                for wav in tqdm(wav_files, desc=subdir_path):
                                    full_wav_path = os.path.join(root, wav)
                                    text = whisper_script(model, full_wav_path, lang)  # whisper_script는 음성 파일을 처리하는 함수로 가정합니다.
                                    # print(f"{root}/{wav}|{idx}|{text}")
                                    output.write(f"{root}/{wav}|{idx}|{text}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--speaker", type=str)
    parser.add_argument("--language", type=str)
    parser.add_argument("--tqdm", type=str)

    args = parser.parse_args()

    speaker = args.speaker
    lang = args.language
    run_tqdm = args.tqdm

    if run_tqdm == 'True':
        run_whisper_tqdm(speaker, lang)
    else:
        run_whisper(speaker, lang)
