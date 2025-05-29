---
marp: true
---

<!-- footer: "機械学習（と統計）第7回" -->

# 機械学習

## 第7回: 法則性の発見: 最小二乗法と回帰											

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- データの法則性
- 最小二乗法
- 回帰

---

### データの法則性

- 右図: 第4回でとりあげたデータ
    - 出典:  [日本病院薬剤師会](https://www.jshp.or.jp/)
    - 共分散を求めた
        - 分布を当てはめるため
- 今回、次回は別の問題を考える
    - 横軸の値（$x$）に対して、縦軸の値の傾向$y = f(x)$を求める<span style="color:red">（回帰）</span>
        - 横軸の値に対して縦軸の値はどういう傾向にあるか

![bg right:35% 100%](./figs/relations.png)

---

### 回帰が適切な例

- $y=f(x)$の関係があると分かっている場合は分布の当てはめより適切
    - 時系列データなど（例: 株価、人口の推移）
        - 時間を分布で扱う必要はない
    - 実験データをナントカ方程式に当てはめてみる

---

### 最小二乗法による一次方程式のあてはめ

- 点$(x_1, y_1), (x_2, y_2), \dots, (x_N, y_N)$に対し、直線$y=w_1 x + w_0$が真ん中を通る$w_1, w_0$を求める
    - $w_1$が傾き、$w_0$が切片
    - おそらくどこかで勉強した、一番基本的な回帰

![bg right:30% 100%](./figs/lsm_liner.png)

<br />
<center style="color:red">どうやって「真ん中」を決めるか?</center>

---

### どうやって「真ん中」を決めるか

- 線とそれぞれの点の$y$軸方向の距離を損失と考えて、距離の2乗を足して最小化
    - <span style="color:red">損失関数</span>$\mathcal{L}(w_{0:1}| x_{1:N}, y_{1:N}) = \{w_1 x_1 + w_0 -y_1\}^2$
    $\qquad\qquad+\{w_1 x_2 + w_0 -y_2\}^2+\dots$
    $\qquad\qquad+\{w_1 x_N + w_0 -y_N\}^2$
    $= \sum_{i=1}^N \{w_1 x_i + w_0 -y_i\}^2$の値を最小化
    - なんで2乗?: 必然性はないが分散を最小にしたいと解釈すれば自然

![bg right:30% 100%](./figs/lsm_loss.png)

---

### 損失関数を最小化するパラメータの導出

- 損失関数をパラメータで偏微分して、$0$になるパラメータを求める
    - $\nabla \mathcal{L}(w_{0:1} | x_{1:N}, y_{1:N} ) = \left( \dfrac{\partial\mathcal{L}}{\partial w_0},  \dfrac{\partial\mathcal{L}}{\partial w_1} \right) = \boldsymbol{0}$
        - $w_0$、$w_1$をどうずらしてもそれ以上$\mathcal{L}$の値が変わらない
        $\Rightarrow$ほかにそういう点がなければそのときの値が$\mathcal{L}$の最小値
- 前ページの式を解いてみましょう
    - $\mathcal{L}(w_{0:1}| x_{1:N}, y_{1:N}) = \sum_{i=1}^N \{w_1 x_i + w_0 -y_i\}^2$
        - $w_0$、$w_1$それぞれで微分したもので連立方程式をたてる

---

### 答え

 $(x,y) = (x \ y)^\top$としています

- $\nabla L(w_{0:1}) = 2 \sum_{i=1}^N \begin{pmatrix}
    \left\{ (w_1 x_i + w_0 ) - y_i  \right\} \\
    \left\{ (w_1 x_i + w_0 ) - y_i  \right\}x_i
    \end{pmatrix}$
    $= 2N \begin{pmatrix}
    w_1 \bar{x} + w_0 - \bar{y}\\
    w_1 \overline{x^2} + w_0 \bar{x} - \overline{xy}
    \end{pmatrix} = \boldsymbol{0}$（$\overline{\ }$は平均値）
<span style="color:red">$\Longrightarrow (w_0 , w_1) = \left(
\dfrac{\overline{x^2}\bar{y} - \overline{xy}\bar{x}}{\overline{x^2} - \bar{x}^2},
\dfrac{\overline{xy} - \bar{x}\bar{y}}{\overline{x^2} - \bar{x}^2}
\right)$</span>

---

### 計算してみましょう

- $(x,y) = (2,3), (6,2), (-3,1), (-6,2)$に対して最小二乗法を適用
- 式（さっき求めたもの）: $(w_0 , w_1) = \left(
\dfrac{\overline{x^2}\bar{y} - \overline{xy}\bar{x}}{\overline{x^2} - \bar{x}^2},
\dfrac{\overline{xy} - \bar{x}\bar{y}}{\overline{x^2} - \bar{x}^2}
\right)$

![bg right:40% 100%](./figs/lms_problem.png)

---

### 答え

- $(x,y) = (2,3), (6,2), (-3,1), (-6,2)$に対して最小二乗法を適用
    - 各種平均値を計算
        - $\overline{x}= -1/4$
        - $\overline{y}= 2$
        - $\overline{x^2}= 85/4$
        - $\overline{xy}= 3/4$
    - $w_0 = (\overline{x^2}\bar{y} - \overline{xy}\bar{x})/(\overline{x^2} - \bar{x}^2)= 2.01$
    - $w_1 = (\overline{xy} - \bar{x}\bar{y})/(\overline{x^2} - \bar{x}^2)= 0.0590$
    $\Longrightarrow y=0.0590 x + 2.01$



![bg right:40% 100%](./figs/lms_ans.png)

---

## 損失関数の重要性

- ベイズの定理とともに機械学習に重要
- 「損失関数の最小化」は機械学習のほぼすべての手法で共通の考え方
    - 「最大化」の場合は符号を変えると最小化になる
    - 機械学習の一番単純な説明（1、2の繰り返し）
        - 1: なにか入力して出力を観測
        - 2: 損失関数の値が小さくなるようにパラメータを変更
    - 最小二乗法: 偏微分で最適なパラメータが分かるので学習が不要なだけ
        - 大規模あるいは非線形な問題ではこの方法が使えない
        $\Rightarrow$様々な手法を使用


---

## 微分方程式で解けない場合の最適化

- $n$個のパラメータで構成される損失関数の最適化を考えてみましょう
    - $\mathcal{L}(w_{1:n}| x_{1:N}, y_{1:N})$
        - どうやって$w_{1:n}$をいじって$\mathcal{L}$の値を減らすか
- ためしに$\Delta w_{1:n}$だけずらしてみる
    - $\mathcal{L}(w_{1:n}| x_{1:N}, y_{1:N})$が$\mathcal{L}(w_{1:n} + \Delta_{1:n}| x_{1:N}, y_{1:N})$に
        - 後者の値が小さくなったら$w_{1:n}$を$w_{1:n} + \Delta w_{1:n}$に変更すると
        「よりよく」なる
    - 問題: いろいろ$\Delta w_{1:n}$を試すとよいんだけどパラメータが多いと組み合わせが多くて大変
    $\Rightarrow$計算で一番よい$\Delta w_{1:n}$を求められないだろうか?

---

### ふたたび偏微分

- $\nabla \mathcal{L}(w_{1:n} | x_{1:N}, y_{1:N} ) = \left( \dfrac{\partial\mathcal{L}}{\partial w_0},  \dfrac{\partial\mathcal{L}}{\partial w_1}, \dots, \dfrac{\partial\mathcal{L}}{\partial w_n} \right)$
    は、$w_0, w_1, \dots, w_n$それぞれを少しずらしたときの$\mathcal{L}$の変化量
- 変化量の計算
    - $\Delta \mathcal{L} = \dfrac{\partial \mathcal{L}}{\partial w_1}\Delta w_1 + \dfrac{\partial \mathcal{L}}{\partial w_2} \Delta w_2 + \dots \dfrac{\partial \mathcal{L}}{\partial w_m} \Delta w_m = \nabla \mathcal{L}(w_{1:n})^\top \Delta w_{1:n}$
- わかること
    - $|\Delta w_{1:n}| \le \alpha$という制限がある場合、最も減るのは
    $<span style="color:red">\Delta w_{1:n} = - \alpha \nabla \mathcal{L}(w_{1:n})$</span>のとき
        - 内積が最小になる
    - 上記の赤字の式にしたがってパラメータを更新すればよい


---

### いままでの回帰手法の問題

- 1つの答えしか出さない
   - 前回、前々回のような「自信のなさ」が表現できない
   - $L$の大小で当てはまりの良さは計算できるが、確率的な「自信のなさ」とは少し違う
- パラメータの数が多いと「過学習」
   - データを曲線でつないだグラフができる
