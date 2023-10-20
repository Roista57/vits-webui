import json


'''
Defines the set of symbols used in text input to the model.
'''
"""
cleaner_symbols = {
    'japanese_cleaners2': {
        '_pad': '_',
        '_punctuation': ',.!?-~…',
        '_letters': 'AEINOQUabdefghijkmnoprstuvwyzʃʧʦ↓↑ '
    },
    'korean_cleaners': {
        '_pad': '_',
        '_punctuation': ',.!?…~',
        '_letters': 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉㅏㅓㅗㅜㅡㅣㅐㅔ '
    },
    'chinese_cleaners': {
        '_pad': '_',
        '_punctuation': '，。！？—…',
        '_letters': 'ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏㄐㄑㄒㄓㄔㄕㄖㄗㄘㄙㄚㄛㄜㄝㄞㄟㄠㄡㄢㄣㄤㄥㄦㄧㄨㄩˉˊˇˋ˙ '
    },
    'zh_ja_mixture_cleaners':{
        '_pad': '_',
        '_punctuation' : ',.!?-~…',
        '_letters' : 'AEINOQUabdefghijklmnoprstuvwyzʃʧʦɯɹəɥ⁼ʰ`→↓↑ '
    },
    'sanskrit_cleaners':{
        '_pad': '_',
        '_punctuation' : '।',
        '_letters' : 'ँंःअआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलळवशषसहऽािीुूृॄेैोौ्ॠॢ '
    },
    'cjks_cleaners':{
        '_pad': '_',
        '_punctuation' : ',.!?-~…',
        '_letters' : 'NQabdefghijklmnopstuvwxyzʃʧʥʦɯɹəɥçɸɾβŋɦː⁼ʰ`^#*=→↓↑ '
    },
    'thai_cleaners':{
        '_pad': '_',
        '_punctuation' : '.!? ',
        '_letters' : 'กขฃคฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลวศษสหฬอฮฯะัาำิีึืุูเแโใไๅๆ็่้๊๋์'
    },
    'cjke_cleaners2':{
        '_pad': '_',
        '_punctuation' : ',.!?-~…',
        '_letters' : 'NQabdefghijklmnopstuvwxyzɑæʃʑçɯɪɔɛɹðəɫɥɸʊɾʒθβŋɦ⁼ʰ`^#*=ˈˌ→↓↑ '
    },
    'shanghainese_cleaners':{
        '_pad': '_',
        '_punctuation' : ',.!?…',
        '_letters' : 'abdfghiklmnopstuvyzøŋȵɑɔɕəɤɦɪɿʑʔʰ̩̃ᴀᴇ15678 '
    },
    'chinese_dialect_cleaners':{
        '_pad': '_',
        '_punctuation' : ',.!?~…─',
        '_letters' : '#Nabdefghijklmnoprstuvwxyzæçøŋœȵɐɑɒɓɔɕɗɘəɚɛɜɣɤɦɪɭɯɵɷɸɻɾɿʂʅʊʋʌʏʑʔʦʮʰʷˀː˥˦˧˨˩̥̩̃̚ᴀᴇ↑↓∅ⱼ '
    }
}


# setting.json을 읽어 text_cleaners의 값을 반환
def load_settings():
    json_file = 'setting.json'
    with open(json_file, 'r', encoding='utf-8') as file:
        setting_json = json.load(file)
    return setting_json['text_cleaners'][0]


default_cleaner = load_settings()

# setting.json의 text_cleaners의 값에 해당하는 언어의 심볼들을 symbols에 리스트 형태로 저장
symbols = [cleaner_symbols[default_cleaner]['_pad']] + list(cleaner_symbols[default_cleaner]['_punctuation']) + list(cleaner_symbols[default_cleaner]['_letters'])

SPACE_ID = symbols.index(" ")
"""


# symbols.json에서 cleaner_symbols 데이터를 로드하는 함수
def load_cleaner_symbols():
    with open('text/symbols.json', 'r', encoding='utf-8') as file:
        return json.load(file)


# setting.json에서 기본 cleaner 설정을 로드하는 함수
def load_settings():
    with open('setting.json', 'r', encoding='utf-8') as file:
        setting_json = json.load(file)
    return setting_json['text_cleaners'][0]


# 기본 cleaner 설정을 로드
default_cleaner = load_settings()
# cleaner_symbols을 로드
cleaner_symbols = load_cleaner_symbols()

# 선택된 cleaner에 대한 심볼들을 가져와서 symbols 리스트 생성
symbols = [cleaner_symbols[default_cleaner]['_pad']] + list(cleaner_symbols[default_cleaner]['_punctuation']) + list(cleaner_symbols[default_cleaner]['_letters'])

# SPACE_ID 설정
SPACE_ID = symbols.index(" ")