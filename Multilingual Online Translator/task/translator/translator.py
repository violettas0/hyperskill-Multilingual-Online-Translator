import sys
import requests
from bs4 import BeautifulSoup
import argparse

languages = ["Arabic", "German","English","Spanish","French","Hebrew","Japanese","Dutch", "Polish",
             "Portuguese","Romanian","Russian","Turkish"]


parser = argparse.ArgumentParser()
parser.add_argument('source_lang', help='The source language.')
parser.add_argument('target_lang', help='The target language or "all" for all languages.')
parser.add_argument('word', help='The word to translate.')
args = parser.parse_args()
source_lang = args.source_lang
target_lang = args.target_lang
word = args.word

headers = {'User-Agent': 'Mozilla/5.0'}



with open(f'{word}.txt', 'w', encoding='utf-8') as f:
    pass



def translating(word,source_lang, target_lang, n_example):
    while True:
        try:
            url = f'https://context.reverso.net/translation/{source_lang.lower()}-{target_lang.lower()}/{word}'
            page = requests.get(url, headers=headers)
            page.encoding = 'utf-8'
            if page.status_code == 200:
                html_content = page.text
                soup = BeautifulSoup(html_content, 'html.parser')

                translation_sent = []
                orig_sent = []
                words = []

                translated_words = soup.select('.display-term')

                for element in translated_words:
                    words.append(element.get_text())

                og_sent = soup.select('.trg.ltr, .trg.rtl')
                trs_sent = soup.select('.src.ltr, .src.rtl')

                for element in og_sent:
                    translation_sent.append(element.get_text().strip())
                for element in trs_sent:
                    orig_sent.append(element.get_text().strip())

                pairs = dict(zip(orig_sent, translation_sent))
                print(f'{target_lang.capitalize()} Translations:')
                with open(f'{word}.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{target_lang.capitalize()} Translations:\n')
                if len(words) > 0:
                    length = 0
                    for tr_word in words:
                        if length == n_example:
                            break
                        else:
                            length += 1
                            print(f'{tr_word}')
                            with open(f'{word}.txt', 'a', encoding='utf-8') as f:
                                f.write(f'{tr_word}\n')
                print(f'{target_lang.capitalize()} Examples:')
                with open(f'{word}.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{target_lang.capitalize()} Examples:\n')
                if len(pairs) > 0:
                    length = 0
                    for trg, src in pairs.items():
                        if length == n_example:
                            break
                        else:
                            length += 1
                            print(f'{trg}')
                            print(f'{src}')
                            with open(f'{word}.txt', 'a', encoding='utf-8') as f:
                                f.write(f'{trg}\n')
                                f.write(f'{src}\n')
                break
            elif page.status_code == 404:
                print(f'Sorry, unable to find {word}')
                sys.exit()

        except requests.exceptions.RequestException as e:
            print('Something wrong with your internet connection')
            sys.exit()

if target_lang.capitalize() not in languages and target_lang != 'all':
    print(f'Sorry, the program doesn\'t support {target_lang}')
    sys.exit()
elif target_lang == 'all':
    for lang in languages:
        if lang == source_lang:
            pass
        else:
            translating(word, source_lang, lang, 1)
else:
    translating(word, source_lang, target_lang, 5)

