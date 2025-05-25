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

- word2vecというモデル群のなかのひとつ
- 人工ニューラルネットワーク
    - ある単語について、文の左右にある単語を予想させる
    （つまり条件付き確率を求める）
    - 大量の文章から学習
    - 予想できるようになったネットワークの途中の層の重みからベクトルが計算できる

---

### skip-gramの埋め込みでできるもの

- 単語が$w_1, w_2, \dots, w_N$だけあると、それぞれに対応する埋め込みのベクトル
$\boldsymbol{x}_{w_1}, \boldsymbol{x}_{w_2}, \dots, \boldsymbol{x}_{w_N}$ができる
    - 並べると$X=[\boldsymbol{x}_{w_1}\ \boldsymbol{x}_{w_2}\ \dots\ \boldsymbol{x}_{w_N}]^\top$という行列に
- もうひとつ、左右の単語の予測のための行列$U$というものもできる
    - $P(w_j | w_i) = \text{softmax}_{w_j}(U \boldsymbol{x}_{w_i})$
        - ベクトル$U\boldsymbol{x}_{w_i}$: $w_i$に対する各単語の関連性の強さを表す
        - $\text{softmax}$: ソフトマックス関数（強さを確率に正規化する関数）
    - $U=[\boldsymbol{u}_{w_1}\ \boldsymbol{u}_{w_2}\ \dots\ \boldsymbol{u}_{w_N}]^\top$を構成するベクトル$\boldsymbol{u}_{w_j}$も埋め込みのベクトル
        - おそらく双対ベクトルの一種

---

### 埋め込みができて、skip-gramができればコンピュータが文章を認識する?

・・・ことはできない

- 単語をひとつずつskip-gramで予想して並べていけばそれっぽい文は作れるけど、その文は無意味
    - マルコフ連鎖ジェネレータのようなもの
- 単純な埋め込みには限界
    - 語順に関する情報は、完全にはない
    - 同音異義語に1つのベクトルしか与えないので区別不可能
        - 例: チンチラ（げっ歯類のチンチラ/猫のチンチラ）
        - つまり文脈の依存性に関する情報を持っていない

![bg right:20% 100%](./figs/Chinchilla.jpg)


<span style="font-size:70%">
<a href="https://commons.wikimedia.org/wiki/Chinchilla_lanigera#/media/File:Chinchilla_lanigera_(Wroclaw_zoo)-2.JPG">写真上 by Guérin Nicolas（CC BY-SA 3.0）</a>
<a href="https://commons.wikimedia.org/wiki/File:Chinchilla_cat_(3228221937).jpg">写真下 by allen watkin（CC BY-SA 2.0）</a>

---

## どうすればいいか?

- 埋め込みに語順と文脈の情報を付加してやるとよい
    - 前ページのスライドを逆に考えると、そういうことになる
- <span style="color:red">Transformer</span>（のエンコーダ）
    - そのような仕組みで、文の情報を埋め込みに追加
        - 「文脈化トークン埋め込み」を出力


---

### Transformerのエンコーダ（学習済みのものの説明）

- 入力: 文
    - 単語に（実際はもっと細かく）分けて、埋め込みのベクトルに変換
        - $E=[\boldsymbol{e}_{w_1}\ \boldsymbol{e}_{w_2}\ \dots\ \boldsymbol{e}_{w_N}]^\top$という行列に
- 文への位置情報の付加
    - $H = E + P$という行列$H$を作成
       - $P$には単語が文の何番目にあるかの情報が入る
           - 単純に「何番目か」ではなく三角関数を使ったややこしもの

<center>とりあえずこれで入力に位置情報が加わる</center>

---

### 文脈の情報の埋め込み

- 自己注意機構

