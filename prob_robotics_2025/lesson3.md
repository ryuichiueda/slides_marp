---
marp: true
---

<!-- footer: 確率ロボティクス第3回 -->

# 確率ロボティクス第3回: 期待値

千葉工業大学 上田 隆一

<br />

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 今回の内容

- 期待値
- 期待値を使った計算

---

## 期待値

- （雑な）定義: なにかばらつく値の平均値を推定、予想した値
- 問題: 3700円を払い、サイコロの出目に1000をかけただけお金がかえってくるギャンブルがありますが、1回の試行で儲かるお金の期待値は？
    - 答え
        * $1000/6 + 1000\cdot 2/6 + 1000\cdot 3/6 + 1000\cdot 4/6$
$+ 1000 \cdot 5/6 + 1000 \cdot 6/6 - 3700 = 1000(3.5) - 3700$ <span style="color:red">$= -200$</span>

---

### 日常生活における期待値の意義

- 何かを決めたらどれだけ見返りが戻ってくるかを勘ではなく数値で考えられる
    - しかも確率的な事象に対して
- （釘をさしておくと）物事を雑に単純化して期待値で考えてはいけない
    - 例
        - 宝くじは期待値が掛金の半分だが現に何億円を手にする人がいる
        - 「期待値最大で生きる」と言って講義の単位だけ狙っていたら何も身に付かなかった


---

### ロボティクスでの期待値の意義

- 行動を決める際に計算に出てくる
    - ある時刻に選べる行動は1つ$\rightarrow$あらゆる可能性を1つの数値に集約
- 他、計算の過程でたくさん出てくる（今日やります）

---

### 期待値の計算

- $\Pr$表記
    - 期待値 = $\text{Pr}\{$A$\}f($A$) + \text{Pr}\{$B$\}f($B$) + \cdots \text{Pr}\{$E$\}f($E$)$
        - 事象A, B, C, ..., Eが互いに排反で、A〜Eでない事象の起こる確率が0
            - $f$: 事象に対してお金などの数値を決める関数
- 確率変数を使った表記
    - $\langle f \rangle_P = \sum_{x=-\infty}^{x=\infty}f(x)P(x)$
        - $\text{E}_P(f)$などの表記もあり
            - $P$が省略されていて混乱することがあるので注意

---

- 平均値も期待値
    - $f$を何にするとよいでしょうか？
- 他、計算上の様々な性質、テクニックがありますがそれはまた今度

---

### 時間が余ったときの問題

- [3つのサイコロのうち2つ以上が揃う確率](https://b.ueda.tech/?page=robot_and_stats_questions#%E7%A2%BA%E7%8E%87%E3%81%AE%E9%9B%91%E5%A4%9A%E3%81%AA%E5%95%8F%E9%A1%8C1)
- 上の問題について、3つのサイコロが揃うと1万円、2つのサイコロが揃うと千円もらえるとしたら、掛け金はいくらまで支払いますか?

---

## まとめ

- 確率と期待値を勉強
- 期待値があると意思決定ができる（すべての意思決定ができるわけではない）


---

## 2.3.3 期待値

- 期待値: 無限にセンサ値をドローしたときの平均値
    - $\langle z \rangle_{P(z)}$、$\langle z \rangle_{p(z)}$と表現
    - 実際にドローしなくても計算可能
        - $\langle z \rangle_{P(z)} = \sum_{-\infty}^{\infty} zP(z)$（サイコロで計算してみまし>ょう）
        - $\langle z \rangle_{p(z)} = \int_{-\infty}^{\infty} zp(z) dz$<br />　
- 一般化した期待値
    - $z$が$p(z)$に従うとき、$f(z)$の値はどうなる？
    - $\langle f(z) \rangle_{p(z)} = \int_{-\infty}^{\infty} f(z)p(z) dz$<br />　

---

## 期待値の性質

- 期待値の性質
    - 線形性
        - $\big\langle f(z) + \alpha g(z) \big\rangle_{p(z)} = \big\langle f(z) \big\rangle_{p(z)} + \alpha \big\langle g(z) \big\rangle_{p(z)}$
        - $\big\langle f(z) + \alpha \big\rangle_{p(z)} = \big\langle f(z) \big\rangle_{p(z)} + \alpha \big\langle 1 \big\rangle_{p(z)} = \big\langle f(z) \big\rangle_{p(z)} + \alpha$
    - 平均値
        - $\langle z \rangle_{p(z)} = \mu$、$\langle z - \mu \rangle_{p(z)} = 0$
    - 分散
        - $\langle (z - \mu)^2 \rangle_{p(z)} = \sigma^2$<br />　
- その他、各確率モデルには期待値に関する特有の性質があり、計算に利用できる（付録B.2）

