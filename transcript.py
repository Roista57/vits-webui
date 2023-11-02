from faster_whisper import WhisperModel
import argparse
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import os
import wave
from tqdm import tqdm


def resample_wav(input_wav_path, output_wav_path, target_sample_rate=22050):
    # If the output file already exists and has the correct parameters, skip processing.
    if os.path.exists(output_wav_path):
        try:
            with wave.open(output_wav_path, 'rb') as wf:
                num_channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                sample_rate = wf.getframerate()
        except wave.Error as e:
            print(f"An error occurred while reading {output_wav_path}: {e}")
            return False
        if num_channels == 1 and sample_width == 2 and sample_rate == target_sample_rate:
            return True

    # Process the input WAV file
    try:
        audio = AudioSegment.from_wav(input_wav_path)
        audio_duration = len(audio)
        if not (1000 <= audio_duration <= 10000):
            print(f"{input_wav_path} is out of the valid duration range (1-10 seconds).")
            return False
        resampled_audio = audio.set_frame_rate(target_sample_rate)
        resampled_audio.export(output_wav_path, format="wav")
        return True
    except CouldntDecodeError as e:
        print(f"Could not decode {input_wav_path}. It might not be a valid audio file: {e}")
        return False
    except Exception as e:
        print(f"An unspecified error occurred while loading {input_wav_path}: {e}")
        return False


def check_wav_files(wav_path):
    try:
        with wave.open(wav_path, 'rb') as wf:
            """
            num_channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            sample_rate = wf.getframerate()
            
            if num_channels != 1:
                print(f"{wav_path}:{num_channels} is not mono.")
            if sample_width != 2:
                print(f"{wav_path}:{sample_width} does not have a sample width of 2.")
            if sample_rate not in (8000, 16000, 32000, 48000):
                print(f"{wav_path}:{sample_rate} does not have a valid sample rate.")
            if num_channels == 1 and sample_width == 2 and sample_rate in (8000, 16000, 32000, 48000):
                print(f"{wav_path} meets all the requirements.")
            """
            return True
    except wave.Error as e:
        print(f"Failed to open or read {wav_path} due to a WAV error: {e}")
        return False


def whisper_script(model, path, lang):
    segments, info = model.transcribe(path, language=lang, beam_size=5)
    text = "".join(segment.text for segment in segments).strip()
    return text


def get_speaker_index(filename, speakers_mapping):
    # 상위 폴더의 이름을 가져온다.
    speaker_folder_name = os.path.basename(os.path.dirname(filename))
    # 해당 이름을 기반으로 index를 반환한다.
    return speakers_mapping[speaker_folder_name]

def run_whisper_to_script(args):
    base_input_dir = 'audio'
    base_output_dir = 'filelists'

    speaker = args.speaker
    language = args.language
    sample_rate = args.samplerate
    run_tqdm = args.tqdm

    try:
        model_size = "large-v2"
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
    except Exception as e:
        print(f"Error initializing Whisper model: {e}. Exiting...")
        return

    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)

    input_dir = os.path.join(base_input_dir, "SP" if speaker == "Single" else "MP")
    output_dir = os.path.join(base_output_dir, "SP" if speaker == "Single" else "MP")

    filenames = [os.path.join(dirpath, filename) for dirpath, _, files in os.walk(input_dir) for filename in files if filename.endswith('.wav')]
    iterator = tqdm(filenames, desc="Processing", disable=not run_tqdm)

    if speaker == "Multi":
        # audio/MP 폴더 내의 모든 폴더들의 이름을 가져와 순서대로 index를 부여
        speaker_folders = sorted([folder for folder in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, folder))])
        speakers_mapping = {name: idx for idx, name in enumerate(speaker_folders)}
    else:
        speakers_mapping = {}

    with open("filelists/filelists.txt", "w", encoding='utf-8') as file:
        for filename in iterator:
            try:
                if not os.access(filename, os.R_OK):
                    print(f"Error: No read access to {filename}. Skipping...")
                    continue

                output_wav_path = os.path.abspath(os.path.join(output_dir, os.path.relpath(filename, input_dir)))
                output_dir_path = os.path.dirname(output_wav_path)

                # print(f"Checking existence of directory: {output_dir_path}")
                if not os.path.exists(output_dir_path):
                    # print(f"Creating directory: {output_dir_path}")
                    os.makedirs(output_dir_path)

                if resample_wav(filename, output_wav_path, sample_rate):
                    text = whisper_script(model, output_wav_path, language)
                    # 기존 코드에서 speaker 처리 부분을 요구사항에 맞게 수정
                    if speaker == "Multi":
                        idx = get_speaker_index(filename, speakers_mapping)
                        file.write(f"{output_wav_path}|{idx}|{text}\n")
                        if not run_tqdm:
                            print(f"{output_wav_path}|{idx}|{text}\n")
                    else:
                        file.write(f"{output_wav_path}|{text}\n")
                        if not run_tqdm:
                            print(f"{output_wav_path}|{text}\n")
            except Exception as e:
                print(f"Error processing {filename} with Whisper or during resampling: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--speaker", type=str, choices=['Single', 'Multi'], required=True, help="Specify if it's single or multi speaker.")
    parser.add_argument("--language", type=str, required=True, help="Language of the audio files.")
    parser.add_argument("--samplerate", type=int, default=22050, help="Target sample rate for resampling.")
    parser.add_argument("--tqdm", action="store_true", help="Show progress bar.")

    args = parser.parse_args()

    try:
        run_whisper_to_script(args)
    except Exception as e:
        print(f"Error running script: {e}")