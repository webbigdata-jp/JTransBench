# JTransBench

日本語翻訳スコアを簡単にベンチマークするためのツール群  
Tools for easily benchmarking Japanese translation scores  


## Setup

(1) 仮想環境作成(option) (Create a virtual environment (optional))

```
python3 -m venv venv
source venv/bin/activate
```

(2)ライブラリのインストール (Installing libraries)

```
pip install -r requirements.txt
```

## 使い方 (How to use)

### (1)データセットのダウンロード(Download the dataset)

```
python3 1_datasetup.py
```

これによりflores200データセットがdataset/original以下にダウンロードされます。  
This will download the flores200 dataset into the dataset/original directory.  

更に見分けやすいように名称を変更した flores200, wmt22, wmt23の各テストセットがdataset/use以下にコピーされます。  
The test sets flores200, wmt22, and wmt23, whose names have been changed to make them easier to distinguish, are copied to the dataset/use directory.  

```
行数(line number) ファイル名(file name)
1012 flores200v1-enja.ref
1012 flores200v1-enja.src
flores200を英日翻訳用に名称変更したデータ。*.srcが元の英語。*.refが参照用の日本語訳。以下同様  
Data that has been renamed from flores200 for English-Japanese translation. *.src is the original English. *.ref is the Japanese translation for reference. Same below.  

1012 flores200v1_jaen.ref
1012 flores200v1_jaen.src
2037 wmt22_enja.ref
2037 wmt22_enja.src
2008 wmt22_jaen.ref
2008 wmt22_jaen.src
2074 wmt23_enja.ref
2074 wmt23_enja.src
1992 wmt23_jaen.ref
1992 wmt23_jaen.src
```

全部を使ってテストするのはかなり時間がかかるので必要なデータだけをwork配下にコピーするのが良いでしょう  
Testing everything takes a lot of time, so it's a good idea to copy only the data you need to work.

自分自身のデータセットを使う際は下記の命名規則に合わせる必要があります
If you use your own datasets, they must adhere to the following naming conventions  

```
元の文章: <データセット名称_(enja or jaen).src>
参照翻訳: <データセット名称_(enja or jaen).ref>

Original text: <Dataset name_(enja or jaen).src>
Reference translation text: <Dataset name_(enja or jaen).ref>
```



### 2_Translate

翻訳作業はあなた独自のモデル／環境で好きな形式で実施する事ができます
You can translate in your own model/environment in any format you like.

もし、flores200v1-enja.srcを翻訳した場合は
flores200v1-enja.hyp
と言う名称でworkディレクトリ配下に保存してください

If you translated flores200v1-enja.src, save it as flores200v1-enja.hyp in the work directory.

翻訳作業終了時には
・同名で拡張子だけ異なるsrc, ref, hypの3種類のファイルがwork配下に存在する
・各ファイルは同じ行数
になっている必要があります

When the translation is complete,
- Three files with the same name but different extensions, src, ref, and hyp, must exist in the work directory.
- Each file must have the same number of lines.


以下はtransformers形式とgguf形式のモデルで翻訳を実施する際のサンプルスクリプトです
conf配下に格納されている設定ファイルを適宜改変し、ご自分のモデルを動かしてください

Below is a sample script for translating models in transformers and gguf formats.
Please modify the configuration file stored under conf as appropriate and run your own model.


2_1_transformer_translate_sample.py

実行には以下のライブラリの追加インストールが必要です
The following libraries must be installed to run the program

```
peft==0.11.1
bitsandbytes==0.43.1

python3 2_1_transformer_translate_sample.py  --input work --output work --config conf/2_1_transformer_translate_sample.conf

```


2_2_gguf_translate_sample.py
実行にはllama.cppのインストールが必要です
llama.cpp must be installed to run.

```

python3 2_2_gguf_translate_sample.py --input work --output work --conf conf/2_2_gguf_translate_sample.conf
```

### 3_eval.py
3_eval.py

spBLEU, chrf++, cometの三指標で評価をおこないます

spBLEUは最もよく使われているBLEUスコアの改良版です
spBLEU is an improved version of the most popular BLEU score.

chrF2++短いテキストや文法が異なる言語間での翻訳評価に適しています
chrF2++ Suitable for evaluating short texts and translations between languages with different grammar

cometは深層学習ベースのモデルで人間の評価に近いとされています。  
Comet is a deep learning-based model that is said to be close to human evaluation.  

