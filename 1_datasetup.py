import os
import subprocess

# ディレクトリの作成
os.makedirs('dataset/original', exist_ok=True)
os.makedirs('dataset/use', exist_ok=True)

# flores200データセットのダウンロードと解凍
os.chdir('dataset/original')
subprocess.run(['wget', 'https://tinyurl.com/flores200dataset', '-O', 'flores200dataset.tgz'])
subprocess.run(['tar', 'xvfz', 'flores200dataset.tgz'])
subprocess.run(['rm', '-f', 'flores200dataset.tgz'])


# ファイルのコピー
subprocess.run(['cp', 'flores200_dataset/devtest/jpn_Jpan.devtest', '../use/flores200v1_jaen.src'])
subprocess.run(['cp', 'flores200_dataset/devtest/eng_Latn.devtest', '../use/flores200v1_jaen.ref'])
subprocess.run(['cp', 'flores200_dataset/devtest/jpn_Jpan.devtest', '../use/flores200v1_enja.ref'])
subprocess.run(['cp', 'flores200_dataset/devtest/eng_Latn.devtest', '../use/flores200v1_enja.src'])

# NTREX-128データセットのコピー
subprocess.run(['cp', '../../external/NTREX/NTREX-128/newstest2019-src.eng.txt', '../use/NTREX-128_enja.src'])
subprocess.run(['cp', '../../external/NTREX/NTREX-128/newstest2019-ref.jpn.txt', '../use/NTREX-128_enja.ref'])

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

# モデルのダウンロード
os.chdir('../..')
os.makedirs('models', exist_ok=True)
os.chdir('models')
subprocess.run(['wget', 'https://tinyurl.com/flores200sacrebleuspm', '-O', 'flores200_sacrebleu_tokenizer_spm.model'])

