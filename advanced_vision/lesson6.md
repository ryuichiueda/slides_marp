---
marp: true
---

<!-- footer: "アドバンストビジョン第6回" -->

# アドバンストビジョン

## 第6回: Transformerの構造と用途

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- Transformerの構造
- Transformerの基本的な使い方

---

## Transformerの構造

- エンコーダ、デコーダで構成される
    - 右図の右: エンコーダ
    - 右図の左: デコーダ
        - [<span style="font-size:70%">画像: CC-BY-4.0 by dvgodoy</span>](https://commons.wikimedia.org/wiki/File:Transformer,_full_architecture.png)

<center style="padding-top:3em">順に見ていきましょう</center>

![bg right:45% 100%](https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png)

---

### エンコーダへの入力前と入力後の最初の層正則化

- サブワード$\rightarrow$分散表現（ベクトル）$\rightarrow$位置情報の付加
    - 前回の通り
    - 右図の赤枠部分
- 層正則化（layer normalization）
    - 右図の赤枠の上の「Norm」
    - 各ベクトル$\boldsymbol{h}=(h_1 \ h_2 \ \cdots \ h_D)^\top$の要素を正規化してベクトルごとの影響力を揃える
        - どう正規化するか？
            - 1: $h_{1:D}$の平均値が$0$、標準偏差が$1$に
            - 2: $h_i$ごとに$\gamma_i, \beta_i$（学習対象）というパラメータを用意して$\gamma_ih_i + \beta_i$に変換
                - 要素の位置ごとに重要度が異なるため

![bg right:20% 100%](./figs/transformer_pos.png)

---

### Transformerのエンコーダ: 文脈情報の付加1

- <span style="color:red">自己注意機構</span>という仕組みで文脈の情報を付加
    - 行列$W_Q, W_K, W_V$という3つの行列を使う
        - これらの行列は学習の対象で、ここでは学習が済んでいると仮定
    - $H$のなかのベクトル$\boldsymbol{h}_i$に対して次のベクトルを作成
        - $\boldsymbol{k}_i = W_K\boldsymbol{h}_i$（キー埋め込み）
        - $\boldsymbol{v}_i = W_V\boldsymbol{h}_i$（バリュー埋め込み）
        - $\boldsymbol{q}_i = W_Q\boldsymbol{h}_i$（クエリ埋め込み）
    - 3つのベクトルを使う自己注意機構なので特に
    「キー・クエリ・バリュー注意機構」と呼ばれる方法（次のスライドに続く）

![bg right:20% 100%](./figs/transformer_kvq.png)

---

### Transformerのエンコーダ: 文脈情報の付加2

- $\boldsymbol{k}_i, \boldsymbol{v}_i, \boldsymbol{q}_i$から、文脈を考慮した埋め込みベクトルを計算
    - 手順
        - $i$番目のトークンと$j$番目のトークンの関連性の強さを次のように計算
            - $s_{ij} = \boldsymbol{q}_i^\top \boldsymbol{k}_j/\sqrt{D}$（内積）
        - $s_{ij}$をソフトマックス関数で合計1に正規化
            - $\alpha_{ij} = e^{s_{ij}}/\sum_{j'=1}^Ne^{s_{ij'}}$
        - 次の$\boldsymbol{o}_i$を$i$番目のトークンの埋め込みベクトルとして出力
            - $\boldsymbol{o}_i = \sum_{j=1}^N \alpha_{ij} \boldsymbol{v}_j$

![bg right:20% 100%](./figs/transformer_kvq.png)

---

### Transformerのエンコーダ: 文脈情報の付加3

- $\boldsymbol{o}_i$をフィードフォワード層に通す
    - このあと2層のニューラルネットワークを通ってさらに文脈が強化された文脈化トークン埋め込みに

- 全体で$O=[\boldsymbol{o}_{w_1}\ \boldsymbol{o}_{w_2}\ \dots\ \boldsymbol{o}_{w_N}]^\top$という行列が出力される

![bg right:20% 100%](./figs/transformer_ff.png)

---

## エンコーダの出力を使った翻訳

- 問題の定式化: 条件付き確率の問題にする
（例: 日本語から英語への翻訳）
    - 問題1: 先頭のトークンを選ぶ
        - $p(w_1 |$私 は 牛丼 を 食べ ます 。$)$
    - 問題2: 2番目のトークンを選ぶ
        - $p(w_2 |$私 は 牛丼 を 食べ ます 。, I$)$
    - 問題3: 3番目のトークンを選ぶ
        - $p(w_3 |$私 は 牛丼 を 食べ ます 。, I eat$)$
- Transformerのデコーダがこれを解く
$\Rightarrow$どうやって?

![bg right:35% 100%](./figs/transformer_decoder.png)


---

### デコーダ側の処理1

- 自己注意機構で翻訳途中の文の文脈を埋め込みに反映
    - 途中の文なので計算のときに少し細工が必要だけど、
    エンコーダと同じ

![bg right:15% 100%](./figs/transformer_dec_context.png)


---

### デコーダ側の処理2: <span style="color:red">交差注意機構</span>

