---
marp: true
---

<!-- footer: 確率ロボティクス第4回（その3） -->

# 確率ロボティクス第4回: 連続値と多変量（その3）

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

- 多変量ガウス分布
- 多変量ガウス分布の演算

---

## 多変量ガウス分布

- ガウス分布に従う変数$x_{1:n}$をまとめて1つの多次元のガウス分布で表せる
- 式をまず見せます
	- $\mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}, \Sigma) = \dfrac{1}{\sqrt{(2\pi)^n |\Sigma|}}
	\exp\left\{-\dfrac{1}{2}(\boldsymbol{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu}) \right\}$
        - ここで
	$\boldsymbol{x} = \begin{pmatrix}
		x_1 \\ x_2 \\ \vdots \\ x_n
		\end{pmatrix}, \ 
	\boldsymbol{\mu} = \begin{pmatrix}
		\mu_1 \\ \mu_2 \\ \vdots \\ \mu_n
		\end{pmatrix}, \ 
	\Sigma = \begin{pmatrix}
		\sigma^2_1 & \sigma_{12} & \dots & \sigma_{1n} \\
		\sigma_{12} & \sigma^2_2 & \dots & \sigma_{2n}  \\
		\vdots & \vdots & \ddots & \vdots \\
		\sigma_{1n} & \sigma_{2n} & \dots & \sigma^2_n  \\
	\end{pmatrix}$


---

### 分散共分散行列

- 前ページの$\Sigma$: 各変数の分散と共分散を組み合わせた行列
    - $\Sigma = \begin{pmatrix}
		\sigma^2_1 & \sigma_{12} & \dots & \sigma_{1n} \\
		\sigma_{12} & \sigma^2_2 & \dots & \sigma_{2n}  \\
		\vdots & \vdots & \ddots & \vdots \\
		\sigma_{1n} & \sigma_{2n} & \dots & \sigma^2_n  \\
	\end{pmatrix}$
         - $\sigma_{ij} = \big\langle (x_i - \mu_i )(x_j-\mu_j) \big\rangle_{\mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}, \Sigma)}$
- 普通に話す時は「共分散行列」でよい

---

### 例: 移動ロボットの実験

- 実験で得られたデータのうち、$x$と$y$について多変量ガウス分布（2次元ガウス分布）に当てはめてみましょう
- [20試行分のデータ](./misc/xy_data.txt)
    - 1列目: $x$[m]、2列目: $y$[m]
- 計算すべきパラメータ
    - $x, y$それぞれの平均値と分散
    - $x$と$y$の共分散
        - <span style="color:red">データからの共分散の計算方法</span>: $s_{ab} = \dfrac{1}{N-1}\sum_{i=1}^n (a_i - \bar{a})(b_i - \bar{b})$
	        - $N$個のデータのペア$(a,b)_{1:N}$に対して


![bg right:30% 95%](./figs/robot_final_pos_b.png)

---

### 計算結果

- `datamash`を使った例
```bash
### 平均値 ###
$ cat xy_data.txt | tr ' ' \\t | datamash mean 1 mean 2
3.8822	0.51035
### 分散 ###
$ cat xy_data.txt | tr ' ' \\t | datamash svar 1 svar 2
0.016455957894737	0.19727097631579
### 共分散 ###
$ cat xy_data.txt |tr ' ' \\t | datamash scov 1:2
-0.029138231578947
```
- これらの値からガウス分布の式を書きましょう

---

### 答え

- $\mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}, \Sigma) = \dfrac{1}{\sqrt{(2\pi)^2 |\Sigma|}}
\exp\left\{-\dfrac{1}{2}(\boldsymbol{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu}) \right\}$
    - $\Sigma 
	= \begin{pmatrix} 
		0.016 & -0.029 \\
		-0.029 & 0.197 \\
	\end{pmatrix},
	\boldsymbol{\mu} 
	= \begin{pmatrix}
		3.88 \\
		0.51 
	\end{pmatrix}$
- 式はわかったけど解釈がよくわからない
    - グラフを描いてみましょう

---

### 2変量ガウス分布の描画

- とりあえず中心からマハラノビス距離$n$になる箇所を描いてみましょう
	- マハラノビス距離: $D_\text{M}(\boldsymbol{x}) = \sqrt{
	(\boldsymbol{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu})}$
	    - 1次元のものと比較を 
- 図形は楕円に
    - 楕円の式: $\dfrac{(x - \mu_x)^2}{a^2} + \dfrac{(y - \mu_y)^2}{b^2} = 1$
	    - $(\boldsymbol{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu})$の部分を多項式にすると同じ形に（次のページから検証）

