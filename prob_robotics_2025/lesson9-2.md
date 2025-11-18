---
marp: true
---

<!-- footer: 確率ロボティクス第9回 -->

# 確率ロボティクス第9回: 行動決定（その2）

千葉工業大学 上田 隆一

<br />

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 今日やること

- Q学習のおさらい
- ベルマン方程式

---

## Q学習の「学習の原理」として紹介した手続き

- 最初に適当な$V$を設定
- 次の2つの値を比較
    - $V^\Pi(\boldsymbol{x})$
    - $Q^\Pi(\boldsymbol{x}, a) = \big\langle \ell(\boldsymbol{x}, a, \boldsymbol{x}')  + V^\Pi(\boldsymbol{x}' )\big\rangle_{P(\boldsymbol{x}' | \boldsymbol{x}, a)}$
        - $a$は方策が示すものとは別の行動
- 後者のほうがよければ
    - $\Pi(\boldsymbol{x}) \longleftarrow a$
    - $V^\Pi(\boldsymbol{x})\longleftarrow Q(\boldsymbol{x},a)$

<center style="color:red">いつか収束する</center>

---

### ベルマン（最適）方程式

- 収束した$\Pi$と$V$をそれぞれ$\Pi^*, V^*$とすると
    - $V^*(\boldsymbol{x}) = \min_{a\in\mathcal{A}} \big\langle \ell(\boldsymbol{x}, a, \boldsymbol{x}')  + V^*(\boldsymbol{x}' )\big\rangle_{P(\boldsymbol{x}' | \boldsymbol{x}, a)}$
    - $\Pi^*(\boldsymbol{x}) = \arg\!\min_{a\in\mathcal{A}} \big\langle \ell(\boldsymbol{x}, a, \boldsymbol{x}')  + V^*(\boldsymbol{x}' )\big\rangle_{P(\boldsymbol{x}' | \boldsymbol{x}, a)}$
- $\Pi^*$: 最適方策
    - どの$\boldsymbol{x}$でも最適な行動を提示可能
- $V^*$: 最適状態価値関数
    - 状態$\boldsymbol{x}$から最適方策を選び続けたときの価値の期待値
- ベルマン方程式を解く問題: 最適制御問題

<center style="color:red">実は世の中の制御はベルマン方程式を解く問題になっている</center>

---

### （最適）制御問題の例

- 制御の問題: ある状態を別の状態に変化させたい
    - その際、コストを抑えたい（最小化したい）
        - PIDなどはコストを直接考えていないのである意味でヒューリスティック

|現象|制御|
|:---|:---|
|ロボットが目的地にいない|目的地にいる状態にしたい|
|機械が振動している|振動してない状態に戻したい|
制御|ライントレースのロボットがラインからずれた|ライン中央に戻したい|
|洗濯物が洗濯機の中に|畳んで収納したい|

<span style="font-size:80%">（※VLAは目的の状態を言葉から自律的に設定）</span>

<center style="color:red">制御対象の見かけ、計算リソース・時間の制約、解法で違う問題に見えるだけ</center>

---

### 例: ベルマン方程式から機械を安定させる問題へ

- 考えるシステム
	- $\dot{\boldsymbol{x}} = A\boldsymbol{x} + B\boldsymbol{u} + \boldsymbol{\varepsilon}$
	    - $\boldsymbol{x}$: 状態（時間の関数）
	    - $\boldsymbol{u}$: 制御入力（時間の関数）
	    - $\dot{\boldsymbol{x}} = \dfrac{\text{d}\boldsymbol{x}}{\text{d}t}$
- 制御の目的: $J(\Pi, \boldsymbol{x}_0) =  \int_0^\infty L\left[ \boldsymbol{x}(t), \boldsymbol{u}(t) \right] \text{d}t$の最小化
	- $L(\boldsymbol{x}, \boldsymbol{u}) = 
	\dfrac{1}{2}\boldsymbol{x}^\top Q \boldsymbol{x}
	+\dfrac{1}{2}\boldsymbol{u}^\top R \boldsymbol{u}$
	    - 最初の項: なるべく$\boldsymbol{x}$を原点付近に保つ
	    - 次の項: なるべく入力$\boldsymbol{u}$の値を小さく（労力をかけたくない）

<center>つまり（なにかの拍子に動いてしまった）システムを制止させたい</center>

---

### この問題のベルマン方程式

- ある時刻$0$から微小時間$\Delta t$の間の制御$\boldsymbol{u}(t)$が最適なとき
    - $V^*(\boldsymbol{x}_0) = \min_{\substack{\boldsymbol{u}(t) \\ (0\le t < \Delta t)}}\left\{ \int_0^{\Delta t} L\left[ \boldsymbol{x}(t), \boldsymbol{u}(t) \right] \text{d}t +  V^*\left[ \boldsymbol{x}( \Delta t) \right] \right\}$
        - $\boldsymbol{x}_0 = \boldsymbol{x}(0)$
        - どの時刻を$0$とおいてもよいことに注意
- $\boldsymbol{u}(t)$を求めましょう

---

### ベルマン方程式の整理

方法は教科書を

- $V^*[ \boldsymbol{x}( \Delta t)]$を$\Delta t$に対して線形な式に近似してベルマン方程式を整理すると
	- $0 = \min_{\boldsymbol{u}} \left\{ L( \boldsymbol{x}, \boldsymbol{u} ) +  \nabla V^*(\boldsymbol{x})^{\top}  ( A\boldsymbol{x} + B\boldsymbol{u} ) \right\}$
    （これもベルマン方程式といえる）
- 意味
    - $\dot{\boldsymbol{x}} = A\boldsymbol{x} + B\boldsymbol{u} + \boldsymbol{\varepsilon}$なので、$\dot{\boldsymbol{x}}$の平均値$\bar{\dot{\boldsymbol{x}}}$を考えると
    $0 = \min_{\boldsymbol{u}} \left\{ L( \boldsymbol{x}, \boldsymbol{u} ) +  \nabla V^*(\boldsymbol{x})^{\top} \bar{\dot{\boldsymbol{x}}}\right\}$
    - つまり、$V^*$の変化量に速度の平均値をかけると、状態遷移に伴って$-L$だけコストが減るという意味

---

### 例: ベルマン方程式から機械を安定させる問題へ

