---
marp: true
---

<!-- footer: "アドバンストビジョン第5回" -->

# アドバンストビジョン

## 第5回: 埋め込みと文脈の付加

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- なんでビジョンの講義で言葉（自然言語）を扱うのか
- Word2vec
- Transformer
- Transformerの応用例

---

## なんでビジョンの講義で自然言語を扱うのか

- 画像$\leftrightarrow$言葉のアプリケーションの存在
    - 画像説明文生成
    - プロンプトへの指示$\rightarrow$画像の生成や指定した物体の認識
        - Stable Diffusion
        - Segment Anything Model
        ↑いずれも今回扱うTransformerを使用
- 言語処理の手法の画像処理への転用
    - Transformer$\rightarrow$Vision Transformer
    - データの種類が異なるだけで本質的な違いは少ない（？）
- Transformerの普及: 上記のように様々なところで利用

<center>やらざるをえない</center>

---

## Word2vec[[Mikolov2013]](https://arxiv.org/abs/1301.3781)

- 単語をベクトル表現するためのモデル群や枠組み
- Word2vecで作られたベクトル表現はTransformerの入力に

---

### 単語のベクトル表現（単語の埋め込み、分散表現）

- 近い単語は似たベクトルに
    - 例（適当。上記のように次元はもっと必要）
        - おじさん$= (0.9, 0.32, 0.07)$
        - おばさん$= (0.7, 0.55, 0.08)$
        - 不動産$= (0.1, 0.05, 0.88)$
    - 類似度が内積で計算できる
        - おじさん$\cdot$おばさん$=0.77$
        - おじさん$\cdot$不動産$=0.07$
    - 次元を大きくすると、様々な切り口で類似度を計算可能
- <span style="color:red">分散表現（埋め込み表現）</span>: 上記のような単語のベクトル表現
- <span style="color:red">埋め込み</span>: 分散表現を作ること

![bg right:20% 100%](./figs/embedding.png)

---

### 埋め込みとこれまでの内容の関係

- 分散表現の空間=潜在空間
    - 入力をエンコーダで別の空間に写像
    - （Word2vecの場合は確率は考えない）
- 疑問
    - 単語同士の類似度を潜在空間に作り出すには？
        - エンコーダ側の構造は？
        - デコーダ側の構造は？
        - 何を学習させる？

![bg right:40% 100%](./figs/word_latent.png)

---

### 分布仮説（distributional hypothesis）