![bg right:30% 95%](./figs/2d_gauss_draw_question.png)

---

### とりあえず対角化

- 次のように$\Sigma$を分解
    - $\Sigma = R(-\theta)^\top S R(-\theta)$
        - $R(\theta) = 
	\begin{pmatrix}
		\cos\theta & -\sin\theta \\
		\sin\theta & \cos\theta 
	\end{pmatrix}$: 回転行列
        - $S =
	\begin{pmatrix}
		\sigma_a^2 & 0 \\
		0 & \sigma_b^2  \\
	\end{pmatrix}
	= \text{diag}(\sigma_a^2, \sigma_b^2)$: 対角行列
- このとき
    - $D_\text{M}(\boldsymbol{x}) 
	= \sqrt{
		(\boldsymbol{x} - \boldsymbol{\mu})^\top \{
			R(-\theta)^\top S R(-\theta)
		\}^{-1} (\boldsymbol{x} - \boldsymbol{\mu})
	}$
	$=
	 \sqrt{
		(\boldsymbol{x} - \boldsymbol{\mu})^\top 
			R(-\theta)^{-1} S^{-1} \{R(-\theta)^{\top}\}^{-1}
		 (\boldsymbol{x} - \boldsymbol{\mu})
	}$
	$=
	 \sqrt{
		(\boldsymbol{x} - \boldsymbol{\mu})^\top 
			R(-\theta)^{\top} S^{-1}R(-\theta)
		 (\boldsymbol{x} - \boldsymbol{\mu})
	}$
	$=
	 \sqrt{
		 \{R(-\theta)(\boldsymbol{x} - \boldsymbol{\mu})\}^\top 
			S^{-1} \{ R(-\theta)
		 (\boldsymbol{x} - \boldsymbol{\mu}) \}
	 }$

---

### 座標変換

- 前ページ最後の式: $D_\text{M}(\boldsymbol{x}) =
	 \sqrt{
		 \{R(-\theta)(\boldsymbol{x} - \boldsymbol{\mu})\}^\top 
			S^{-1} \{ R(-\theta)
		 (\boldsymbol{x} - \boldsymbol{\mu}) \}
	 }$
- 次を代入すると$D_\text{M}(\boldsymbol{x}) = \sqrt{ a^2/\sigma_a^2 + b^2 / \sigma_b^2}$ となる
    - $\boldsymbol{a} = (a \ \ b)^\top = R(-\theta)(\boldsymbol{x} - \boldsymbol{\mu})$
    - $S = \text{diag}(\sigma_a^2, \sigma_b^2)$
- したがって
    - マハラノビス距離が$n$になる点の描く図形:
    $ab$-座標系で$\dfrac{a^2}{\sigma_a^2} + \dfrac{b^2}{\sigma_b^2} = n^2$を満たす楕円


---

### 座標を戻す

- $ab$-座標系で$\dfrac{a^2}{\sigma_a^2} + \dfrac{b^2}{\sigma_b^2} = n^2$を満たす楕円を$xy$-座標系に
    - $\boldsymbol{a} = (a \ \ b)^\top = R(-\theta)(\boldsymbol{x} - \boldsymbol{\mu})$
- $\theta$だけ回転して$\mu$だけ移動

$\qquad\qquad\qquad$![w:700](./figs/ellipse.png)

---

### 実際の値で描画

- $\Sigma = \begin{pmatrix} 
		0.016 & -0.029 \\
		-0.029 & 0.197 \\
	\end{pmatrix}$
    $= R(-8.9$deg$)
    \begin{pmatrix}
        0.107^2 & 0 \\
        0 & 0.449^2 \\
    \end{pmatrix}R(-8.9$deg$)$
	$\boldsymbol{\mu} 
	= \begin{pmatrix}
		3.88 \\
		0.51 
	\end{pmatrix}$
- 右図: $n=1,2,3$の楕円を描画
    - <span style="color:red">誤差楕円</span>と呼ばれる

![bg right:30% 95%](./figs/robot_final_pos_ellipse.png)

---

## 多変量ガウス分布の演算

- 再生性はあるのか


---

### 再生性・線形変換

- 例1: $\boldsymbol{x}_i \sim \mathcal{N}(\boldsymbol{\mu}_i, \Sigma_i)\ (i=1,2)$のとき、$\boldsymbol{x} = \boldsymbol{x}_1 + \boldsymbol{x}_2$の分布は？
    - $\boldsymbol{x}_1, \boldsymbol{x}_2$は独立
    - 答え（1次元のときから類推して書いてみましょう）: 
        * $\boldsymbol{x} \sim \mathcal{N}(\boldsymbol{\mu}_1 + \boldsymbol{\mu}_2,  \Sigma_1 + \Sigma_2)$
    - 詳解確率ロボティクスに導出例あり
