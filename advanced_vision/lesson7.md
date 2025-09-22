---
marp: true
---

<!-- footer: "アドバンストビジョン第7回" -->

# アドバンストビジョン

## 第7回: Transformerの応用

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- BERT
- GPT

---

## [BERT](https://aclanthology.org/N19-1423/)（Bidirectional Encoder Representations from Transformers）[Devlin2019]

- Transformerのエンコーダを用いたモデル
    - 応用: Google検索
- BERT<span style="font-size:60%;vertical-align:-5pt">BASE</span>、BERT<span style="font-size:60%;vertical-align:-5pt">LARGE</span>がある
    - エンコーダの数: 前者が12、後者が24
    - パラメータの数: 前者が110M、後者が340M
- 訓練方法（ANNの構成: [原著のFig.1](https://aclanthology.org/N19-1423.pdf)）
    - 事前学習: 文章の穴埋め（masked LM、MLM）タスクと次文予測タスクを同時に
        - Wikipedia + 7000冊の書籍
    - ファインチューニング: 各用途に応じたタスク

---

### 入力の形式

- 通常の位置埋め込みの他に、何文目かを表すセグメント埋め込みを各トークンに付与
    - 後発の[RoBERTa](https://arxiv.org/abs/1907.11692)ではセグメント埋め込みは使われない
    （次文予測もしない）
- 特殊トークン
    - `[CLS]`: クラストークン（先頭につける）
    - `[SEP]`: 文の区切り
    - `[MASK]`: 訓練のときにトークンを隠すマスク

---

### 事前学習

- masked LM（双方向タスクとも）: Transformerのエンコーダに文章の穴埋め問題を解かせる
   - 例: `[CLS]` I went to Doutonbori `[MASK]` bus. `[SEP]`
   - エンコーダが出力する埋め込みの先に各単語の確率を出力する全結合層がくっついていてそれが学習
   - たまにマスクせずにそのまま存在する単語を答えさせたり、トークンを入れ替えて正しいものを答えさせたりする
- 次文予測: 2つの文を`[sep]`でつなぎ、続きの文かそうでないかを当てさせる
   - 訓練データの50%を続きの文、50%を別の文にして学習
   - 出力のクラストークンの先に連続/不連続を確率で出す全結合層がくっついていてそれが学習

---

### BERTの使い方

様々で、用途にあわせて<span style="color:red">ファインチューニング</span>される（[参考](https://wandb.ai/mukilan/BERT_Sentiment_Analysis/reports/An-Introduction-to-BERT-And-How-To-Use-It--VmlldzoyNTIyOTA1)）
- 分類、感情分析
    - クラストークンの出力を分類器へ
- 質問応答
    - 最初に答えの含まれる文を読み込ませ、その後1単語でこたえられるクイズを出して答えさせる
        - クイズの続きになる単語を予測する問題に
- 固有表現抽出（named entity recognition）
    - 未知の単語を「人名」、「地名」、「組織名」・・・などに分類
    - 文をラベルに変換（雑な説明ですが）

---

### BERTの使い方（続き）

- 抽出型要約
    - 文から重要な部分を抜き出して要約
    - 構成例[[Liu2019]](https://aclanthology.org/D19-1387.pdf): BERTの上にさらにエンコーダを乗っけて、各文の頭のクラストークンの部分に、その文を出力するかどうかのバイナリを出力
- 抽象型要約
    - ちゃんと書き直して要約
    - できるっぽいが調査中

---

## GPT（Generative Pre-trained Transformer）

- GPT-1
- GPT-2
- GPT-3, 4

---

### [GPT-1 [Radford2018]](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)

- TransformerのデコーダにBERTのように仕事をさせる
    - （BERTはエンコーダだった）
    - この場合のデコーダ: 交差注意機構は用いず、マスクつきの自己注意機構を持つTransformerデコーダ
        - マスク: つまり次の単語の予測で事前学習

[<span style="font-size:70%">画像: CC0 (public domain)</span>](https://commons.wikimedia.org/wiki/File:Full_GPT_architecture.svg)


![bg right:40% 100%](https://upload.wikimedia.org/wikipedia/commons/5/51/Full_GPT_architecture.svg)

---

### GPT-1の学習方法（事前学習）

- マスクのかかっていない部分から次の単語を予測
    - 前ページで書いたとおり
- 特殊トークン: 文章の始まりに`<s>`、終わりに`<e>`
- `<e>`に対応する出力に全結合層をつないで、全単語に対して出現確率を算出
- データ: 様々なジャンルの7000冊の未発表書籍からの4.5GBのテキスト（[BookCorpus](https://github.com/soskek/bookcorpus)）

---

### GPT-1の学習方法（ファインチューニングと意義）

- 事前学習後のデコーダの`extract`に対応する部分にヘッドをつけて特定の仕事をさせる
    - タスクによっては文と文の間に`$`を入れる
    - 分類など
- ただ、こういう作業がいらないんじゃないかという話になった


---

### GPT-2

- ゼロショット学習



---

### ChatGPT

- GPTを使ってテキスト（人の質問や発言）に答える
    - （構造に関する決定的な文献なし）

