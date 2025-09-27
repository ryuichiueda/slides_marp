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
- GPT-3
    - ChatGPT
- GPT-4

---

### [GPT-1 [Radford2018]](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)

- TransformerのデコーダにBERTのように仕事をさせる
    - （BERTはエンコーダ）
    - この場合のデコーダ: 交差注意機構は用いず、マスクつきの自己注意機構を持つTransformerデコーダ
        - マスク: つまり次の単語の予測で事前学習

[<span style="font-size:70%">画像: CC0 (public domain)</span>](https://commons.wikimedia.org/wiki/File:Full_GPT_architecture.svg)


![bg right:40% 100%](https://upload.wikimedia.org/wikipedia/commons/5/51/Full_GPT_architecture.svg)

---

### GPT-1の学習方法（事前学習その1）

- 事前学習のデータ: 様々なジャンルの7000冊の未発表書籍からの4.5GBのテキスト（[BookCorpus](https://github.com/soskek/bookcorpus)）
- マスクのかかっていない部分から次の単語を予測
    - 前ページで書いたとおり
    - 損失関数: $\mathcal{L}(\boldsymbol{\Theta}) = -\sum_i \log P(w_i | w_{{i-k}:{i-1}}, \boldsymbol{\Theta})$
        - $w_i$: 予測したいトークン
        - $w_{i-k:i-1}$: 予測に使うトークン
        - $k$: 過去のトークンを読ませる範囲（打ち切りの閾値）

---

### GPT-1の学習方法（事前学習その2）

- 特殊トークンの付加: 文章の始まりに`<s>`、終わりに`<e>`
- `<e>`に対応する出力$\boldsymbol{h}_\text{<e>}$に全結合層をつないで、
    全単語に対して出現確率を算出
    - $P(w_i) =$softmax$(W\boldsymbol{h}_\text{<e>})$
    - クラストークンのように`<e>`の部分に読み込んだ文章の意味が集約されているという考え

![bg right:20% 100%](./figs/gpt-1_pt.svg)

---

### GPT-1の学習方法（ファインチューニング）

- 事前学習後のデコーダの`<e>`に対応する部分にヘッドをつけて特定の仕事に特化
    - BERTで扱うような問題（GPT-1のほうが先だけど）
    - 高い性能を発揮（割愛）
       - 高い性能は重要だが次のページの成果がもっと大きい

---

### <span style="color:red">ゼロショット</span>での使用の検討

- ファインチューニングなしでGPTを利用
- GPT-1の論文での方法（選択肢のあるクイズに答えさせる例）
    - なにかを質問して答えが最後のトークンにくるようにする
    - 答えのトークンの出現確率を比較して一番高いものを答えに
- 1つのトークンだけでなく、質問を入力して出力を促せば文章で答えを出してくれるのではないか？
    - GPTは本質的に言葉を出し続けるモデル
    <span style="color:red">$\Longrightarrow$GPT-2に続く</span>

---

### [GPT-2 [Radford2019]](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)

- GPT-1をスケールアップ
    - パラメータ数、学習の量を10倍に
    - インターネットから4500万件のリンクを収集し、80GB のテキストを取得
- 論文ではゼロショット学習を追求
    - タスクに応じてモデルを変えるのではなく、タスクも入力してしまう
        - $P($答え$|$タスク$,$入力$)$
        - 例: 「日本語に翻訳: This is a pen. 」、「要約: （長い文章）」
- できるのか？$\rightarrow$パラメータと学習量を増やしてみる（GPT-1のときに学習量で性能が上がっていったので）


---

### GPT-2の能力

- 先述のように、「◯◯:」とタスクの指示を入力として受け取って応答
    - ファインチューニングなしでタスクをこなす汎用性を獲得
    - ただし、タスクによっては依然ファインチューニングが必要
- 架空の記事を書く[[Radford2019]](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)のTable 13
- <span style="color:red">論文ではまだ学習の余地があることを示唆</span>

---

### [GPT-3 [Brown 2020]](https://arxiv.org/abs/2005.14165)

- モデルを大きく、学習量をさらに増やす
    - 1750億パラメータ、2048トークンまで予測に利用、3000億トークンを学習に使用
- 計算量の対策
    - 疎な注意機構[[Child2019]](https://arxiv.org/abs/1904.10509)
        - 通常の注意機構に挟んで（交互に）使用
        - 計算量を削減
            - 特定の位置関係にあるトークンだけを計算の対象に
                - つまり手動アテンション
    - GPUに合わせた構造に

---

### 質問の方法の考案

- 論文ではGPT-3へ質問を次のように分けて入力
    - タスク説明: （例）「Translate English to French」
    - 例示: （例）「sea otter => loutre de mer」
        - 例示がひとつ: <span style="color:red">ワンショット</span>
        - 例示が数個: <span style="color:red">少数（few）ショット</span>
    - プロンプト:（例）「答えて =>」（論文だと「cheese =>」）
- <span style="color:red">文脈内学習</span>
    - 上記のような例示で出力を調整
    - ファインチューニングの代わり
    - 重みの更新はしない（問題を解き終わったら忘れる）

---

### GPT-3の成果

- 少数ショットで4則演算ができるように
- 出力した架空の記事が、人間の書いたものと区別がつかない
- <span style="color:red">ChatGPT</span>
    - GPTを使って<span style="color:red">プロンプト</span>（人のテキスト入力）に答えるサービス
        - 「プロンプト」:タスク説明、例示、プロンプトをまとめた呼称
        - ファインチューニングが不要になって
        様々な質問に答えるサービスが可能に
- 学習量をさらに増やしても性能が上がりそうという見通し

---

### [GPT-4 [OpenAI]](https://arxiv.org/abs/2303.08774)

- 社会的な影響から構造が非公開に
    - パラメータ: GPT-3の数倍〜数十倍？（単位が兆の可能性）
- <span style="color:red">画像も入力可能に</span>
    - 画像+テキストについては次回


---

### Reinforcement Learning from Human Feedback (RLHF) [[Christiano 2017]](https://proceedings.neurips.cc/paper_files/paper/2017/file/d5e2c0adad503c91f91df240d0cd4e49-Paper.pdf)

- GPT-4で導入された仕組み[（[Ouyang 2022]？）](https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf)
    - 人間からのフィードバックで強化学習
- ロボットの複雑な動き（料理や片付け）を生成するときに報酬関数が分からないので、人に様々な動きを提示して比較してもらい、人に状態遷移の点数をつけてもらうことで報酬を設計
    - 絶対評価でなく比較だと人は点数がつけやすいらしい

---

### 「ハルシネーション（幻覚）」

- 突然変なことを言い始める
- 1つずつ単語を出力しているわけなので、
直前の単語の並びによっては話が逸れていく
    - みなさんも面接とかでテンパって変なことを口走ったことはありませんか？
- 単なる確率モデルを擬人化する表現で、誤解を生むので論文でも注意喚起

---

- 参考文献
    - 山田他: 大規模言語モデル入門, 技術評論社, 2023.
    - 菊田 遥平: 原論文から解き明かす生成AI, 技術評論社, 2025.
