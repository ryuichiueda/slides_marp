---
marp: true
---

<!-- footer: 確率ロボティクス第9回 -->

# 確率ロボティクス第9回: カルマンフィルタによる自己位置推定

千葉工業大学 上田 隆一

<p style="font-size:50%">
図の一部は詳解確率ロボティクスから転載しています。
</p>

$$\newcommand{\V}[1]{\boldsymbol{#1}}$$
$$\newcommand{\jump}[1]{[\![#1]\!]}$$
$$\newcommand{\bigjump}[1]{\big[\!\!\big[#1\big]\!\!\big]}$$
$$\newcommand{\Bigjump}[1]{\bigg[\!\!\bigg[#1\bigg]\!\!\bigg]}$$

---

<!-- paginate: true -->


### カルマンフィルタ

- 信念分布をガウス分布に限定したベイズフィルタ
    - 次のベイズフィルタの式をすべてガウス分布の演算に
        - 移動時: $\hat{b}_t(\V{x}) =  \big\langle p(\V{x} | \V{x}', \V{u}_t) \big\rangle_{b_{t-1}(\V{x}')}$ 
        - 観測時: $b_t(\V{x}) = \eta p(\textbf{z}_t | \V{x}) \hat{b}_t(\V{x})$<br />　
- 疑問: なぜガウス分布にこだわるのか？
    - <span style="color:red">計算量が小さい</span>
        - 平均値と共分散行列の演算だけでベイズフィルタを実装可能
        - 状態の次元が高くても適用可能

---

### 自己位置推定への適用

- いろいろ問題がある
    - ガウス分布なので次のような状況で信念が表現しずらい
        - ロボットが壁ぎわにいて、壁の向こうにはいる可能性がない
            - 壁のところで分布を打ち切れない
        - 分布がマルチモーダル
        - 自己位置の情報がない（一様分布）

ということで自己位置推定にはあまり使われないけど、考え方は重要なので計算方法をおさえましょう

---

## 信念分布の表現（詳解6.1節）

- 信念をガウス分布に限定
    - $b_t = \mathcal{N}(\V{\mu}_t, \Sigma_t)$　
- 右図: ロボットの初期姿勢まわりに置いた誤差楕円
    - $XY\theta$空間中の楕円球となる
        - （ユークリッド空間とみなせば）　
    - 以後、次の2要素で描画
        - $XY$平面の$3\sigma$範囲を表す楕円
        - $\theta$方向の$3\sigma$範囲を示す2本の線分

![bg right:30% 100%](./figs/belief_ellipse.png)

---

## 移動後の信念分布の更新（詳解6.2節）

- やること: 移動時のベイズフィルタの式をガウス分布だけの演算に
- ベイズフィルタの式
    - $\hat{b}_t(\V{x}) = \big\langle p(\V{x} | \V{x}', \V{u}_t) \big\rangle_{b_{t-1}(\V{x}')}= \int_{\V{x}' \in \mathcal{X}} p(\V{x} | \V{x}', \V{u}_t) b_{t-1}(\V{x}') d\V{x}'$
        - 疑問1: $p(\V{x} | \V{x}', \V{u}_t)$はガウス分布になるだろうか？
        - 疑問2: $\hat{b}_t$はガウス分布になるだろうか？

---

## 6.2.1 状態遷移モデルの線形化

- 分布$p(\V{x} | \V{x}', \V{u}_t)$がガウス分布にはならない
    - 例: 前章では$\V{u}_t$のばらつきをガウス分布でモデル化したが、そうであってもロボットをまっすぐ走らせるとパーティクルが弓状の分布に
        <img width="30%" src="./figs/simulated_on.png" /><img width="35%" src="./figs/nonliner_motion.jpg" />
- どうするか？$\rightarrow$ むりやりガウス分布に近似
    - 推定姿勢のまわり（信念分布の中心）ほど近似誤差が少ないように
    - 推定の精度を高く保てば問題ないという考え方

---

### 近似の方法（状態遷移関数の線形化）

- 移動後の姿勢$\V{x}_t$の分布がガウス分布になるように、状態方程式を次のような形式に<span style="color:red">線形近似</span>
    - $\V{x}_t = \V{f}(\V{x}_{t-1}, \V{u}_t')$ <span style="color:red">$\approx \V{f}(\V{x}_{t-1}, \V{u}_t) + A_t (\V{u}_t' - \V{u}_t)$</span>
        - $\V{u}_t, \V{u}'_t$: それぞれ制御指令（既知）と真の動き（未知でばらつく）
        - $A_t$: 後述

<center><img width="60%" src="./figs/motion_linerized.jpg" /></center>

<center>速度、角速度の誤差がXYθ空間で等倍に広がる</center>

---

### 行列$A_t$の意味

- $A_t = \dfrac{\partial \V{f}}{\partial \V{u}}\Big|_{\V{x}=\V{x}_{t-1},\V{u}=\V{u}_t}$
    - 近似した状態方程式（再掲）: $\V{x}_t \approx \V{f}(\V{x}_{t-1}, \V{u}_t) + A_t (\V{u}_t' - \V{u}_t)$　
- 解釈
    - <span style="color:red">$\V{x} =\V{x}_{t-1}, \V{u} = \V{u}_t$において、$\V{u}$が少しずれると$\V{f}$がどれだけずれるかを計算したもの</span>
    - $A_t$に$\V{u}'_t - \V{u}$（速度・角速度の誤差）をかけることで、$\V{f}$のズレ（$=XY\theta$空間での$\V{x}_t$の誤差）が計算できる　

---

### 行列$A_t$の計算

- 状態方程式
    - <span style="font-size:90%">$\boldsymbol{f}(\boldsymbol{x}, \boldsymbol{u}) = \begin{pmatrix} x \\ y \\ \theta \end{pmatrix} + \begin{pmatrix} \nu\omega^{-1}\left\{\sin( \theta + \omega \Delta t ) - \sin\theta \right\} \\ \nu\omega^{-1}\left\{-\cos( \theta + \omega \Delta t ) + \cos\theta \right\} \\ \omega \Delta t \end{pmatrix}$</span>
- 状態方程式の偏微分
    - <span style="font-size:70%">$\dfrac{\partial \boldsymbol{f}}{\partial \boldsymbol{u}}=\begin{pmatrix} \partial f_x/\partial \nu & \partial f_x/\partial \omega \\ \partial f_y/\partial \nu & \partial f_y/\partial \omega \\ \partial f_\theta/\partial \nu & \partial f_\theta/\partial \omega \end{pmatrix} \nonumber \\ \hspace{-5em}$
    $= \begin{pmatrix} \omega^{-1}\left\{\sin( \theta + \omega \Delta t ) - \sin\theta \right\} & -\nu\omega^{-2}\left\{\sin( \theta + \omega \Delta t ) - \sin\theta \right\} + \nu\omega^{-1}\Delta t \cos( \theta + \omega \Delta t )  \\ \omega^{-1}\left\{-\cos( \theta + \omega \Delta t ) + \cos\theta \right\} & -\nu\omega^{-2}\left\{-\cos( \theta + \omega \Delta t ) + \cos\theta \right\} + \nu\omega^{-1}\Delta t\sin( \theta + \omega \Delta t ) \\ 0 & \Delta t \end{pmatrix}$</span>

これに$\boldsymbol{x} = \boldsymbol{x}_{t-1}, \boldsymbol{u} = \boldsymbol{u}_t$を代入すると$A_t$が計算できる

---

### 状態遷移モデルの近似

- 次にやること
    - $\V{x}_t \approx \V{f}(\V{x}_{t-1}, \V{u}_t) + A_t (\V{u}_t' - \V{u}_t)$について、$\V{u}'_t$がばらつくときの$\V{x}_t$の分布を求める　
- 分布の式
    - $\V{x}_t \sim \mathcal{N}(\V{x} | \V{\mu}_t , R_t)$
        - $\V{\mu}_t = \V{f}(\V{x}_{t-1}, \V{u}_t)$
        - $R_t$は誤差項$A_t(\V{u}'_t - \V{u}_t)$のばらつきの共分散行列　
- $R_t$の求め方
    - $\nu\omega$空間にある誤差$\V{u}'-\V{u}$の分布を$XY\theta$空間に$A_t$で写像

計算しましょう

---

### $R_t$の計算

1. 制御のばらつきを$\boldsymbol{u}' \sim \mathcal{N}(\boldsymbol{u}, M_t)$でモデル化
    - $M_t = \dfrac{1}{\Delta t}\begin{pmatrix} \sigma^2_{\nu\nu}|\nu_t| + \sigma^2_{\nu\omega}|\omega_t| & 0 \\ 0 & \sigma^2_{\omega\nu}|\nu_t| + \sigma^2_{\omega\omega}|\omega_t| \end{pmatrix}$
        - $\sigma^2_{ab}$: 移動量$b$あたりの$a$の分散
        - <span style="color:red">これはパーティクルフィルタで使ったモデルと同じ</span>
        - すべて分かっている変数で構成される　
2. 共分散行列の定義から
    - $R_t = \left\langle  (\V{x}_t - \V{\mu}_t) (\V{x}_t - \V{\mu}_t)^\top \right\rangle_{\mathcal{N}(\V{u}, M_t)}$
    $= \left\langle A_t (\V{u}'_t - \V{u}_t) \left\{ A_t (\V{u}'_t - \V{u}_t) \right\}^\top \right\rangle_{\mathcal{N}(\V{u}, M_t)}$
    $= A_t  \left\{ \left\langle (\V{u}'_t - \V{u}_t) (\V{u}'_t - \V{u}_t)^\top \right\rangle_{\mathcal{N}(\V{u}, M_t)} \right\} A_t^\top$
	<span style="color:red">$= A_t M_t A_t^\top$</span>
        <span style="font-size:60%">※ 書籍（付録B.1.10）はもう少し回りくどい方法で計算しています。書き直したい・・・</span>

---

## 信念分布の遷移（詳解6.2.2）

- 今まで: 姿勢の状態遷移をガウス分布で近似
    - 点を分布に
- 次やること: 信念分布の状態遷移をガウス分布で近似
    - 分布を分布に　
- 手順
    1. 信念$\ b_{t-1} = \mathcal{N}(\V{\mu}_{t-1}, \Sigma_{t-1} )$を$\hat{b}_t$に遷移する計算式をたてる
        - ベイズフィルタの移動の式$\ \hat{b}_t(\V{x}) = \int_{\V{x}' \in \mathcal{X}} p(\V{x} | \V{x}', \V{u}_t) b_{t-1}(\V{x}') d\V{x}'$で
        - 状態遷移モデル$p(\V{x} | \V{x}_{t-1}, \V{u}_t)$は今作ったガウス分布を利用
    2. $\hat{b}_t$がガウス分布になるように近似の方法を考える　

---

### ガウス分布を代入したベイズフィルタの移動の式

- 代入するガウス分布
    - $p(\V{x} | \V{x}', \V{u}_t) = \mathcal{N}(\V{x} | \V{\mu}_t, R_t)$
    $= \mathcal{N}\left[ \V{f}(\V{x}',\V{u}_t),R_t \right]$
   <span style="color:red">$= \eta \exp\left\{ -\frac{1}{2} \left[\V{x} - \V{f}(\V{x}',\V{u}_t) \right]^\top R_t^{-1} \left[ \V{x} - \V{f}(\V{x}',\V{u}_t) \right] \right\}$</span>
        - $R_t$の逆行列は存在しないがその問題はあとで扱う
    - $b_{t-1}(\V{x}') = \mathcal{N}( \V{x}' | \V{\mu}_{t-1}, \Sigma_{t-1} )$
    <span style="color:red">$= \eta \exp\left\{-\frac{1}{2}(\V{x}' - \V{\mu}_{t-1})^\top \Sigma_{t-1}^{-1} (\V{x}' - \V{\mu}_{t-1})  \right\}$</span>　
- 代入して式を整理
    - $\hat{b}_t(\V{x}) = \eta\int_{\V{x}' \in \mathcal{X}}\exp\big\{ -\frac{1}{2} \big[\V{x} - \V{f}(\V{x}',\V{u}_t) \big]^\top R_t^{-1} \big[ \V{x} - \V{f}(\V{x}',\V{u}_t) \big]$
    $-\frac{1}{2} (\V{x}' - \V{\mu}_{t-1})^\top \Sigma_{t-1}^{-1} (\V{x}' - \V{\mu}_{t-1}) \big\}  d\V{x}'$

$\V{f}$が非線形なので$\hat{b}_t$がガウス分布にならない

---

### $\V{f}$の線形化

- $\hat{b}_t$の積分内の指数部
    - <span style="font-size:75%">$-\dfrac{1}{2} \big[\V{x} - \V{f}(\V{x}',\V{u}_t) \big]^\top R_t^{-1} \big[ \V{x} - \V{f}(\V{x}',\V{u}_t) \big] -\dfrac{1}{2} (\V{x}' - \V{\mu}_{t-1})^\top \Sigma_{t-1}^{-1} (\V{x}' - \V{\mu}_{t-1})$</span>
    - <span style="color:red">$\V{x}'$を非線形な関数$\V{f}$の外に出すと、指数部が$\V{x}'$の分布に対応する多項式と$\V{x}$の分布に対応する多項式に分けることが可能</span>
        - この分離で$\hat{b}_t$がガウス分布に（理由はあとで）　
- 今度は$\V{x}'$（$= \V{x}_{t-1}$）に着目して$\V{f}$の線形近似を行う
    - $\V{f}(\V{x}', \V{u}_t) \approx \V{f}(\V{\mu}_{t-1}, \V{u}_t) + F_t(\V{x}' - \V{\mu}_{t-1})$
        - $F_t = \dfrac{\partial \V{f}(\V{x}', \V{u})}{\partial \V{x}'}\Big|_{ \V{x}' = \V{\mu}_{t-1}}$
            - さっきは$\V{u}$で偏微分していた　
- 近似式の意味
    - 移動前の姿勢$\V{x}'$が信念分布の中心$\V{\mu}_{t-1}$から$\V{x}'-\V{\mu}_{t-1}$だけずれているとき、その誤差は移動後に$F_t$倍拡大される

---

### $F_t$の計算

- <span style="font-size:70%">$F_t = \begin{pmatrix} \partial f_x(\boldsymbol{x}_{t-1}, \boldsymbol{u}) / \partial x_{t-1} & \partial f_x(\boldsymbol{x}_{t-1}, \boldsymbol{u}) / \partial y_{t-1} & \partial f_x(\boldsymbol{x}_{t-1}, \boldsymbol{u}) / \partial \theta_{t-1} \\ \partial f_y(\boldsymbol{x}_{t-1}, \boldsymbol{u}) / \partial x_{t-1} & \partial f_y(\boldsymbol{x}_{t-1}, \boldsymbol{u}) / \partial y_{t-1} & \partial f_y(\boldsymbol{x}_{t-1}, \boldsymbol{u}) / \partial \theta_{t-1} \\ \partial f_\theta(\boldsymbol{x}_{t-1}, \boldsymbol{u}) / \partial x_{t-1} & \partial f_\theta(\boldsymbol{x}_{t-1}, \boldsymbol{u}) / \partial y_{t-1} & \partial f_\theta(\boldsymbol{x}_{t-1}, \boldsymbol{u}) / \partial \theta_{t-1} \end{pmatrix} \Bigg|_{ \boldsymbol{x}_{t-1} = \boldsymbol{\mu}_{t-1}}$</span>　
<span style="font-size:70%">$= \begin{pmatrix} 1 & 0 & \nu_t\omega_t^{-1}\{\cos(\theta_{t-1} + \omega_t\Delta t) - \cos \theta_{t-1} \} \\ 0 & 1 & \nu_t\omega_t^{-1}\{\sin(\theta_{t-1} + \omega\Delta t) - \sin \theta_{t-1} \} \\ 0 & 0 & 1 \end{pmatrix} \Bigg|_{ \boldsymbol{x}_{t-1} = \boldsymbol{\mu}_{t-1}}$</span>　
<span style="font-size:70%">$= \begin{pmatrix} 1 & 0 & \nu_t\omega_t^{-1}\{\cos(\mu_{\theta_{t-1}} + \omega_t\Delta t) - \cos \mu_{\theta_{t-1}} \} \\ 0 & 1 & \nu_t\omega_t^{-1}\{\sin(\mu_{\theta_{t-1}} + \omega_t\Delta t) - \sin \mu_{\theta_{t-1}} \} \\ 0 & 0 & 1 \end{pmatrix}$</span>


---

### 指数部の計算

- 指数部に近似式を代入
    - <span style="font-size:80%">$= - \dfrac{1}{2}\left[ \V{x} - \V{f}(\V{\mu}_{t-1}, \V{u}_t) - F_t(\V{x}' - \V{\mu}_{t-1}) \right]^\top R_t^{-1} \left[ \text{省略} \right] \\\\ - \dfrac{1}{2}( \V{x}' - \V{\mu}_{t-1} )^\top \Sigma_{t-1}^{-1} ( \text{省略} )$</span>
<span style="font-size:80%">$= - \dfrac{1}{2}\left[ \V{x} - \V{f}(\V{\mu}_{t-1}, \V{u}_t) \right]^\top (F_t \Sigma_{t-1} F_t^\top + R_t)^{-1} \left[ \V{x} - \V{f}(\V{\mu}_{t-1}, \V{u}_t) \right]- \dfrac{1}{2} (\V{x}'$の二次形式$)+$定数</span>
        - 二次形式: ガウス分布の指数部が作れるということ

それぞれの項を$L(\V{x}), L'(\V{x}'), C$と表して元の式に戻しましょう

---

### $\hat{b}_t$はガウス分布になる

- $\hat{b}_t(\V{x}) = \eta\int_{\V{x}' \in \mathcal{X}} \exp\big\{$指数部$\big\}  d\V{x}'$
$= \eta\int_{\V{x}' \in \mathcal{X}} \exp\{L(\V{x}) \}\exp\{L'(\V{x}') \} \exp ( C ) d\V{x}'$
$= \eta \exp(C) \exp\{L(\V{x}) \}\int_{\V{x}' \in \mathcal{X}} \exp\{L'(\V{x}') \} d\V{x}'$
<span style="font-size:70%">$\qquad\qquad$（↑$C, L$は$\V{x}'$を含まないので）</span>
$= \eta \exp\{L(\V{x}) \}\int_{\V{x}' \in \mathcal{X}} \mathcal{N}(\V{x}') d\V{x}'$
<span style="font-size:70%">$\qquad\qquad$（↑定数を整理、$L'$で$\V{x}'$のガウス分布を作る）</span>
$= \eta \exp\{L(\V{x}) \}$
$= \eta e^{-\frac{1}{2}\left[ \V{x} - \V{f}(\V{\mu}_{t-1}, \V{u}_t) \right]^\top (F_t \Sigma_{t-1} F_t^\top + R_t)^{-1} \left[ \V{x} - \V{f}(\V{\mu}_{t-1}, \V{u}_t) \right] }$
<span style="color:red">$= \mathcal{N}\left[\V{x} \Big| \V{f}(\V{\mu}_{t-1}, \V{u}_t), F_t \Sigma_{t-1} F_t^\top + R_t\right]$</span>

---

## 移動後の更新の実装（詳解6.2.3）

- 得られた$\hat{b}_t$の式
    - $\hat{b}_t(\V{x}) = \eta e^{-\frac{1}{2}\left[ \V{x} - \V{f}(\V{\mu}_{t-1}, \V{u}_t) \right]^\top (F_t \Sigma_{t-1} F_t^\top + R_t)^{-1} \left[ \V{x} - \V{f}(\V{\mu}_{t-1}, \V{u}_t) \right] }$
- カルマンフィルタで実装すべき更新式
    - <span style="color:red">$\hat{\mu}_t = \V{f}(\V{\mu}_{t-1}, \V{u}_t)$</span>
        - 移動前の信念分布の中心$\V{\mu}_{t-1}$を$\V{f}$で移動
    - <span style="color:red">$\hat{\Sigma}_t = F_t \Sigma_{t-1} F_t^\top + R_t = F_t \Sigma_{t-1} F_t^\top + A_t M_t A_t^\top$</span>
        - 移動前の共分散行列$\Sigma_{t-1}$を移動による誤差の拡大行列$F_t$で大きくして、移動による雑音の共分散行列$R_t$を足す

導出がややこしい割にはたったこれだけ

---

### 実装

- 左図: 3台のロボットを動かした結果
- 右図: 左回りで100台のロボットを30[s]動かした結果
    - 左図で左回りをしているロボットの位置推定結果と比較すると、分布の形状が単純化されているのが分かる

<center><img width="35%" src="figs/kalman_no_obs.gif" /><img width="35%" src="figs/particles_vs_robots_robots.png" /></center>

---

### $R_t$に逆行列がない問題

- $R_t = A_t M_t A_t^\top$
    - $R_t$は$3\times 3$行列だが$M_t$は$2\times 2$行列なのでランク落ち
    $\Longrightarrow$逆行列は存在しない
    - 物理的な意味
        - 速度、角速度の2変数に雑音をのせても$XY\theta$の3次元では雑音が3次元に広がらない　
- 困るのかどうか$\Longrightarrow$困らない
    - 実用上の理由: $\hat{\Sigma}_t = F_t \Sigma_{t-1} F_t^\top + R_t$に$R_t^{-1}$が登場しない
    - 物理的な理由: 速度・角速度の雑音がなくても不確かさ$F_t \Sigma_{t-1} F_t^\top$は存在
（本来は数式で証明しなければならない）

---

## 観測後の信念分布の更新（詳解6.3節）

- やること
    - 観測後の信念がガウス分布になるように近似方法を考えて実装

---

## 近似前の更新式（詳解6.3.1）

- ひとつのセンサ値$\V{z}$を信念分布に反映する式
    - $b(\V{x}) = \eta p(\V{z} | \V{x}) \hat{b}(\V{x}) = \eta L(\V{x} | \V{z}) \hat{b}(\V{x})$
        - ランドマーク1個、時間の流れも気にしなくていいので添字は省略<br />　
- 尤度関数はパーティクルフィルタのものと共通
    - $L(\V{x} | \V{z}) = \mathcal{N}\left[ \V{z} | \V{h}(\V{x}), Q(\V{x}) \right]$
        - $Q(\V{x}) = \begin{pmatrix} [\ell(\V{x})\sigma_\ell]^2 & 0 \\ 0 & \sigma^2_\varphi \end{pmatrix}$
        - $\ell(\V{x})$: $\V{x}$とランドマーク$\text{m}$の距離
        - $\V{h}$: 観測関数
	
<center>$b$はガウス分布にならない</center>

---

### 尤度関数の形

- $XY$平面で見ると、尤度のモードはドーナツ状に
    - 信念分布と掛け算してもガウス分布にならない
<img width="35%" src="figs/likelihood_function.jpg" />
- どうするか？$\Longrightarrow$信念分布の中心で線形化

---

### $b$の計算式のどこを近似するか

- $b(\V{x}) = \eta e^{ -\frac{1}{2} \left[ \V{z} - \V{h}(\V{x}) \right]^\top Q\_{\V{x}}^{-1} \left[ \V{z} - \V{h}(\V{x}) \right] -\frac{1}{2} ( \V{x} - \hat{\V{\mu}} )^\top \hat{\Sigma}^{-1} ( \V{x} - \hat{\V{\mu}} ) }$
    - ここで
        - $Q_{\V{x}}$: $Q(\V{x})$のこと
        - $\hat{b} = \mathcal{N}(\hat{\V{\mu}}, \hat\Sigma)$
        - $\V{h}(\V{x}) = \begin{pmatrix} \sqrt{(x - m_x)^2 + (y - m_y)^2} \\ \text{atan2}(m_y - y, m_x - x) - \theta \end{pmatrix}$<br />　
    - <span style="color:red">指数部が$\V{x}$の二次形式になればガウス分布になる</span><br />　
- やるべき近似
    1. 非線形な$\V{h}$から$\V{x}$を救出
    2. $Q_\V{x}$から変数$\V{x}$をなくす


---

## $XY\theta$空間での観測方程式の線形近似（詳解6.3.2項）

- $\V{h}$を次のように近似して$\V{x}$の多項式に
    - $\V{h}(\V{x}) \approx \V{h}(\hat{\V{\mu}}) + H(\V{x} - \hat{\V{\mu}})$
        - $\hat{\V{\mu}}$: 信念分布の中心
        - $H = \dfrac{\partial \V{h}}{\partial \V{x}}\Big|_{\V{x} = \hat{\V{\mu}}}$
    - 意味: ある姿勢$\V{x}$でのセンサ値は、分布の中心で得られるセンサ値$\V{h}(\hat{\V{\mu}})$に、中心からのずれ$\V{x} - \hat{\V{\mu}}$を$H$倍した値を足したものに
        - もちろん近似で、$\V{x}$が$\hat{\V{\mu}}$から離れるとデタラメ

---

### $H$の計算

- $H = \dfrac{\partial \V{h}}{\partial \V{x}}\Big|_{\V{x} = \hat{\V{\mu}}}$
<span style="font-size:80%">$= \begin{pmatrix} (x - m_x)/\sqrt{(x - m_x)^2 + (y - m_y)^2} & (y - m_y)/\sqrt{(x - m_x)^2 + (y - m_y)^2} & 0 \\ (m_y - y)/\{(x-m_x)^2+(y-m_y)^2\} & (x - m_x)/\{(x-m_x)^2+(y-m_y)^2\} & -1 \end{pmatrix} \Bigg|_{\V{x} = \V{\hat{\mu}}}$</span>
<span style="font-size:80%">$= \begin{pmatrix} (\hat{\mu}_x - m_x)/\ell_{\hat{\V{\mu}}} & (\hat{\mu}_y - m_y)/\ell_{\hat{\V{\mu}}} & 0 \\ (m_y - \hat{\mu}_y)/\ell_{\hat{\V{\mu}}}^2 & (\hat{\mu}_x - m_x)/\ell_{\hat{\V{\mu}}}^2 & -1 \end{pmatrix}$</span>
    - ここで<span style="font-size:80%">$\quad \ell_{\hat{\V{\mu}}} = \sqrt{(\hat{\mu}_x - m_x)^2 + (\hat{\mu}_x - m_y)^2}$</span>
    - すべて既知の変数で構成される

---

### $Q_\V{x}$の近似

- $Q(\V{x}) = \begin{pmatrix} [\ell(\V{x})\sigma_\ell]^2 & 0 \\ 0 & \sigma^2_\varphi \end{pmatrix}$を定数にしたい<br />　
$\Longrightarrow$信念分布の中心$\hat{\V{\mu}}$で$\V{x}$を代用<br />　
- $Q_{\ell_{\hat{\V{\mu}}}} = \begin{pmatrix} [\ell_{\hat{\V{\mu}}} \sigma_\ell]^2 & 0 \\ 0 & \sigma_\varphi^2 \end{pmatrix}\label{eq:kalman_q_lmu}$ を使う
   - $\ell_{\hat{\V{\mu}}}$: $\hat{\V{\mu}}$でのランドマークとの距離<br />　
- 以後、$Q$という表記は$Q_{\ell_{\hat{\V{\mu}}}}$のこと

---

### 近似後の$b$の式

- $b(\V{x}) = \eta\exp \Big\{ -\frac{1}{2} \Big[ \V{z} - \V{h}(\hat{\V{\mu}}) - H(\V{x} - \hat{\V{\mu}})  \Big]^\top Q^{-1} \Big[ \text{省略}\Big]$
$\qquad\qquad -\frac{1}{2} ( \V{x} - \hat{\V{\mu}} )^\top \hat\Sigma^{-1} ( \V{x} - \hat{\V{\mu}} ) \Big\}$
    - $\V{x}$の多項式として指数部を整理
        - 2次の項: $-\dfrac{1}{2} \V{x}^\top (H^\top Q^{-1}H + \hat\Sigma^{-1} ) \V{x}$
        - 1次の項: $\V{x}^\top \{ H^\top Q^{-1} (\V{z} - \V{h}(\hat{\V{\mu}}) + H\hat{\V{\mu}}) + \hat\Sigma^{-1} \hat{\V{\mu}} \}$
- ガウス分布は次のようにも書けるので、上の1, 2次の項から$b = \mathcal{N}(\V{\mu},\Sigma)$が求まる
    - $p(\V{x}) = \eta \exp \left\{ -\dfrac{1}{2}\V{x}^\top \Sigma^{-1} \V{x} + \V{x}^\top \Sigma^{-1}\V{\mu} \right\}$

---

### センサ値を反映するための更新式

- 2次の項から
    - $\Sigma^{-1} =  H^\top Q^{-1}H + \hat\Sigma^{-1}$<span style="color:red">$\ \Longrightarrow\ \Sigma =  (H^\top Q^{-1}H + \hat\Sigma^{-1} )^{-1}$</span>
- 1次の項から
    - $\Sigma^{-1}\V{\mu} = H^\top Q^{-1} (\V{z} - \V{h}(\hat{\V{\mu}}) + H\hat{\V{\mu}}) + \hat\Sigma^{-1} \hat{\V{\mu}}$　
<span style="color:red">$\V{\mu} =$</span>$\Sigma \{ H^\top Q^{-1} (\V{z} - \V{h}(\hat{\V{\mu}}) + H\hat{\V{\mu}}) + \hat\Sigma^{-1} \hat{\V{\mu}} \}$　
$\quad = \Sigma \{ H^\top Q^{-1}(\V{z} - \V{h}(\hat{\V{\mu}})) + (H^\top Q^{-1} H + \hat\Sigma^{-1} )\hat{\V{\mu}} \}$
<span style="color:red">$\qquad = \Sigma H^\top Q^{-1} (\V{z} - \V{h}(\hat{\V{\mu}})) + \hat{\V{\mu}}$</span>
- 解釈
    - 更新後の精度行列: 更新前の情報$\hat{\Sigma}^{-1}$にセンサ値からの情報$H^\top Q^{-1}H$を
    足したもの
    - 更新後の分布の中心: 更新前の中心$\hat{\V{\mu}}$に、センサ値のずれ$\V{z} - \V{h}(\hat{\V{\mu}})$を
    <span style="color:red">行列$\Sigma H^\top Q^{-1}$</span>で変換した量を足したもの

---

## 6.3.3 カルマンゲインによる表現

- 行列$\Sigma H^\top Q^{-1}$を、センサ値のずれに応じて信念分布の中心を移動するための拡大率と考え<span style="color:red">カルマンゲイン</span>と呼ぶ　
- カルマンゲインを使って更新式を整理
（行列の計算は書籍参考のこと）
    - $K = \hat\Sigma H^\top (H \hat\Sigma H^\top + Q )^{-1}$
    - $\Sigma =  (I - KH) \hat{\Sigma}$
    - $\V{\mu} = K (\V{z} - \V{h}(\hat{\V{\mu}})) + \hat{\V{\mu}}$　
- 新たな解釈
    - 更新後の共分散行列: 更新前の不確かさ$\hat{\Sigma}$が$KH\hat{\Sigma}$だけ縮小
    - 更新後の分布の中心: センサ値のズレを$K$で$XY\theta$空間に写像して、その分だけ中心をずらす

---

## 6.3.4 観測後の更新の実装

- 行列とベクトルの計算式をシミュレータに実装
    - 同時刻に複数のランドマークを観測した場合:前ページの処理を繰り返す
    - センサ値のバイアスで誤差楕円から出てしまうがこれはパーティクルフィルタと同じ（4章の独立同分布の問題がある）

<img width="35%" src="./figs/kalman_filter.gif" />

---

## 6.4 まとめ

- カルマンフィルタを実装
    - ガウス分布のパラメータ計算だけでベイズフィルタを実装
    - <span style="color:red">計算が分かれば</span>実装が簡単
    - 本章以降でも同様の計算（理屈をしっかりおさえましょう）
        - FastSLAM、graph-based SLAM、POMDP　
- バイアスは自己位置推定の大敵
    - 残念ながら信念分布はそのまま鵜呑みにできない　
- 誘拐やスタックなど大きな誤りを生む問題は未解決

