""" from https://github.com/keithito/tacotron """
from text import cleaners
from text.symbols import symbols, cleaner_symbols

# 기본 Mappings
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

def _update_symbols(cleaner_name):
    """ Update symbols based on cleaner """
    global _symbol_to_id, _id_to_symbol
    if cleaner_name in cleaner_symbols:
        choice_symbols = cleaner_symbols[cleaner_name]
        current_symbols = [choice_symbols['_pad']] + list(choice_symbols['_punctuation']) + list(choice_symbols['_letters'])
        _symbol_to_id = {s: i for i, s in enumerate(current_symbols)}
        _id_to_symbol = {i: s for i, s in enumerate(current_symbols)}

def text_to_sequence(text, cleaner_names):
    '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.'''
    sequence = []
    print(f"++++++++++++++++++++++++++++  __init__.py cleaner_names : {cleaner_names}  ++++++++++++++++++++++++++++")
    clean_text = _clean_text(text, cleaner_names)

    # Update symbols for the current cleaner
    if cleaner_names:
        _update_symbols(cleaner_names[0])

    for symbol in clean_text:
        if symbol not in _symbol_to_id.keys():
            continue
        symbol_id = _symbol_to_id[symbol]
        sequence += [symbol_id]
    return sequence


def cleaned_text_to_sequence(cleaned_text):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = [_symbol_to_id[symbol] for symbol in cleaned_text if symbol in _symbol_to_id.keys()]
  return sequence


def sequence_to_text(sequence):
  '''Converts a sequence of IDs back to a string'''
  result = ''
  for symbol_id in sequence:
    s = _id_to_symbol[symbol_id]
    result += s
  return result


def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text)
    for char in text:
      if char not in symbols:
        text.replace(char, '')
  return text
