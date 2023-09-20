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

default_cleaner = 'japanese_cleaners2'

# 기본 cleaner에 대한 symbols 구성
symbols = [cleaner_symbols[default_cleaner]['_pad']] + list(cleaner_symbols[default_cleaner]['_punctuation']) + list(cleaner_symbols[default_cleaner]['_letters'])

SPACE_ID = symbols.index(" ")

"""
# Export all symbols:
symbols = ['_pad'] + list(_punctuation) + list(_letters)

# Special symbol ids
SPACE_ID = symbols.index(" ")
"""
