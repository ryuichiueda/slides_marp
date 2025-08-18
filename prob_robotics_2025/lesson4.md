---
marp: true
---

<!-- footer: 確率ロボティクス第4回 -->

# 確率ロボティクス第4回: 連続値と多変量

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

- 連続値に対する確率分布の定義方法
- 多変量の確率分布

教科書では数学的なあれこれがちょっとだけ書いてありますが、講義では実用面から考えましょう。

---

## ある実験

- ある位置から何度もロボットを4m前進させ、実際に到達した位置$(x,y)$と向き$\theta$の統計をとった
- 知りたいこと: ロボットの到達した座標$(x,y,\theta)$の分布は？
    - 右の図のような分布の図を描きたい
$\qquad\qquad\qquad\qquad$![w:600](./figs/robot_final_pos.png)

![bg right:30% 95%](./figs/prob_dist.png)

---

### 困ること

- 困ること1: $x,y,\theta$が「連続的」
    - 統計をとっても点になるから前ページのようなグラフが描けない
- 困ること2: 確率変数$x,y,\theta$が3つもある
    - こういうことは前回もあったが、分布の形については扱っていない

<center style="padding-top:100px;font-size:120%">どうしましょう？</center>

![bg right:30% 95%](./figs/robot_final_pos_b.png)

---

## 連続的・多変量の確率変数の扱い

- ひとつずつ対処の方法を見ていきましょう
    - 離散値に近似して確率分布を求める方法
    - 空間を囲って確率を計算する方法
    - 密度・確率密度関数の導入

---

### 離散値への近似

- 実数を離散値に対応づけると点状のデータから確率分布が描ける
- 離散化や量子化などと呼ばれる
- 方法
    - 実数をどこかの桁で四捨五入
    - 実数を範囲ごとに区切る
- 例: 最初の例の$\theta$の値（単位はdegree）
    - -9.5, -9.5, -4.6, -4.0, -0.3, 4.1, 6.2, 9.0, 11.1, 18.2, 18.3, 19.3, 19.9, 19.9, 21.1, 21.8, 22.5, 23.9, 24.3, 24.7

![bg right:30% 95%](./figs/theta_hist.png)

---

### 離散値への近似（多次元の場合）

- 2次元の場合: 平面を区画化してデータの数を数えて分布に
    - 右図: 最初の例の$(x,y)$座標についてこの作業をしたもの
- より高い次元
    - 3次元空間、4次元空間・・・を同様に区画化
    - 4次元以上は想像しにくいので、リストや数式で考えたほうがいいかもしれない
        - 例: 4軸の区画の組み合わせ$(h,i,j,k)$に対し確率$P(h,i,j,k)$を計算するなど


![bg right:30% 95%](./figs/discretization.png)


---

### 離散値への近似（注意する点・問題点）

- データの数や利用用途に応じて適切な解像度が必要
    - 右図のように分布が元のデータやデータの性質を表さない恐れ
- 多次元になるほどデータが不足
    - 1次元で$1000$データが必要なら$n$次元だと$1000^n$必要
    - データが足りない場合、データの背景、原因を考えたほうがよりよい分布を作れるかもしれない

![bg right:25% 95%](./figs/discretization_resolution.png)

---

## 空間を囲って確率を計算する方法<br />（モンテカルロ法）

- あらかじめ離散化の方法を決めなくても、
データから確率は計算可能（分布は作れない）
    - 例（右図）
        - $\Pr\{ (x,y) \in A \} = 3/20$
        - $\Pr\{ (x,y) \in B \} = 6/20$

![bg right:35% 95%](./figs/montecarlo.png)
