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
- 期待値の計算、期待値を使った計算

<center>ひたすら計算の回です</center>

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
            - 変数が分からないと都合が悪い場合
        - $\text{E}_P(f)$などの表記もあり
            - $P$が省略されていて混乱することがあるので注意

---

### 確率分布と期待値

- 確率分布の平均値と分散は期待値で表現できる
- その前におさらい: データ$x_{1:N}$の平均値と分散
    - $\bar{x}_{1:N} = \dfrac{x_1 + x_2 + \dots + x_N}{N} = \dfrac{1}{N} \sum_{i=1}^N x_i$
    - $s^2 = \dfrac{1}{N-1}\sum_{i=1}^{N} ( x_i - \bar{x})^2$
- $x_{1:n} \sim P$だとすると
    - 平均値: $P$から値を無限に取り出した時の期待値
        - $\mu = \langle x \rangle_{P(x)}$
    - 分散: $P$から値を無限に取り出した時の平均値との差の2乗の期待値
        - $\sigma^2 = \langle (x - \mu)^2\rangle_{P(x)}$
            - 補足: $N-1$で割る必要はないのかどうかの話は後々

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
    - 前ページの例:
        - $g_1(x)=x, g_2(x)=x^2$
        - $w_0=w_1=100, w_2=-100$
- 答え
    * $\langle f \rangle_P = \sum_{x=-\infty}^\infty P(x)f(x)$
    $= \sum_{x=-\infty}^\infty \{ w_0P(x) + w_1P(x)g_1(x) + \cdots + w_nP(x)g_n(x) \}$
    $= w_0 \sum_{x=-\infty}^\infty P(x) + w_1 \sum_{x=-\infty}^\infty P(x)g_1(x) + \cdots + w_n\sum_{x=-\infty}^\infty P(x)g_n(x)$
    $= w_0 \langle 1 \rangle_P + w_1 \langle g_1 \rangle_P+ \cdots + w_n \langle g_n \rangle_P$
* <span style="color:red">ある関数$f$の期待値=$f$の各項の期待値の和</span>
    - これを「期待値の線形性」と呼ぶ

---

### 線形性の利用の例: 分散の計算

- 確率分布$P$に対する分散の式の簡略化
    - $\sigma^2 = \langle (x - \mu)^2\rangle_{P(x)}$
        - 線形性を使って分解してみましょう
- 答え
    * $\sigma^2 = \langle x^2 -2 x\mu + \mu^2\rangle_{P(x)}$
    $= \langle x^2 \rangle_{P(x)} -2 \mu \langle x\rangle_{P(x)} + \mu^2 \langle 1 \rangle_{P(x)}$
    $= \langle x^2 \rangle_{P(x)} -2 \mu \mu + \mu^2$
    $= \langle x^2 \rangle_{P(x)} - \mu^2$


---

### 期待値の他の性質1


- $\big\langle f(x) \big\rangle_{P(x,y)} = \big\langle f(x) \big\rangle_{P(x)}$
    - なんででしょう？
- 答え（周辺化の式から）
    * $\big\langle f(x) \big\rangle_{P(x,y)}= \sum_{x=-\infty}^\infty \sum_{y=-\infty}^\infty f(x) P(x,y)$
	$= \sum_{x=-\infty}^\infty f(x) \sum_{y=-\infty}^\infty P(x,y)$
	$= \sum_{x=-\infty}^\infty f(x) P(x)$
    $= \big\langle f(x) \big\rangle_{P(x)}$

---

### 期待値の他の性質2

- $\big\langle \langle h(x,y) \rangle_{P(y)} \big\rangle_{P(x)} = \big\langle h(x,y) \big\rangle_{P(x)P(y)}$
    - なんででしょう？
- 答え
    * $\sum_{x=-\infty}^\infty P(x) \sum_{y=-\infty}^\infty  h(x,y) P(y)$
    $= \sum_{x=-\infty}^\infty \sum_{y=-\infty}^\infty  h(x,y) P(x)P(y)$

---

### 期待値の他の性質3

