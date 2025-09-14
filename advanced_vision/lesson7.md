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

## [BERT](https://arxiv.org/abs/1810.04805)（Bidirectional Encoder Representations from Transformers）

- Transformerのエンコーダを用いたモデル
    - 応用: Google検索
- 訓練方法
    - 双方向タスク: Transformerのエンコーダに文章の穴埋め問題を解かせる
       - 例: I went to Doutonbori `[MASK]` bus. 
    - 次文予測: 2つの文を与えて、続きの文かそうでないかを当てさせる

---

### BERTの構造

- エンコーダの頭に`[MASK]`の


---

### BERTの使い方

- 分類
    - クラストークンを頭につける
- 質問への回答
    - 質問の文を入力すると、回答となる続きの文を出力


---

## GPT（Generative Pre-trained Transformer）

- 途中の文から次の単語を予測
    - デコーダだけで構成
- ChatGPTの一部に使われる

[<span style="font-size:70%">画像: CC0 (public domain)</span>](https://commons.wikimedia.org/wiki/File:Full_GPT_architecture.svg)


![bg right:40% 100%](https://upload.wikimedia.org/wikipedia/commons/5/51/Full_GPT_architecture.svg)


---

### ChatGPT

- GPTを使ってテキスト（人の質問や発言）に答える
    - （構造に関する決定的な文献なし）

