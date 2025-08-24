---
marp: true
---

<!-- footer: "アドバンストビジョン第6回" -->

# アドバンストビジョン

## 第6回: Transformerの構造とVision Transformer

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- Transformerの構造
- Transformerエンコーダによる分類

---

## Transformer（翻訳用途）の構造

- エンコーダ、デコーダで構成される
    - 右図の左: エンコーダ
        - 入力: 翻訳前の文
        （例: これはペンです。）
    - 右図の右: デコーダ
        - 入力: 「翻訳開始」を表すトークンあるいは途中まで翻訳した文（例: This is）
        - 出力: 次の単語（例: a）

<center style="padding-top:0.5em">順に見ていきましょう</center>

![bg right:45% 100%](https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png)

[<span style="font-size:70%">画像: CC-BY-4.0 by dvgodoy</span>](https://commons.wikimedia.org/wiki/File:Transformer,_full_architecture.png)

---

### エンコーダ

- 濃い黄色の枠が本体
    - 「Nx layers」: 何個も連結するということ
    - 詳しくは次のページ以降で
- 入力（図の下方）: $H_\text{enc} = \sqrt{D}E + P$
    - $E=[\boldsymbol{e}_{w_1}\ \boldsymbol{e}_{w_2}\ \dots\ \boldsymbol{e}_{w_N}]^\top$
        - 文（$D$次元ベクトルで表現されたトークンを並べたもの）
- 出力: デコーダでの仕事に応じて重みの変わった$H_\text{enc}'$
    - 文脈が反映されている

![bg right:28% 95%](./figs/transformer_encoder.png)


---

### 層正則化（layer normalization）

- 図中に3つある「Norm」
- 各ベクトル$\boldsymbol{h}=(h_1 \ h_2 \ \cdots \ h_D)^\top$の要素を正規化してベクトルごとの影響力を揃える
    - どう正規化するか？
        - 1: $h_{1:D}$の平均値が$0$、標準偏差が$1$に
        - 2: $h_i$ごとに$\gamma_i, \beta_i$（学習対象）というパラメータを用意して$\gamma_ih_i + \beta_i$に変換
            - 要素の位置ごとに重要度が異なるため

![bg right:28% 95%](./figs/transformer_encoder.png)

---

### <span style="color:red">自己注意機構</span>

- 自分自身の情報でトークンの重みを変える
    - 例: 「ガラス窓を割ったのは私です。」ならガラスと私を強調する等の働き
- 仕組み: Q、K、Vをすべて自身への入力から作成
    - クエリ: $Q= W_\text{Q}H$<span style="color:red">$_\text{enc}$</span>（前回は$H_\text{dec}$だった）
    - キー: $K= W_\text{K}H$<span style="color:red">$_\text{enc}$</span>（同上）
    - バリュー: $V= W_\text{V}H_\text{enc}$
    - 出力: $H'=$Softmax$\Big(\dfrac{QK^\top}{\sqrt{D}}\Big)V$
- 前回の注意機構は<span style="color:red">交差注意機構</span>

![bg right:20% 100%](./figs/transformer_kvq.png)

---

### マルチヘッド注意機構

- Transformerの実装では注意機構が複数に分割される
    - $W_\text{K}, W_\text{V}, W_\text{Q}$（$D \times D$行列）が分割される
        - $Q^{(m)}= W_\text{Q}^{(m)}H$
        - $K^{(m)}= W_\text{K}^{(m)}H$
        - $V^{(m)}= W_\text{V}^{(m)}H\quad$（$m=1,2,\dots,M$）
            - $W_X^{(m)}$: $W_X$を横に切った$(D/M) \times D$行列
    - ANN的には、$m$ごとに結合が切れて独立
        - それぞれが文の解釈方法を変える
        （ように学習されるらしい）
- 出力の$Q^{(m)}, K^{(m)}, V^{(m)}$を結合$\rightarrow$元の$D \times D$行列に

![bg right:20% 100%](./figs/transformer_kvq.png)

---

### フィードフォワード層（全結合層）

- 自己注意機構を通った文が通される
    - 右図の2つの点線の枠のうち上のほう
    - 非線形な活性化関数を通して特徴をより強調
- 活性化関数: GELU（Gaussian Error Linear Unit）の使用
    - $h(x) = x\cdot \frac{1}{2}\big\{ 1 + \text{erf}(x/\sqrt{2})\big\}$
        - $\text{erf}(a) = \frac{2}{\sqrt{\pi}}\int_0^a e^{-t^2}\text{d}t$
![w:300](https://upload.wikimedia.org/wikipedia/commons/4/42/ReLU_and_GELU.svg)<span style="font-size:50%">（[画像by Ringdongdang CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:ReLU_and_GELU.svg)）</span>

![bg right:28% 95%](./figs/transformer_encoder.png)

---

### その他補足

- 注意機構もフィードフォワード層もスキップ接続を使用
    - 各層で学習/出力されるのは差分
- 学習初期に各層にわかりやすい入力をするため
    - 層が深いので必要

![bg right:20% 95%](./figs/transformer_encoder_body.png)

---

### エンコーダのまとめ

- 次のような挙動を実現するように学習される
    - 文をトークンのベクトルを並べて位置の情報を加えた行列$H_\text{enc}$で受け取る
    - 自己注意機構と全結合層で$H$中の各ベクトルを文脈にあわせて操作
        - ↑繰り返し
    - 文脈の反映された$H'_\text{enc}$を出力
- 受け取る逆伝播誤差がどんなものかは
デコーダ側による

![bg right:28% 95%](./figs/transformer_encoder.png)


---

### デコーダ（とデーコーダの先）

- 本体は緑の枠内
    - 途中までの作文に対応する行列$H_\text{dec}$を受け取り
- デコーダの先に具体的な仕事をするためのANNが接続される
    - 翻訳の場合は次の単語を予測するための全結合層
    - デコーダはこの仕事がしやすいように$H_\text{dec}$を$H'_\text{dec}$に変更


![bg right:50% 100%](./figs/transformer_decoder.png)

---

### デコーダの本体

- （自己注意機構+交差注意機構+フィードフォワード層）$\times N$
- 自己注意機構
    - 翻訳途中の文の文脈を考慮して$H_\text{dec}$を操作
    - 図中の「Masked」の意味: 文の後半にマスクをかける仕組み
        - 学習の際、完成された翻訳例が入力されてくるので必要に
        - 例: 「This is」の次を考える訓練をするときに、「This is a pen.」が入力されてくるので、$W_X$の「a pen」に対応する要素にマスク
- 交差注意機構
    - デコーダの出力$H'_\text{enc}$を反映

![bg right:15% 100%](./figs/transformer_decoder2.png)

---

### デコーダの先

- 全結合層でデーコーダの入力の次の単語を予測
    - skip-gramのように学習可能
    - 出力は各トークンが次にくる確率
        - トークンの種類だけ次元がある
- この部分の誤差を逆伝播することで学習が進行
    - 損失関数: 交差エントロピー
        - $-\sum_{i=1}^{N_\text{token}} P(\boldsymbol{e}_i)\log Q(\boldsymbol{e}_i)$
        $= - \log Q(\boldsymbol{e}^*)$
            - $\boldsymbol{e}^*$: 正解のトークン

![bg right:40% 125%](./figs/transformer_prediction.png)

---

### Transformer（翻訳用途）の構造のまとめ

- 結局どんな問題を解いていたのか？$\rightarrow$こういう確率の問題
    - $\Pr\{$次に来る単語$|$翻訳前の文章$,\quad\!\!\!\!$翻訳途中の文章$\}$
- Transformerの工夫
    - 翻訳前の文章、翻訳途中の文章に位置情報を付加
    - 文脈の考慮
        - 翻訳前の文章から注目すべき箇所を自己注意機構で
        発見して埋め込みに反映（エンコーダ）
        - 翻訳途中の文章を自己注意機構にかけて文脈を考慮した上で、
        さらにエンコーダからの文脈を交差注意機構で反映

---

## Transformerエンコーダによる分類

- Transformerを分類タスクに応用することを考える
    - 入力: 文（例: 今日、100円を拾いました。）
    - 出力: 感情（楽しい、嬉しい、悲しいなど）
- エンコーダで構成可能[[中井2025]](https://gihyo.jp/book/2025/978-4-297-14972-7)

---

### 他のタスクでの

- 分類: 文を「楽しい」、「悲しい」などいくつかの感情に結びつける
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


