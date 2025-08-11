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

### 期待値の定義

- 期待値 = $\text{Pr}\{$A$\}f($A$) + \text{Pr}\{$B$\}f($B$) + \cdots \text{Pr}\{$E$\}f($E$)$
    - 事象A, B, C, ..., Eが互いに排反で、A〜Eでない事象の起こる確率が0
        - $f$: 事象に対してお金などの数値を決める関数
- 確率変数を使った表記
    - $\langle f \rangle_P = \sum_{x=-\infty}^{x=\infty}f(x)P(x)$
        - $\langle f(x) \rangle_{P(x)}$と表記することも
    - $\text{E}_P(f)$などの表記もあり
        - $P$が省略されていて混乱することがあるので注意

---

### 期待値の線形性

- 問題: 100円を払ってサイコロをふったら、AさんとBさんが次のように
お金をくれる（むしられる）場合の期待値を考えましょう
    - Aさんが出目$\times 100$円
    - Bさんが$(10-$出目の2乗$)\times 100$円

<center>計算したら次のページにどうぞ</center>

---

### 答え

- 出目の確率分布: $P(x) = 1/6$
- 出目を$x$としたときにもらえるお金の関数
    - $f(x) = -100 + 100x + 100(10-x^2) = 900 + 100x - 100x^2$
- 計算
    - $\langle f \rangle_P = \sum_{x=1}^6 (900 + 100x - 100x^2)/6$
    <span style="color:red">$= 900 + 100 \cdot \dfrac{1}{6}\sum_{x=1}^6 x - 100 \cdot \dfrac{1}{6}\sum_{x=1}^6 x^2$</span>
    $= 900 + 100 \cdot 3.5 - 100 \cdot (1+4+9+16+25+36)/6$
    $= 900 + 350 - 100 \cdot 91/6 \approx -267$円

---

### 前ページの例の一般化

- $x \sim P$のとき、$f(x) = w_0 + w_1 g_1(x) + \dots + w_n g_n(x)$の期待値は？
    -$g_0(x) = 1$とすると$f(x) = \sum_{i=0}^n w_i g_i(x)$
    - 前ページの例:
        - $g_1(x)=x, g_2(x)=x^2$
        - $w_0=w_1=100, w_2=-100$
- 答え
    * $\langle f \rangle_P = \sum_{i=0}^n w_i g_i(x)$

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


---

- 平均値も期待値
    - $f$を何にするとよいでしょうか？
- 他、計算上の様々な性質、テクニックがありますがそれはまた今度

