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
- 訓練方法（ANNの構成: [原著のFig.1](https://aclanthology.org/N19-1423.pdf)）
    - 事前学習: 文章の穴埋め（masked LM、MLM）タスクと次文予測タスク
    - ファインチューニング: 各用途に応じたタスク

---

### 事前学習

- masked LM（双方向タスクとも）: Transformerのエンコーダに文章の穴埋め問題を解かせる
   - 例: I went to Doutonbori `[MASK]` bus. 
   - エンコーダが出力する埋め込みの先に各単語の確率を出力する全結合層がくっついていてそれが学習
- 次文予測: 2つの文を与えて、続きの文かそうでないかを当てさせる
   - 訓練データの50%を続きの文、50%を別の文にして学習
   - 出力のクラストークンの先に連続/不連続を確率で出す全結合層がくっついていてそれが学習



---

### BERTの使い方

- 様々で、用途にあわせて<span style="color:red">ファインチューニング</span>される
    - [参考](https://wandb.ai/mukilan/BERT_Sentiment_Analysis/reports/An-Introduction-to-BERT-And-How-To-Use-It--VmlldzoyNTIyOTA1)
- 分類
    - クラストークンの出力を分類器へ
- 質問応答
    - 最初に答えの含まれる文を読み込ませ、その後1単語でこたえられるクイズを出して答えさせる
        - クイズの続きになる単語を予測する問題に
- 固有表現抽出（named entity recognition）
    - 未知の単語を「人名」、「地名」、「組織名」・・・などに分類


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

