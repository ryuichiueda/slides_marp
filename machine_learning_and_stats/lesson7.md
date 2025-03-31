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
        - ※分布を考えることと本質的な違いはそれほどない。道具の違い。

![bg right:40% 100%](./figs/relations.png)

---

### 回帰が便利な例

- 時系列データなど、分布で扱う必要のない変数がある
    - 例: 株価、人口・・・
    - 時間を分布で扱う必要はない
- なにかしらの関数$y = f(x)$で縦軸の値が決まっていそうな場合
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
    - $\{w_1 x_1 + w_0 -y_1\}^2+\{w_1 x_2 + w_0 -y_2\}^2+$
    $\dots+\{w_1 x_N + w_0 -y_N\}^2$の値を最小化
    - なんで2乗?: 必然性はないが分散を最小にしたいと解釈すれば自然
- 一般的な回帰
    - $L\left[w_{0:M} | (x,y)_{1:N}\right] = \sum_{i=1}^N \left\{f(x_i | w_{0:M}) - y_i \right\}^2$
    の最小化
        - データ$(x_i, y_i) \ (i=1,2,\dots,N)$に対して$y=f(x|w_{0,M})$を当てはめる場合

![bg right:30% 100%](./figs/lsm_liner.png)

---

### 最小二乗法による一次方程式のあてはめ

- おそらくどこかで勉強した、一番基本的な回帰
- 線が点の真ん中を通るようにする
    - どうやって「真ん中」を決めるか
    $\rightarrow$線とそれぞれの点の$y$軸方向の距離を損失と考えて足して最小化
    $\qquad\Downarrow$
- 点$(x_1, y_1), (x_2, y_2), \dots, (x_N, y_N)$に対し、$y=f(x)$について
$\{y_1 - f(x_1)\}^2+ \{y_2 - f(x_2)\}^2+\dots+$
$\{y_N - f(x_N)\}^2$の値を最小化
    - なんで2乗の和を最小化するか: 必然性はないが分散を最小にしたいと解釈

![bg right:30% 100%](./figs/lsm_liner.png)