- "You shall know a word by the company it keeps!" [[Firth1957]](https://cs.brown.edu/courses/csci2952d/readings/lecture1-firth.pdf)
    - ![](./figs/ass.png)
        - ass言い過ぎ
    - ある単語の意味は周辺の単語が担っているということ
- つまり、ある単語のベクトルの値は、文の前後の単語から決めるとよい
（仮説が正しいならば）
    - [Mikolov2013]では、この性質を利用した分散表現の作成方法が
    2つ示されている

<center>順に見ていきましょう</center>

---

### 埋め込みの方法1: skip-gram

- 右図の構造のANNを準備
    - アフィン層2つとソフトマックス層
- 受け付ける入力: $\boldsymbol{v} = (0\ 0\ \cdots\ 1\ 0\ \cdots\ 0)$
    - ある単語について、その単語に対応する要素が$1$になったone-hotベクトル
    - 単語の種類だけ次元がある
- アフィン層間のベクトル$\boldsymbol{x}$: 数百〜数千次元
    - <span style="color:red">これが分散表現に</span>
- 出力: 入力と同じ次元のベクトル
    - 各単語に対応する確率

![bg right:35% 100%](./figs/skip_gram.png)

---

### skip-gramの学習

- ある単語$w$のone-hotベクトル$\boldsymbol{v}_{w}$に対し、ある範囲内に別の単語$\boldsymbol{w}'$がある確率を学習
    - <span style="font-size:60%">お詫び: 「範囲内」なのか位置を具体的に指定するのかは何を読んでもよく分からないのでコードを読まないといけないんですがまだです</span>
    - たくさんの文献から訓練データを作成
    - 単語間の関係を反映した埋め込みが可能
- <span style="color:red">$X$の各行が分散表現に</span>
    - $X = [\boldsymbol{x}_{w_1}\ \boldsymbol{x}_{w_2}\ \dots\ \boldsymbol{x}_{w_N}]^\top$
    - $\boldsymbol{x}_{w_i} = \boldsymbol{v}_{w_i}X$
        - ある単語$w_i$のone-hotベクトル$\boldsymbol{v}_{w_i}$を入力すると、$\boldsymbol{x}_{w_i}$が得られる

![bg right:35% 100%](./figs/skip_gram.png)

---

### 埋め込みの方法2: Continuous Bag-of-Words（CBoW）

- 下図のANNに次の学習をさせる
    - 文のなかの単語を隠して、周辺の$C$個の単語から隠した単語を当てる
        - 例: "Tokyo Skytree is the __ tower in Japan."（$C=2$）
        $\rightarrow$ is、the、tower、inからtallestを推測させる
- ANNの入出力
    - 入力: 前後$C$範囲内の単語のone-hotベクトルを平均したもの
    - 出力: 各単語について、隠された文字である確率を記録したもの
        - skip-gramと同じく次元は単語の種類の数
- skip-gramと同様、<span style="color:red">$X$の各行が潜在表現のベクトルに</span>

$\qquad\qquad\qquad\qquad$![w:600](./figs/cbow.png)

---

## Transformer

---

### 埋め込みができればコンピュータが文章を認識する?

・・・ことはできない

- 最尤な単語をskip-gramで予想して並べていけばそれっぽい文は作れるけど、たぶん無意味な文ができる
    - [マルコフ連鎖ジェネレータ](https://lorem.sabigara.com/?source=ginga-tetsudo&format=plain&sentence_count=5)のようなもの
- 単純な埋め込みには限界
    - 語順に関する情報は、完全にはない
    - 文脈依存な情報を持っていない
        - 同音異義語に1つのベクトル$\rightarrow$区別してない
            - 例: チンチラ（げっ歯類にも猫にもいる）

<center>どうしましょう？</center>

![bg right:20% 100%](./figs/Chinchilla.jpg)


<span style="font-size:70%">
<a href="https://commons.wikimedia.org/wiki/Chinchilla_lanigera#/media/File:Chinchilla_lanigera_(Wroclaw_zoo)-2.JPG">写真上 by Guérin Nicolas（CC BY-SA 3.0）</a>
<a href="https://commons.wikimedia.org/wiki/File:Chinchilla_cat_(3228221937).jpg">写真下 by allen watkin（CC BY-SA 2.0）</a>


---

### どうすればいいか?

- 埋め込みに語順と文脈の情報を付加してやるとよい
    - 潜在表現のベクトルに位置情報を付加
    - さらに<span style="color:red">注意機構</span>で文脈を考慮
- <span style="color:red">Transformer</span>[[Vaswani2017]](https://arxiv.org/abs/1706.03762)で考案された
    - これらの仕組みで既存のANNを凌駕
        - Transformerの概略と入力を説明してから順に説明していきます

---

### Transformer

- 翻訳のためにGoogleで開発された
    - [使ってみましょう](https://translate.google.co.jp/?hl=ja&sl=en&tl=ja&op=translate)
- 正体: 右のような構造のANN
    - エンコーダ（左側）とデコーダ（右側）で構成
- 画像にも応用されている
    - Vision Transformer（ViT）
- その他言葉を扱うもので新しいものは、だいたいこれの応用

![bg right:45% 100%](https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png)

[<span style="font-size:70%">画像: CC-BY-4.0 by dvgodoy</span>](https://commons.wikimedia.org/wiki/File:Transformer,_full_architecture.png)


---

### Transformerへの入力（エンコーダ）

- 文章: サブワード単位のトークン（単語をより細かく文を区切って埋め込みをしたもの）の分散表現でのベクトルを並べたもの
    - $E=[\boldsymbol{e}_{w_1}\ \boldsymbol{e}_{w_2}\ \dots\ \boldsymbol{e}_{w_N}]^\top$という行列に
    - 右の例では省略されているが`<EOS>`（文の終わり）などの特殊なトークンも入力として並べる

![bg right:30% 95%](./figs/sentence.png)

---

### Transformerへの入力（デコーダ）

- デコーダの場合は途中までの文を入力
    - `<SOS> I want to eat`など
        - （`<SOS>`: start of sentence）
- `<SOS>`から始めて、翻訳したものを次に入力に回す
    - 最初の入力: `<SOS>`
    - 次の入力: `<SOS> I`
    - 次の入力: `<SOS> I want`
    - ・・・と文ができていく
    （実際はエンコーダと同じく行列$E$を入力）

![bg right:30% 95%](./figs/translate.png)

---

### 位置情報の追加

- エンコーダに入力する$E$の各トークンに、文章中での位置情報を付加
    - $H = \sqrt{D}E + P = [\boldsymbol{p}_1\ \boldsymbol{p}_2\ \dots\ \boldsymbol{p}_N]^\top$を作成
        - $p_i = (p_{i,0} \quad p_{i,1} \quad \cdots \quad p_{i,D})^\top$
           - $p_{i,j} = \begin{cases}
            \sin ( i \beta^{-j/D})  & (i\%2 = 0) \\
            \cos ( i \beta^{-(j-1)/D}) & (i\%2 = 1) 
\end{cases}$
    - 下の例（$\beta=10$。原著では$\beta = 10000$）
    - おそらく$\sqrt{D}$のおかげで微かな情報の付加に

$\qquad\qquad$![w:700](./figs/position_enc.png)

![bg right:30% 100%](./figs/position_encoding.png)

---

### 文脈の考慮の必要性

- 必要な例
    - 例1: 「ガラス窓を割ったのは私です。」を英語に翻訳
        - "It's me who broke the ..."まで翻訳したとき、次に注目すべきは壊れるもの（=ガラス）
    - 例2: 右上の丸を月と認識させたい
- 既存の時系列情報や画像を扱うANNは苦手
    - 「近い位置にある=関連性が大きい」と捉えるので
        - 日本語と英語で語順が違っているので難しい
        - 丸が他の手がかりが丸と離れていて難しい

![bg right:20% 95%](./figs/tsukimi.png)

---

### 注意機構（attention機構）

- なにかを出力する際、文脈上、入力のどこに注目するかを
決める（決めるように訓練される）機構
    - glassを出力したい時にはbrokeやtheに注目
    - 丸が分からないので画像の別の特徴も注意して見る
- 注意機構の層がやること
    - 注目すべき埋め込みのベクトルに重みをかけて後段の層に伝達
        - $\boldsymbol{w}$を$\alpha\boldsymbol{w}$に
        - ↑どうやって？（次ページ）

---

### キー・バリュー・クエリを使った注意機構

- クエリ: 問い合わせのこと
    - 例: 翻訳の例のIt's me who broke the
- キー・バリュー: データベース用語
    - キーに値をぶら下げるキーバリュー型データベースなどのたとえ
    デコーダのある箇所の場合、翻訳前の言語の埋め込みから作成（そうでない箇所もあるので次回くわしく）
- クエリにキーが反応して、対応するバリューが出力される
    - 例: クエリ中のbrokeに「割った」が反応して、日本語の文脈で重みづけ

![bg right:35% 95%](./figs/kvq.png)

---

### 具体的な計算

- クエリ: $Q= W_\text{Q}H_\text{dec}$という行列
    - 以下、$W_\text{X}$は学習で獲得する行列
- キー: クエリに反応するトークンを選択
    - $K= W_\text{K}H_\text{enc}$を用意して$QK^\top$を計算
- バリュー: 重み付けの値
    - $V= W_\text{V}H_\text{enc}$
- 出力: Softmax$\Big(\dfrac{QK^\top}{\sqrt{D}}\Big)V$

そうしろと人間が言ってるわけではないが、こういう構造を用意してあげるとそういうふうに学習

![bg right:35% 95%](./figs/kvq.png)

---

## まとめ

- 埋め込み
    - 次元の高いベクトルで、単語やトークンの様々な関係性を表現可能
    - skip-gramなどの学習方法で実用性のある埋め込みが作成可能
    - ViTなどでは画像に対しても作られる
- Transformer
    - 一言でいうと、埋め込みに注意機構で文脈を反映させる仕組み
    - <span style="color:red">詳しくは次回</span>
- 補足: 位置情報については決め打ちではなく学習させる方法もあり
- 参考文献: [[菊田2025]](https://gihyo.jp/book/2025/978-4-297-15078-5)