- 例2: $\boldsymbol{x} \sim \mathcal{N}(\boldsymbol{\mu}, \Sigma)$のとき、$\boldsymbol{y} = A\boldsymbol{x} + \boldsymbol{b}$の分布は？
    - 答え（これは次のページで扱います）: 
	    * $\boldsymbol{y} \sim \mathcal{N}(A\boldsymbol{\mu} +\boldsymbol{b}, A\Sigma A^\top )$
	        - $A\Sigma A^\top$: この形はよく出てくる

---

### ガウス分布の線形変換

- $\boldsymbol{x}$の座標系から$\boldsymbol{y} = A \boldsymbol{x} + \boldsymbol{b}$の座標系に変換するとき、空間が$|\det(A)|$だけ引き伸ばされる[[杉浦1985]](https://www.utp.or.jp/book/b302043.html)
    - 下図の緑色の部分の面積比が$1:|\det(A)|$
        - 補足: $|\det(A)|$は$A$の行列式の絶対値
        （$||A||$と書くとややこしいのでこう表記）
![w:600](https://upload.wikimedia.org/wikipedia/commons/3/34/DeterminantOfMatrix.png)
<span style="font-size:50%">[（画像: CC0）](https://commons.wikimedia.org/wiki/File:DeterminantOfMatrix.png)</span>

---

### ガウス分布の線形変換（続き）

- 空間が$|\det(A)|$引き伸ばされると密度は$1/|\det(A)|$だけ薄まる
    - $p(\boldsymbol{y}) = \mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}, \Sigma ) \big/ |\det(A)|$
$= \mathcal{N}\big[ A^{-1}(\boldsymbol{y} - \boldsymbol{b}) | \boldsymbol{\mu}, \Sigma \big] \big/ |\det(A)|$
$= \frac{1}{\sqrt{(2\pi)^n |\Sigma| |A|^2}}
\cdot\exp\left\{
		-\frac{1}{2}\left[  A^{-1}(\boldsymbol{y} - \boldsymbol{b}) - \boldsymbol{\mu} \right]^T \Sigma^{-1} \left[  A^{-1}(\boldsymbol{y} - \boldsymbol{b}) - \boldsymbol{\mu}\right] 
		\right\}$
        - 指数部の外にある$|\Sigma| |A|^2$について$|\Sigma||A|^2 = |A| |\Sigma| |A^\top|= |A\Sigma A^\top|$
        - 指数部の括弧内$= -\frac{1}{2}  \left[
		A^{-1} ( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )
		\right]^\top \Sigma^{-1} A^{-1} ( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )$
	$= -\frac{1}{2}
		( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )^\top 
		(A^{-1})^\top \Sigma^{-1} A^{-1} ( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )$
	$= -\frac{1}{2}
		( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )^\top 
		(A \Sigma A^\top )^{-1}
        ( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )$

$\Longrightarrow p(\boldsymbol{y}) = \mathcal{N}(\boldsymbol{y} | A\boldsymbol{\mu} + \boldsymbol{b}, A\Sigma A^\top)$

---

### 多変量ガウス分布の積

- 問題: 
$p(\boldsymbol{x}) = \eta \mathcal{N}(\boldsymbol{a} | A\boldsymbol{x} + \boldsymbol{b}, sB) \mathcal{N}(\boldsymbol{x} | \boldsymbol{c}, sC)$はどんな分布になるか
- 講義の後半に出てくる形
    - 解き方: ひたすら式変形
    - 後半のための要望: $s$は$\eta$に組み入れないで
    - $s > 0$

---

### 多変量ガウス分布の積（解答）

- まず展開$\mathcal{N}$を数式にして整理
    - $p(\boldsymbol{x}) = \eta 
	\dfrac{1}{\sqrt{(2\pi)^k |sB| }}
	\dfrac{1}{\sqrt{(2\pi)^\ell |sC| }}$
	$\cdot \exp\Big\{
		-\dfrac{1}{2s}(\boldsymbol{a} - A\boldsymbol{x} - \boldsymbol{b})^\top B^{-1} (\boldsymbol{a} - A\boldsymbol{x} - \boldsymbol{b})
		-\dfrac{1}{2s}(\boldsymbol{x} - \boldsymbol{c})^\top C^{-1}(\boldsymbol{x} - \boldsymbol{c})
		\Big\}$ 
	$= \dfrac{\eta}{s}
	\exp\Big\{ -\dfrac{1}{2s} L(\boldsymbol{x}) \Big\}$
        - ここで$L(\boldsymbol{x})$は指数部に$-2s$をかけたもの

---

### 多変量ガウス分布の積（解答・つづき）


- $L$を整理
	- $L(\boldsymbol{x}) = (A\boldsymbol{x})^\top B^{-1}(A\boldsymbol{x}) + \boldsymbol{x}^\top C^{-1}\boldsymbol{x}$
	$\qquad\quad - (A\boldsymbol{x})^\top B^{-1}(\boldsymbol{a}- \boldsymbol{b} ) - \boldsymbol{x}^\top C^{-1}\boldsymbol{c}$
	$\qquad\quad - (\boldsymbol{a}- \boldsymbol{b} )^\top B^{-1} (A\boldsymbol{x}) - \boldsymbol{c}^\top C^{-1} \boldsymbol{x} + U'$
        - $U'$は$\boldsymbol{x}$と関係のない項
- $(XY)^\top = Y^\top X^\top$、共分散行列が対称行列という性質を使うと
	- $L(\boldsymbol{x}) = (A\boldsymbol{x})^\top B^{-1}(A\boldsymbol{x}) + \boldsymbol{x}^\top C^{-1}\boldsymbol{x}$
	$\qquad\quad - 2(A\boldsymbol{x})^\top B^{-1}(\boldsymbol{a}- \boldsymbol{b} ) - 2\boldsymbol{x}^\top C^{-1}\boldsymbol{c} + U'$
	$\qquad = \boldsymbol{x}^\top(A^\top B^{-1} A + C^{-1})\boldsymbol{x}- 2\boldsymbol{x}^\top \left\{ A^\top B^{-1}(\boldsymbol{a}- \boldsymbol{b} ) + C^{-1}\boldsymbol{c} \right\} + U'$

---

### 多変量ガウス分布の積（解答・つづき）

- 前ページ最後の行について、次のようにおく
    - $D^{-1} = A^\top B^{-1} A + C^{-1}$
    - $\boldsymbol{d} = D \left\{ A^\top B^{-1}(\boldsymbol{a}- \boldsymbol{b} ) + C^{-1}\boldsymbol{c} \right\}$
- $L(\boldsymbol{x}) = \boldsymbol{x}^\top D^{-1} \boldsymbol{x} - 2\boldsymbol{x}^\top D^{-1}\boldsymbol{d} +U'$
	$\qquad = ( \boldsymbol{x} - \boldsymbol{d} )^\top D^{-1} ( \boldsymbol{x} - \boldsymbol{d} ) - \boldsymbol{d}^\top D^{-1} \boldsymbol{d} + U'$
	$\qquad = ( \boldsymbol{x} - \boldsymbol{d} )^\top D^{-1} ( \boldsymbol{x} - \boldsymbol{d} ) + U$
- $L$を指数部に戻す
	- $p(\boldsymbol{x}) = \frac{\eta}{s}
	\exp\Big\{ -\frac{1}{2s} 
	( \boldsymbol{x} - \boldsymbol{d} )^\top D^{-1} ( \boldsymbol{x} - \boldsymbol{d} ) 
    \Big\} \cdot \exp \left( - \frac{1}{2s} U \right)$
	$= \frac{\eta}{s^{1/2}} \frac{1}{\sqrt{(2\pi)^\ell |sD|}} \exp \left\{
		-\frac{1}{2s}( \boldsymbol{x} - \boldsymbol{d} )^\top D^{-1} ( \boldsymbol{x} - \boldsymbol{d} ) \right\}
	\cdot e^{ - U/2s}$
	$= \eta s^{-1/2}e^{-U/2s}
	\mathcal{N}(\boldsymbol{x} | \boldsymbol{d} , sD)$

---

### 多変量ガウス分布の積（まとめ）

- 問題: $p(\boldsymbol{x}) = \eta \mathcal{N}(\boldsymbol{a} | A\boldsymbol{x} + \boldsymbol{b}, sB) \mathcal{N}(\boldsymbol{x} | \boldsymbol{c}, sC)$はどんな分布になるか
- 答え: $p(\boldsymbol{x}) = \frac{\eta}{s}= \eta s^{-1/2}e^{-U/2s}
	\mathcal{N}(\boldsymbol{x} | \boldsymbol{d} , sD)$
        - $U = (\boldsymbol{a} - \boldsymbol{b})^\top B^{-1}(\boldsymbol{a} - \boldsymbol{b}) + \boldsymbol{c}^\top C^{-1} \boldsymbol{c} - \boldsymbol{d}^\top D^{-1} \boldsymbol{d}$

ということでガウス分布になる（どう使うかは講義の後半に期待）
