---
marp: true
---

<!-- footer: "機械学習（と統計）第13回" -->

# 機械学習

## 第13回: 言語と人工ニューラルネットワーク

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 機械学習での言葉の扱い方
- Transformer

---

## 機械学習での言葉の扱い方

- 単語の埋め込み
    - ひとつの単語を次元の大きな（数百〜数千次元の）ベクトルに置き換える
    - 「近い」単語は似たベクトル（内積の値が大きくなるよう）にする
        - 例（てきとうです）
            - おじさん$= (0.9, 0.32, 0.07)$
            - おばさん$= (0.7, 0.55, 0.08)$
            - 不動産$= (0.1, 0.05, 0.88)$
                - 当然、日本語の単語はもっと多いので次元は大きい必要がある
- 埋め込むと計算ができる
    - 類似度が内積で計算できる

---

## 埋め込みの方法（例: skip-gram）

- [word2vec](https://arxiv.org/pdf/1301.3781)というモデル群のなかのひとつ
- 人工ニューラルネットワーク
    - ある単語について、文の左右にある単語を予想させる
    （つまり確率$\Pr\{$単語$w'$が範囲$p$以内にある$|$単語$w$がある$\}$を求める）
- 学習のための損失関数: $\mathcal{L}(\boldsymbol{\Theta}) = - \dfrac{1}{N}\sum_{i=1}^N\sum_{-p\le j \le p} \log P(w_{i+j}|w_i, \boldsymbol{\Theta})$
    - ある文$w_1, w_2, \dots, w_N$に対して
    - 大量の文章から学習
- 重要: 予想できるようになったネットワークの途中の
    層の重みから<span style="color:red">埋め込みのベクトル</span>が計算できる

---

### skip-gramの埋め込みでできるもの1

- 単語が$w_1, w_2, \dots, w_N$だけあると、それぞれに対応する埋め込みのベクトル$\boldsymbol{x}_{w_1}, \boldsymbol{x}_{w_2}, \dots, \boldsymbol{x}_{w_N}$ができる
    - 並べると$X=[\boldsymbol{x}_{w_1}\ \boldsymbol{x}_{w_2}\ \dots\ \boldsymbol{x}_{w_N}]^\top$という行列に
    - 空間にプロットすると右図のような分布ができる
        - 意味的に近いものが近くに
        - 空間の次元が高いので、切り出し方によって
        様々な意味での遠近が出現
- これらのベクトル、行列そのものや、それらを作ることを「埋め込み」と呼んでいる 


![bg right:20% 100%](./figs/embedding.png)

---

### skip-gramの埋め込みでできるもの2

- もうひとつ、左右の単語の予測のための行列$U$というものもできる
    - $\boldsymbol{x}_{w_i}$に作用させて別の単語に対して出現確率を計算できる
        - $P(w_j | w_i) = \text{softmax}_{w_j}(U \boldsymbol{x}_{w_i})$
            - ベクトル$U\boldsymbol{x}_{w_i}$: $w_i$に対する各単語の関連性の強さを表す
            - $\text{softmax}$: ソフトマックス関数（強さを確率に正規化する関数）
    - $U=[\boldsymbol{u}_{w_1}\ \boldsymbol{u}_{w_2}\ \dots\ \boldsymbol{u}_{w_N}]^\top$を構成するベクトル$\boldsymbol{u}_{w_j}$も埋め込みのベクトル
        - おそらく双対ベクトルの一種

---

### 埋め込みができて、skip-gramができればコンピュータが文章を認識する?

・・・ことはできない

- 最尤な単語をskip-gramで予想して並べていけばそれっぽい文は作れるけど、たぶん無意味な文ができる
    - マルコフ連鎖ジェネレータのようなもの
- 単純な埋め込みには限界
    - 語順に関する情報は、完全にはない
    - 文脈依存な情報を持っていない
        - 同音異義語に1つのベクトル$\rightarrow$区別してない
            - 例: チンチラ（げっ歯類にも猫にもいる）

![bg right:20% 100%](./figs/Chinchilla.jpg)


<span style="font-size:70%">
<a href="https://commons.wikimedia.org/wiki/Chinchilla_lanigera#/media/File:Chinchilla_lanigera_(Wroclaw_zoo)-2.JPG">写真上 by Guérin Nicolas（CC BY-SA 3.0）</a>
<a href="https://commons.wikimedia.org/wiki/File:Chinchilla_cat_(3228221937).jpg">写真下 by allen watkin（CC BY-SA 2.0）</a>

---

### どうすればいいか?

- 埋め込みに語順と文脈の情報を付加してやるとよい
    - 前ページのスライドを逆に考えると、そういうことになる
- <span style="color:red">Transformer</span>（のエンコーダ）
    - 入力: 埋め込みに位置情報を加えて変更したもの
    - 出力: <span style="color:red">文脈化トークン埋め込み</span>
        - 各単語の関係性（文脈）に応じて各ベクトルの位置を変更
        - 次の単語の予測などにより有用な埋め込み（使い方はあとで）

![w:1100](./figs/add_context_embedding.png)

---

## Transformerのエンコーダ: 入力


- 入力: 文
    - トークン（単語をより細かく文を区切ったもの）に分けて、
    埋め込みのベクトルに変換
        - $E=[\boldsymbol{e}_{w_1}\ \boldsymbol{e}_{w_2}\ \dots\ \boldsymbol{e}_{w_N}]^\top$という行列に
- 文への位置情報の付加
    - $H = \sqrt{D}E + P = [\boldsymbol{h}_{w_1}\ \boldsymbol{h}_{w_2}\ \dots\ \boldsymbol{h}_{w_N}]^\top$という行列$H$を作成
       - $D$: ベクトルの次元（正規化のため）
       - $P$にはトークンが文の何番目にあるかの情報が入る
           - 単純に「何番目か」ではなく三角関数を使ったややこしもの

<center>とりあえずこれで入力に位置情報が加わる</center>

---

### Transformerのエンコーダ: 文脈情報の付加1

- <span style="color:red">自己注意機構</span>という仕組みで文脈の情報を付加
    - 行列$W_\text{q}, W_\text{k}, W_\text{v}$という3つの行列を使う
        - これらの行列は学習の対象で、ここでは学習が済んでいると仮定
    - $H$のなかのベクトル$\boldsymbol{h}_i$に対して次のベクトルを作成
        - $\boldsymbol{k}_i = W_\text{k}\boldsymbol{h}_i$（キー埋め込み）
        - $\boldsymbol{v}_i = W_\text{v}\boldsymbol{h}_i$（バリュー埋め込み）
        - $\boldsymbol{q}_i = W_\text{q}\boldsymbol{h}_i$（クエリ埋め込み）
    - 3つのベクトルを使う自己注意機構なので特に
    「キー・クエリ・バリュー注意機構」と呼ばれる方法（次のスライドに続く）


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

---

### Transformerのエンコーダ: 文脈情報の付加3

- $\boldsymbol{o}_i$をフィードフォワード層に通す
    - このあと2層のニューラルネットワークを通ってさらに文脈が強化された文脈化トークン埋め込みに

- 全体で$O=[\boldsymbol{o}_{w_1}\ \boldsymbol{o}_{w_2}\ \dots\ \boldsymbol{o}_{w_N}]^\top$という行列が出力される

---

## エンコーダの出力を使った翻訳

- 問題の定式化: 条件付き確率の問題にする（例: 日本語から英語への翻訳）
    - 問題1: 先頭のトークンを選ぶ
        - $p(w_1 |$私 は 昼 に 牛丼 を 食べ まし た 。$)$
    - 問題2: 2番目のトークンを選ぶ
        - $p(w_2 |$私 は 昼 に 牛丼 を 食べ まし た 。I$)$
    - 問題3: 3番目のトークンを選ぶ
        - $p(w_3 |$私 は 昼 に 牛丼 を 食べ まし た 。I ate$)$
- Transformerのデコーダがこれを解くための埋め込みを作る

<center>学習はともかくどうやって計算するの?</center>

---

### <span style="color:red">交差注意機構</span>

- デコーダが持つ
- 自己注意機構の計算方法はそのままで、一部エンコーダの出力を使用
    - クエリ埋め込み$\boldsymbol{q}_i = W_\text{q}\boldsymbol{h}_i$だけエンコーダの埋め込みから計算
        - 前ページの例の場合: 「私は昼に牛丼を食べました。」
        の文脈化トークン埋め込み
    - キー埋め込み、バリュー埋め込みは、デコーダ側の自己注意機構で計算

<center>これで翻訳前の文の文脈を翻訳に反映できる</center>

---

## Vision Transformer (ViT）

---

## まとめ

- 埋め込み
    - 次元の高いベクトルで、単語やトークンの様々な関係性を表現可能
    - skip-gramなどの学習方法で実用性のある埋め込みが作成可能
- Transformer
    - 埋め込みに文脈を反映させる仕組み
