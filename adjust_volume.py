import os
import argparse
from tqdm import tqdm
import subprocess


def run_adjust_volume(input_folder, output_folder, args):
    all_files = []
    for root, _, files in os.walk(input_folder):
        for file in tqdm(files, desc=f"{root}"):
            if file.endswith(('.wav', '.mp3')):
                all_files.append((file, root))
                audio_input = os.path.join(root, file).replace('\\', '/')
                audio_output = audio_input.replace(input_folder, output_folder)
                os.makedirs(os.path.dirname(audio_output), exist_ok=True)
                command = rf'ffmpeg\bin\ffmpeg.exe -y -i "{audio_input}" -ar {args.target_sample_rate} -ac {args.channel} -af loudnorm=I={args.volume_dest}:TP=-2:LRA=11 "{audio_output}"'
                subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('--volume-dest', '-v', type=int, dest='volume_dest', required=False, default=-25)
    args.add_argument('--target-sample-rate', '-sr', type=int, dest='target_sample_rate', required=False, default=44100)
    args.add_argument('--channel', '-c', type=int, dest='channel', required=False, default=1)
    args.add_argument('--extention', '-e', type=str, dest='extention', required=False, default='wav')
    args = args.parse_args()

    input_folder = "audio/input/"
    output_folder = "audio/output/"

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    run_adjust_volume(input_folder, output_folder, args)