- もとの言語の文脈を翻訳中の文に持ち込む
    - クエリ埋め込み$\boldsymbol{q}_i = W_Q\boldsymbol{h}_i$だけデコーダの埋め込みから計算
    - キー埋め込み、バリュー埋め込みは、エンコーダ側の出力から計算


![bg right:15% 100%](./figs/transformer_cross.png)


---

### デコーダ側の処理3: 次の単語の出力

![bg right:15% 100%](./figs/transformer_output.png)

- 全単語について次の単語になる確率を計算して、
その確率が最も高いものを出力
    - 文脈がしっかり考慮されているので、かつての
    マルコフ連鎖ジェネレータのようにはならない
    - その文脈に最もふさわしい単語が出てくる

---

## Transformerの応用例

---

### 分類

- 文を「楽しい」、「悲しい」などいくつかの感情に結びつける
- ANNの構造
    - 文の頭に「クラストークン」をつける
        - 埋め込みベクトルと同じ次元
        - 注意機構
    - エンコーダに通すとクラストークンにもなにか値が入る
    - クラストークンの値の並びから感情を分類するANNをつける
- 学習
    - 全体を教師あり学習
    - 文がエンコーダを通るとクラストークンに分類のための情報が集まるようになる


---

### Vision Transformer (ViT）

- Transformerを画像に転用
    - 画像をブロック状に切って単語のように扱う（右図）
    - 右図のCLS: クラストークン
        - 文の分類と同じ
- 画像をブロック状に扱うのはCNNと同じだが、そのあとが違う
    - CNNは遠くのブロックの関係性を見るのが苦手

[<span style="font-size:70%">画像: CC-BY-4.0 by Daniel Voigt Godoy</span>](https://commons.wikimedia.org/wiki/File:Vision_Transformer.png)

![bg right:40% 100%](https://upload.wikimedia.org/wikipedia/commons/9/93/Vision_Transformer.png)


---

### GPT（Generative Pre-trained Transformer）

- 途中の文から次の単語を予測
    - デコーダだけで構成
- ChatGPTの一部に使われる

[<span style="font-size:70%">画像: CC0 (public domain)</span>](https://commons.wikimedia.org/wiki/File:Full_GPT_architecture.svg)


![bg right:40% 100%](https://upload.wikimedia.org/wikipedia/commons/5/51/Full_GPT_architecture.svg)


---

### ChatGPT

- GPTを使ってテキスト（人の質問や発言）に答える
    - （構造に関する決定的な文献なし）

---

### [Segment Anything](https://segment-anything.com/)

- [コードや説明](https://github.com/facebookresearch/sam2)
- プロンプトの指示で画像から特定の部分を切り出す（セグメンテーション）
- 画像のエンコードにはViTを使う
- プロンプトのエンコードにはCLIPを使う

---

### Stable Diffusion

- プロンプトを画像に変換
    - プロンプトから画像のタネを作るためにCLIPを利用
    - 画像を復元するときにも注意機構
- [図](https://medium.com/data-science/what-are-stable-diffusion-models-and-why-are-they-a-step-forward-for-image-generation-aa1182801d46)


---

## まとめ

- Transformer
    - 埋め込みに文脈を反映させる仕組み
- 埋め込み
    - 次元の高いベクトルで、単語やトークンの様々な関係性を表現可能
    - skip-gramなどの学習方法で実用性のある埋め込みが作成可能
    - ViTなどでは画像に対しても作られる
- 埋め込みを使うと性質の異なるデータを交差注意機構で関連させることが可能
    - ある言語$\rightarrow$別の言語
    - 画像$\leftrightarrow$言語
- 参考文献: [[菊田2025]](https://gihyo.jp/book/2025/978-4-297-15078-5)

---

### どうすればいいか?

- 埋め込みに語順と文脈の情報を付加してやるとよい
- <span style="color:red">Transformer</span>（のエンコーダ）
    - 入力: 潜在表現のベクトルに位置情報を加えたもの
        - さらに<span style="color:red">注意機構</span>で文脈を考慮
    - 出力: <span style="color:red">文脈化トークン埋め込み</span>
        - 各単語の関係性（文脈）に応じて各ベクトルの位置を変更
        - 次の単語の予測などにより有用な埋め込み（使い方はあとで）

![w:1100](./figs/add_context_embedding.png)

---

## Transformerのエンコーダ: 入力


- 入力: 文
    - トークン（単語をより細かく文を区切ったもの）の分散表現でのベクトルを並べたもの
        - $E=[\boldsymbol{e}_{w_1}\ \boldsymbol{e}_{w_2}\ \dots\ \boldsymbol{e}_{w_N}]^\top$という行列に
- 文への位置情報の付加（右図Positional Encoding）
    - 行列$H = \sqrt{D}E + P = [\boldsymbol{h}_{w_1}\ \boldsymbol{h}_{w_2}\ \dots\ \boldsymbol{h}_{w_N}]^\top$を作成
       - $D$: ベクトルの次元（正規化のため）
       - $P$にはトークンが文の何番目にあるかの情報が入る
           - 単純に「何番目か」ではなく三角関数を使ったややこしもの

<center>とりあえずこれで入力に位置情報が加わる</center>

![bg right:20% 100%](./figs/transformer_pos.png)

