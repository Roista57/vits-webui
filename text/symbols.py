import json


# 설정 파일에서 설정 로드
def load_settings(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        settings = json.load(file)
    return settings


'''
Defines the set of symbols used in text input to the model.
'''

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

settings_file = 'setting.json'
settings = load_settings(settings_file)
default_cleaner = settings['text_cleaners'][0]

# 기본 cleaner에 대한 symbols 구성
symbols = [cleaner_symbols[default_cleaner]['_pad']] + list(cleaner_symbols[default_cleaner]['_punctuation']) + list(cleaner_symbols[default_cleaner]['_letters'])

SPACE_ID = symbols.index(" ")