- $\big\langle f(x)g(y) \big\rangle_{P(x)P(y)} = \big\langle f(x) \big\rangle_{P(x)} \big\langle g(y) \big\rangle_{P(y)}$
    - $\Sigma$を使わず導出してみましょう
	    * 左辺$=\big\langle \langle f(x)g(y)\rangle_{P(x)} \big\rangle_{P(y)}$（性質2から）
        $= \big\langle \langle f(x)\rangle_{P(x)}g(y) \big\rangle_{P(y)}$（$x$と無関係な部分を内側の$\langle\rangle$の外に）
        $= \big\langle f(x) \big\rangle_{P(x)} \big\langle g(y) \big\rangle_{P(y)}$（$y$と無関係な部分を外側の$\langle\rangle$の外に）

---

## 期待値を利用した計算

---

### 周辺化の式の簡略化

- $P(x) = \langle P(x|y) \rangle_{P(y)}$
    - 導出
        * $P(x) = \sum_{y=-\infty}^\infty P(x,y) = \sum_{y=-\infty}^\infty P(x|y)P(y) = \langle P(x|y) \rangle_{P(y)}$
    - $\Sigma$や$\infty$を書く必要がなく便利

---

### ふたつの変数の和の分散

- 確率変数$x$と$y$の和$(x+y)$の分散を計算してみましょう
	- <span style="color:red">共分散</span> $\sigma_{xy} = \big\langle (x- \mu_x )(y-\mu_y) \big\rangle_{P(x,y)}$を使って簡略化を
        - 共分散がなんなのかについては次ページ以降
- 答え
    * $\sigma_{x+y}^2 = \left\langle \left\{ (x+y) - (\mu_x + \mu_y )\right\}^2 \right\rangle_{P(x,y)}$
	$= \langle (x- \mu_x )^2 \rangle_{P(x,y)} + \langle (y- \mu_y )^2 \rangle_{P(x,y)} + 2 \big\langle (x- \mu_x )(y-\mu_y) \big\rangle_{P(x,y)}$
	$= \langle (x- \mu_x )^2 \rangle_{P(x)} + \langle (y- \mu_y )^2 \rangle_{P(y)} + 2 \sigma_{xy}$
	（$\uparrow$p.12から）
	$= \sigma_x^2 + \sigma_y^2 + 2 \sigma_{xy}$
- それぞれの分散を足して、さらに$2\times$共分散を足す

---

### 共分散

- $\sigma_{xy} = \big\langle (x- \mu_x )(y-\mu_y) \big\rangle_{P(x,y)}$
    - $\langle\  \rangle$の中
        - $x$と$y$がそれぞれの平均を上回ると正
        - 片方が上回って片方が下回ると負
    $\rightarrow$正負で$x$と$y$の相関関係が分かる
- 相関係数（各自調査を）とは異なるので注意


---

### 共分散の式の簡略化

- $\sigma_{xy} = \big\langle (x- \mu_x )(y-\mu_y) \big\rangle_{P(x,y)}$を分解して整理してみましょう
- 答え
	* $\sigma_{xy} =  \big\langle xy - x\mu_y - y\mu_x + \mu_x \mu_y  \big\rangle_{P(x,y)}$
	$= \big\langle xy  \big\rangle_{P(x,y)} - \big\langle x  \big\rangle_{P(x,y)}\mu_y - \big\langle y  \big\rangle_{P(x,y)}\mu_x + \mu_x \mu_y$
	$= \big\langle xy  \big\rangle_{P(x,y)} - \big\langle x  \big\rangle_{P(x)}\mu_y - \big\langle y  \big\rangle_{P(y)}\mu_x + \mu_x \mu_y$ 
	$= \big\langle xy  \big\rangle_{P(x,y)} - \mu_x\mu_y - \mu_y\mu_x + \mu_x \mu_y$
	$= \big\langle xy  \big\rangle_{P(x,y)} - \mu_x\mu_y$
- この式から次のページの性質が導出できる

---

### $x$と$y$が独立な場合の共分散

- $\sigma_{xy} = \big\langle xy  \big\rangle_{P(x,y)} - \mu_x\mu_y$をさらに整理
- 計算
    * $= \big\langle xy  \big\rangle_{P(x)P(y)} - \mu_x\mu_y= \langle x \rangle_{P(x)} \langle y \rangle_{P(y)} - \mu_x\mu_y = 0$
    （p.14の性質を利用）