cometの実行にはGPUが必須です。
A GPU is required to run comet.  

cometは三種類存在し、最初に発表されたcomet(wmt22-comet-da)、改良版のXCOMET-XL, XCOMET-XXLが存在します。
XCOMET-XXLは10.7Bサイズのモデルであり 15GB程度のGPUメモリでは動かす事ができないのでコメントにしてあります

There are three types of comet: the first announced comet (wmt22-comet-da), the improved versions XCOMET-XL and XCOMET-XXL.
XCOMET-XXL is a 10.7B model and cannot run on a GPU with around 15GB of memory, so this is commented out.


3_eval.pyを実行するとworkディレクトリ配下の*.srcと*.refの各ペアに対して以下のファイルが出来ます
When you run 3_eval.py, the following files are created for each pair of *.src and *.ref in the work directory.

*.hyp.spBLEU
*.hyp.chrf
*.hyp.comet
*.hyp.xlcomet
*.hyp.xxlcomet

これらはツールが出力した生の評価データでなので必要に応じて参考にしてください  
These are the raw evaluation data output by the tool, so please refer to them as needed.


### 4_result.py

```
python3 4_result.py
```

4_result.pyを実行すると3で作成した各評価データを読みこんで整形して出力します。  
When you run 4_result.py, it will read the evaluation data created in 3, format it, and output it.  

```
filename direction spBLEU chrF2++ comet xlcomet xxlcomet
mytest enja 25.74 34.7 0.9016 0.8875
mytest jaen 36.0 59.9 0.8246 0.8872
```


## 補足(Notes)

3つ決めることがある

(1)どのデータをつかってテストするか？
(2)どの指標を使ってテストするか？
(3)どのツールを使ってテストするか？

(1)どのデータをつかってテストするか？
自作データ使ってテストするのも有効ですが、他のモデルが発表してくれている指標と比較する事ができない
ので有名なデータを使ってやることも必要。大きく分けて2つある。

1-1)flores200
meta社が作った超多言語翻訳能力をベンチマークするデータ
1012の例文が204の言語に翻訳されているため多言語翻訳能力を試す際によく使われる
元文章はニュース記事などのフォーマルよりの文章

2024-05-13時点の最新版としてVersion2が公開されている(本PJではまだ未対応)
主にデータが少ない低リソース言語に焦点をあてている。
事前トレーニングデータとして収集される事を防ぐため、 パスワード付きのファイルで提供されており
パブリックなサイトへの転載も禁止されている

1-2)WMT(Workshop on Machine Translation)
WMT（Workshop on Machine Translation）は、機械翻訳の最新の研究と技術を紹介する国際会議で、毎年開催
されている。同時に翻訳競技会も開催され、その競技会で使用されたデータが終了後に公開される。
例えば、2023年のデータは「wmt23」となる

WMTのデータは多様な言語ペアが存在し、ダウンロード元や公開タイミングがわかりにくいことが多いため、>データを効率的にダウンロードするためのツールが存在するほど。

wmt22はニュース記事などのフォーマルよりの文章

(2)どの指標を使ってテストするか？
指標は沢山あるが、 一長一短
様々な新しい指標が発表されているので網羅は難しいが、ツールが決まれば利用可能な指標も自然と決まる
私が意識しているのは下記
spBLEU, chrf++, comet(Unbabel/wmt22-comet-da,  Unbabel/XCOMET-XL, Unbabel/XCOMET-XXL)

cometは人間の評価に近い計測ができるとされているが、GPUが必須で一番大きいXCOMET-XXLは
15GB程度のGPUメモリでは動かす事ができない

(3)どのツールを使ってテストするか？
flores200の説明書の中で言及されているfairseq + sacrebleu及びUnbabel/COMETを私は使っています








# 謝辞(Acknowledgements)

このプロジェクトで利用させて頂いた以下のプロジェクト、データセット、及びデータセットの元文章の著作者に感謝します  
We would like to thank the following projects, datasets, and authors of the original documents used in this project: 

- [facebookresearch/fairseq](https://github.com/facebookresearch/fairseq)
- [facebookresearch/flores](https://github.com/facebookresearch/flores/blob/main/flores200/README.md)
- [wmt22](https://www.statmt.org/wmt22/)
- [wmt23](https://www2.statmt.org/wmt23/mtdata/)
- [mjpost/sacrebleu](https://github.com/mjpost/sacrebleu)
- [Unbabel/COMET](https://github.com/Unbabel/COMET)






