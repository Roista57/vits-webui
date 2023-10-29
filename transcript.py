import faster_whisper
from faster_whisper import WhisperModel
import os
import torch
import argparse
from tqdm import tqdm
import sys
from pydub import AudioSegment


def resample_directory(wav_files, root, speaker_info, target_sample_rate=22050):
    if speaker_info == 'Single':
        replace_dir = ["audio_file/SP/", "filelists/SP/"]
    else:
        replace_dir = ["audio_file/MP/", "filelists/MP/"]
    os.makedirs(root.replace(replace_dir[0], replace_dir[1]), exist_ok=True)
    for wav in tqdm(wav_files, desc=f"resample ==> {root}"):
        full_wav_path = os.path.join(root, wav)
        output_path = full_wav_path.replace(replace_dir[0], replace_dir[1])
        audio = AudioSegment.from_wav(full_wav_path)
        resampled_audio = audio.set_frame_rate(target_sample_rate)
        resampled_audio.export(output_path, format="wav")


# faster_whisper를 사용하여 음성 파일을 읽은 뒤 대사를 반환합니다.
def whisper_script(model, path, lang):
    segments, info = model.transcribe(path, language=lang, beam_size=5)
    text = ""
    for segment in segments:
        text += segment.text
    if len(text) > 0 and text[0] == ' ':
        return text[1:]
    else:
        return text


def process_wav_files(model, files, base_path, output, lang, idx=None):
    for wav in files:
        full_wav_path = os.path.join(base_path, wav)
        text = whisper_script(model, full_wav_path, lang)  # 음성 파일을 처리하는 함수.
        print_line = f"{full_wav_path}|{text}" if idx is None else f"{full_wav_path}|{idx}|{text}"
        print(print_line)
        output.write(print_line + "\n")


def process_wav_files_tqdm(model, files, base_path, output, lang, idx=None):
    for wav in tqdm(files, desc=base_path):
        full_wav_path = os.path.join(base_path, wav)
        text = whisper_script(model, full_wav_path, lang)  # 음성 파일을 처리하는 함수.
        print_line = f"{full_wav_path}|{text}" if idx is None else f"{full_wav_path}|{idx}|{text}"
        output.write(print_line + "\n")


# 추출된 대사를 보여주지만 예측하는 작업 종료시간을 보여주지 않습니다.
def run_whisper(speaker, lang, target_sample):
    model_size = "large-v2"
    if torch.cuda.is_available():
        print('GPU 모델 사용')
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
    else:
        print('CPU 모델 사용')
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

    transcript_path = "filelists/filelists.txt"

    if speaker == 'Single':
        print("단일 화자 대사 작업 시작")
        replace_dir = ["audio_file/SP/", "filelists/SP/"]
        input_folder_path = replace_dir[0]
        output_folder_path = replace_dir[1]
        wav_files = [f for f in os.listdir(input_folder_path) if f.endswith('.wav')]
        with open(transcript_path, "w", encoding="utf-8") as output:
            resample_directory(wav_files, input_folder_path, speaker, target_sample)
            process_wav_files(model, wav_files, output_folder_path, output, lang)

    elif speaker == 'Multi':
        print("다중 화자 대사 작업 시작")
        replace_dir = ["audio_file/MP/", "filelists/MP/"]
        base_path = replace_dir[0]
        speakers = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        with open(transcript_path, "w", encoding="utf-8") as output:
            for idx, speaker in enumerate(speakers):
                speaker_path = os.path.join(base_path, speaker)
                for root, dirs, files in os.walk(speaker_path):
                    wav_files = [f for f in files if f.endswith('.wav')]
                    output_path = root.replace(replace_dir[0], replace_dir[1])
                    resample_directory(wav_files, root, speaker, target_sample)
                    process_wav_files(model, wav_files, output_path, output, lang, idx)


# tqdm을 사용하여 작업 종료시간을 예측해주지만 추출된 대사를 보여주지 않습니다.
def run_whisper_tqdm(speaker, lang, target_sample):
    model_size = "large-v2"
    if torch.cuda.is_available():
        print('GPU 모델 사용')
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
    else:
        print('CPU 모델 사용')
        model = WhisperModel(model_size, device="cpu", compute_type="int8")

    transcript_path = "filelists/filelists.txt"

    if speaker == 'Single':
        print("단일 화자 대사 작업 시작")
        replace_dir = ["audio_file/SP/", "filelists/SP/"]
        input_folder_path = replace_dir[0]
        output_folder_path = replace_dir[1]
        wav_files = [f for f in os.listdir(input_folder_path) if f.endswith('.wav')]
        with open(transcript_path, "w", encoding="utf-8") as output:
            resample_directory(wav_files, input_folder_path, speaker, target_sample)
            process_wav_files_tqdm(model, wav_files, output_folder_path, output, lang)

    elif speaker == 'Multi':
        print("다중 화자 대사 작업 시작")
        replace_dir = ["audio_file/MP/", "filelists/MP/"]
        base_path = replace_dir[0]
        speakers = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        with open(transcript_path, "w", encoding="utf-8") as output:
            for idx, speaker in enumerate(speakers):
                speaker_path = os.path.join(base_path, speaker)
                for root, dirs, files in os.walk(speaker_path):
                    wav_files = [f for f in files if f.endswith('.wav')]
                    output_path = root.replace(replace_dir[0], replace_dir[1])
                    resample_directory(wav_files, root, speaker, target_sample)
                    process_wav_files_tqdm(model, wav_files, output_path, output, lang, idx)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--speaker", type=str)
    parser.add_argument("--language", type=str)
    parser.add_argument("--samplerate", type=int)
    parser.add_argument("--tqdm", type=str)

    args = parser.parse_args()

    speaker = args.speaker
    lang = args.language
    sample_rate = args.samplerate
    run_tqdm = args.tqdm

    if run_tqdm == 'True':
        run_whisper_tqdm(speaker, lang, sample_rate)
    else:
        run_whisper(speaker, lang, sample_rate)
