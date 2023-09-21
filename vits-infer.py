"""
https://github.com/ilya-scherzo/b2ins.git
gradio webui inference v1.02
python vits-infer.py --config_path path/to/config.json --model_path path/to/model.pth
"""

import argparse
import torch
from torch import no_grad, LongTensor
import commons
import utils
import webbrowser
import gradio as gr
from models import SynthesizerTrn
from text import text_to_sequence, _clean_text


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm).to(device)
    return text_norm


def create_tts_fn(model, hps, speaker_ids):
    def tts_fn(text, speaker, speed, noise_scale_value, noise_scale_w_value):
        speaker_id = speaker_ids[speaker]
        stn_tst = get_text(text, hps)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
            sid = LongTensor([speaker_id]).to(device)
            audio = model.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale_value, noise_scale_w=noise_scale_w_value, length_scale=1.0 / speed)[0][0, 0].data.cpu().float().numpy()
        del stn_tst, x_tst, x_tst_lengths, sid
        return "Success", (hps.data.sampling_rate, audio)

    return tts_fn


def create_to_phoneme_fn(hps):
    def to_phoneme_fn(text):
        return _clean_text(text, hps.data.text_cleaners) if text != "" else ""

    return to_phoneme_fn

css = """
        #advanced-btn {
            color: white;
            border-color: black;
            background: black;
            font-size: .7rem !important;
            line-height: 19px;
            margin-top: 24px;
            margin-bottom: 12px;
            padding: 2px 8px;
            border-radius: 14px !important;
        }
        #advanced-options {
            display: none;
            margin-bottom: 20px;
        }
"""


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", required=True, help="path to config file")
    parser.add_argument("--model_path", required=True, help="path to model file")
    args = parser.parse_args()

    models_tts = []
    name = 'VITS-TTS demo v1.02'
    example = '학습은 잘 마치셨나요? 좋은 결과가 있길 바래요.'

    config_path = args.config_path
    model_path = args.model_path

    hps = utils.get_hparams_from_file(config_path)
    model = SynthesizerTrn(
        len(hps.symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).to(device)
    utils.load_checkpoint(model_path, model, None)
    model.eval()
    speaker_ids = [sid for sid, name in enumerate(hps.speakers) if name != "None"]
    speakers = [name for sid, name in enumerate(hps.speakers) if name != "None"]

    models_tts.append((name, speakers, example,
                        hps.symbols, create_tts_fn(model, hps, speaker_ids),
                        create_to_phoneme_fn(hps)))

    app = gr.Blocks(css=css)

    with app:
        gr.Markdown("Gradio VITS-TTS Inference demo v1.02\n\n")
        with gr.Tabs():
            for i, (name, speakers, example, symbols, tts_fn,
                    to_phoneme_fn) in enumerate(models_tts):
                with gr.TabItem(f"VITS-TTS_v1.02"):
                    with gr.Column():
                        gr.Markdown(f"## {name}\n\n")
                        tts_input1 = gr.TextArea(label="Text",
                                                 elem_id=f"tts-input{i}")

                        if hps.data.text_cleaners[0] == "korean_cleaners":
                            # 예제 입력 및 출력 제공
                            gr.Examples(
                                examples=[
                                    ["학습은 잘 마치셨나요? 좋은 결과가 있길 바래요."],
                                    ["오늘의 날씨는 어떻게 되나요? 비가 오려나요?"],
                                    ["저는 AI 기술에 대한 연구를 진행 중입니다."],
                                    ["주말 계획은 이미 정해두셨나요? 어디로 가실 건가요?"],
                                    ["음성 인식 기술의 발전에 대해 어떻게 생각하시나요?"],
                                    ["휴일에는 가족들과 함께 행복한 시간을 보내고 싶어요."],
                                    ["한국어 TTS 시스템은 다양한 목소리로 테스트해보세요."],
                                    ["AI 모델의 학습 시간을 단축하고 싶은데 조언 부탁드려요."],
                                    ["데이터 전처리 과정에서 주의할 점이 무엇인가요?"],
                                    ["감사합니다! 당신의 도움 덕분에 문제를 해결했어요."]
                                ],
                                inputs=[tts_input1]
                            )
                        elif hps.data.text_cleaners[0] == "japanese_cleaners2":
                            # 예제 입력 및 출력 제공
                            gr.Examples(
                                examples=[
                                    ["料理をするのが趣味で、よく家で夕食を作ります。"],
                                    ["最近の技術進歩は驚くべきものがありますね。"],
                                    ["週末はどこかに旅行する予定がありますか？"],
                                    ["私はAI技術の研究をしている大学生です。"],
                                    ["日本語の音声認識システムをテストしています。"],
                                    ["天気予報によると、明日は雨が降るそうです。"],
                                    ["読書は心のリフレッシュに最適な趣味だと思います。"],
                                    ["AIの進化について、どのように感じていますか？"],
                                    ["今日の夕食は何を作る予定ですか？美味しそう!"],
                                    ["ありがとうございます。あなたの助けで問題を解決しました。"]
                                ],
                                inputs=[tts_input1]
                            )

                        tts_input2 = gr.Dropdown(label="Speaker", choices=speakers,
                                                    type="index", value=speakers[0])
                        tts_input3 = gr.Slider(label="Speed", value=1, minimum=0.1, maximum=2, step=0.05)

                        noise_scale_slider = gr.Slider(label="Noise-scale (defaults = 0.667)", value=0.667, minimum=0, maximum=1, step=0.01)
                        noise_scale_w_slider = gr.Slider(label="Noise-width (defaults = 0.8)", value=0.8, minimum=0, maximum=2, step=0.05)

                        tts_submit = gr.Button("Generate", variant="primary")
                        tts_output1 = gr.Textbox(label="Output Message")
                        tts_output2 = gr.Audio(label="Output Audio")

                        tts_submit.click(tts_fn, [tts_input1, tts_input2, tts_input3, noise_scale_slider, noise_scale_w_slider],
                                            [tts_output1, tts_output2])

        gr.Markdown(
            "Originate from \n\n"
            "- [https://github.com/kdrkdrkdr]\n\n"
            "- [https://github.com/ilya-scherzo]\n\n"
        )
    webbrowser.open("http://127.0.0.1:7860/")
    app.queue(concurrency_count=3).launch(server_port=7860, share=True, show_api=False)


if __name__ == "__main__":
    main()
