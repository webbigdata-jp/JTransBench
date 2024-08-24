import os
import json
import subprocess

# ディレクトリの作成
os.makedirs('dataset/original', exist_ok=True)
os.makedirs('dataset/use', exist_ok=True)

# flores200データセットのダウンロードと解凍
os.chdir('dataset/original')
subprocess.run(['wget', 'https://tinyurl.com/flores200dataset', '-O', 'flores200dataset.tgz'])
subprocess.run(['tar', 'xvfz', 'flores200dataset.tgz'])
subprocess.run(['rm', '-f', 'flores200dataset.tgz'])

# flores200ファイルのコピー
subprocess.run(['cp', 'flores200_dataset/devtest/jpn_Jpan.devtest', '../use/flores200v1_jaen.src'])
subprocess.run(['cp', 'flores200_dataset/devtest/eng_Latn.devtest', '../use/flores200v1_jaen.ref'])
subprocess.run(['cp', 'flores200_dataset/devtest/jpn_Jpan.devtest', '../use/flores200v1_enja.ref'])
subprocess.run(['cp', 'flores200_dataset/devtest/eng_Latn.devtest', '../use/flores200v1_enja.src'])

# NTREX-128データセットのコピー
subprocess.run(['cp', '../../external/NTREX/NTREX-128/newstest2019-src.eng.txt', '../use/NTREX-128_enja.src'])
subprocess.run(['cp', '../../external/NTREX/NTREX-128/newstest2019-ref.jpn.txt', '../use/NTREX-128_enja.ref'])

# BSDデータセットの変換とコピー
input_file = '../../external/BSD/test.json'
output_enja_src = '../use/Business_Scene_Dialogue_corpus_enja.src'
output_enja_ref = '../use/Business_Scene_Dialogue_corpus_enja.ref'
output_jaen_src = '../use/Business_Scene_Dialogue_corpus_jaen.src'
output_jaen_ref = '../use/Business_Scene_Dialogue_corpus_jaen.ref'

# ファイル内容のリセット
with open(output_enja_src, 'w') as f:
    f.write('')
with open(output_enja_ref, 'w') as f:
    f.write('')
with open(output_jaen_src, 'w') as f:
    f.write('')
with open(output_jaen_ref, 'w') as f:
    f.write('')

# JSONファイルの読み込み
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 変換処理
for item in data:
    if item['original_language'] == 'en':
        with open(output_enja_src, 'a', encoding='utf-8') as src_file, open(output_enja_ref, 'a', encoding='utf-8') as ref_file:
            for convo in item['conversation']:
                src_file.write(f"{convo['en_speaker']}: {convo['en_sentence']}\n")
                ref_file.write(f"{convo['ja_speaker']}: {convo['ja_sentence']}\n")
    elif item['original_language'] == 'ja':
        with open(output_jaen_src, 'a', encoding='utf-8') as src_file, open(output_jaen_ref, 'a', encoding='utf-8') as ref_file:
            for convo in item['conversation']:
                src_file.write(f"{convo['ja_speaker']}: {convo['ja_sentence']}\n")
                ref_file.write(f"{convo['en_speaker']}: {convo['en_sentence']}\n")


# SacreBLEUによるデータの準備
os.chdir('../use')
subprocess.run(['sacrebleu', '-t', 'wmt22', '-l', 'en-ja', '--echo', 'src'], stdout=open('wmt22_enja.src', 'w'))
subprocess.run(['sacrebleu', '-t', 'wmt22', '-l', 'en-ja', '--echo', 'ref'], stdout=open('wmt22_enja.ref', 'w'))
subprocess.run(['sacrebleu', '-t', 'wmt22', '-l', 'ja-en', '--echo', 'src'], stdout=open('wmt22_jaen.src', 'w'))
subprocess.run(['sacrebleu', '-t', 'wmt22', '-l', 'ja-en', '--echo', 'ref'], stdout=open('wmt22_jaen.ref', 'w'))

subprocess.run(['sacrebleu', '-t', 'wmt23', '-l', 'en-ja', '--echo', 'src'], stdout=open('wmt23_enja.src', 'w'))
subprocess.run(['sacrebleu', '-t', 'wmt23', '-l', 'en-ja', '--echo', 'ref'], stdout=open('wmt23_enja.ref', 'w'))
subprocess.run(['sacrebleu', '-t', 'wmt23', '-l', 'ja-en', '--echo', 'src'], stdout=open('wmt23_jaen.src', 'w'))
subprocess.run(['sacrebleu', '-t', 'wmt23', '-l', 'ja-en', '--echo', 'ref'], stdout=open('wmt23_jaen.ref', 'w'))

subprocess.run(['sacrebleu', '-t', 'wmt20', '-l', 'en-ja', '--echo', 'src'], stdout=open('wmt20_enja.src', 'w'))
subprocess.run(['sacrebleu', '-t', 'wmt20', '-l', 'en-ja', '--echo', 'ref'], stdout=open('wmt20_enja.ref', 'w'))
subprocess.run(['sacrebleu', '-t', 'wmt20', '-l', 'ja-en', '--echo', 'src'], stdout=open('wmt20_jaen.src', 'w'))
subprocess.run(['sacrebleu', '-t', 'wmt20', '-l', 'ja-en', '--echo', 'ref'], stdout=open('wmt20_jaen.ref', 'w'))


# モデルのダウンロード
os.chdir('../..')
os.makedirs('models', exist_ok=True)
os.chdir('models')
subprocess.run(['wget', 'https://tinyurl.com/flores200sacrebleuspm', '-O', 'flores200_sacrebleu_tokenizer_spm.model'])

