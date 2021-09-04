"""Compute density coefficient."""


import argparse
import pprint
import re


CHARS_PER_PAGE = 1800
PUNCTUATION_MARKS = [' ', '"', "'", '-', '^']
COLOUR_BASED_PATTERNS = {
    'aquamarine': 'aquamarine',
    'auburn': 'auburn',
    'azure': 'azure',
    'beige': 'beige',
    'black': 'black',
    'blue': 'blu(e|ish)',
    'brown': 'brown',
    'carmine': 'carmine',
    'celeste': 'celeste',
    'cerise': 'cerise',
    'cerulean': 'cerulean',
    'crimson': 'crimson',
    'cyan': 'cyan',
    'emerald': 'emerald',
    'ginger': 'ginger',
    'grey': 'gr(a|e)y',
    'green': 'green',
    'indigo': 'indigo',
    'khaki': 'khaki',
    'lilac': 'lilac',
    'madder': 'madder',
    'magenta': 'magenta',
    'maroon': 'maroon',
    'mauve': 'mauve',
    'nude': 'nude',
    'orange': 'orang(e|y|ish)',
    'pink': 'pink',
    'purple': 'purpl(e|y|ish)',
    'red': 'red',
    'rosy': 'rosy',
    'ruddy': 'ruddy',
    'scarlet': 'scarlet',
    'sienna': 'sienna',
    'teal': 'teal',
    'turquoise': 'turquoise',
    'ultramarine': 'ultramarine',
    'umber': 'umber',
    'vermilion': 'vermill?ion',
    'violet': 'violet',
    'viridian': 'viridian',
    'white': 'white',
    'yellow': 'yellow'
}
ADDED_WORDS = ['colou?red', 'shaded', 'tinted', 'hued']


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Calculating colour density in text')
    parser.add_argument(
        '-t', '--text_path', type=str, required=True,
        help='path to source text'
    )
    parser.add_argument(
        '-e', '--encoding', type=str, default='utf-8',
        help='encoding of source text file (by default, utf-8 is used)'
    )
    cli_args = parser.parse_args()
    return cli_args


def generate_patterns():
    punctuations_marks_group = f"({'|'.join(PUNCTUATION_MARKS)})"
    anti_added_words_group = f"(?!-({'|'.join(ADDED_WORDS)}))"
    patterns = {}
    for k, v in COLOUR_BASED_PATTERNS.items():
        patterns[k] = punctuations_marks_group + f"({v})" + anti_added_words_group
    patterns['of colour'] = 'of [^ ]+ colou?r'
    patterns['colour of'] = 'colou?r of'
    patterns['of shade'] = 'of [^ ]+ shade'
    for added_word in ADDED_WORDS:
        key = added_word if added_word != 'colou?red' else 'coloured'
        patterns[key] = f'[^ ]-{added_word}'
    return patterns


def main():
    cli_args = parse_cli_args()
    with open(cli_args.text_path, "r", encoding=cli_args.encoding) as source_file:
        file_content = source_file.read()
    file_content = file_content.lower()

    results = {}
    patterns = generate_patterns()
    for key, pattern in patterns.items():
        results[key] = len(re.findall(pattern, file_content))

    print('Counts of colour names:')
    pp = pprint.PrettyPrinter()
    pp.pprint({k: v for k, v in results.items() if v > 0})
    print()

    colour_name_count = sum(v for k, v in results.items())
    print(f'Total number of colour names: {colour_name_count}.')
    text_length = len(file_content)
    print(f'Text length in symbols: {text_length}.')
    number_of_pages = text_length / CHARS_PER_PAGE
    density_coef = colour_name_count / number_of_pages
    print(f'Density coefficient: {density_coef}.')


if __name__ == '__main__':
    main()