$\Longrightarrow$<span style="color:red">$x$と$y$が独立だと共分散が$0$</span>
- 上記性質から導出される式
    - $\sigma^2_{x+y}= \sigma_x^2 + \sigma_y^2 \quad (x \bot\!\!\!\!\bot y)$
        - 独立な変数に対して分散は足し算に（便利な性質）
    - $\sigma^2_{x_1+x_2+\dots+x_n} = \sum_{i=1}^n \sigma^2_i\quad$（$x_{1:n}$が互いに独立 or 独立同分布）

---

### 不偏分散と確率分布の分散の関係（本日のラスボス）

- $x_{1:N} \overset{\text{iid}}{\sim} P$のとき、この2つは一致するか？
    - $s^2 = \dfrac{1}{N-1}\sum_{i=1}^{N} ( x_i - \bar{x})^2$（の期待値）
    - $\sigma^2 = \langle (x - \mu)^2\rangle_{P(x)}$
- 確認してみましょう
	- $s^2$の期待値を$\langle s^2 \rangle_{Q(x_{1:N})} = \left\langle \dfrac{1}{N-1}\sum_{i=1}^{N} ( x_i - \bar{x})^2 \right\rangle_{Q(x_{1:N})}$とおく
        - ここで
            - $Q(x_{1:N})=P(x_1)P(x_2)\dots P(x_N)$
            - $\bar{x} = (\sum_{i=1}^N x_i)/N$
	- $\langle s^2 \rangle_{Q(x_{1:N})}$を変形していきましょう（次ページ）
	    - ヒント: $P(x)$の平均値$\mu$をうまく使います

---

### $\langle s^2 \rangle_{Q(x_{1:N})}$の変形

- $(N-1)\langle s^2 \rangle_{Q(x_{1:N})} = \left\langle \sum_{i=1}^{N} \left\{ (x_i - \mu) + (\mu - \bar{x})\right\}^2  \right\rangle_{Q(x_{1:N})}$
$= \left\langle \sum_{i=1}^{N} (x_i - \mu)^2 + 2(\mu - \bar{x}) \sum_{i=1}^{N} (x_i - \mu) + \sum_{i=1}^{N} (\mu - \bar{x})^2  \right\rangle_{Q(x_{1:N})}$
$= \left\langle \sum_{i=1}^{N} (x_i - \mu)^2 + 2(\mu - \bar{x}) N (\bar{x} - \mu) + N (\mu - \bar{x})^2  \right\rangle_{Q(x_{1:N})}$
$= \left\langle \sum_{i=1}^{N} (x_i - \mu)^2 - N (\mu - \bar{x})^2  \right\rangle_{Q(x_{1:N})}$
$= \sum_{i=1}^{N} \left\langle (x_i - \mu)^2 \right\rangle_{Q(x_{1:N})} - N \left\langle
	(\bar{x} - \mu)^2  \right\rangle_{Q(x_{1:N})}$
$= \sum_{i=1}^{N} \left\langle (x_i - \mu)^2 \right\rangle_{P(x_i)} - N \left\langle 
	\Big( \dfrac{\sum_{i=1}^{N} x_i}{N} - \mu \Big)^2  \right\rangle_{Q(x_{1:N})}$
	（$\uparrow$第1項: p.12の性質にもとづいて余計な変数を除去）

---

### $\langle s^2 \rangle_{Q(x_{1:N})}$の変形（続き）

- $(N-1)\langle s^2 \rangle_{Q(x_{1:N})} = \sum_{i=1}^{N} \left\langle (x_i - \mu)^2 \right\rangle_{P(x_i)} - \dfrac{1}{N} 
	\left\langle \Big( \sum_{i=1}^{N} x_i - N\mu \Big)^2  \right\rangle_{Q(x_{1:N})}$
    - 右辺第1項: $x_1, x_2, \dots, x_N$それぞれの分散を足したもの
    - 右辺第2項: $x_1 + x_2 + \dots + x_N$の分散を$N$で割ったもの
    （p.20の性質が利用可能）
- したがって
    - $(N-1)\langle s^2 \rangle_{Q(x_{1:N})} = N\sigma^2 - N\sigma^2/N = (N-1)\sigma^2$
    $\Longrightarrow$ <span style="color:red">$\langle s^2 \rangle_{Q(x_{1:N})} = \sigma^2$が成立</span>
        - 不偏分散の期待値と分布の期待値が一致
        - 式変形だけでは分からないけど$N-1$で割ることが妥当ということに
