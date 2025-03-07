---
marp: true
---

<!-- footer: "機械学習（と統計）第4回" -->

# 機械学習

## 第4回: 様々な分布II

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 離散型確率分布と連続型確率分布の違い
- 二項分布、ガウス分布以外の重要な分布について確認
    - ポアソン分布
    - ディリクレ分布
    - 多次元の分布
- 式も重要ですけど現象との関係に注目しましょう

---

## 離散、連続

- 確率変数が整数のときと実数（小数）のときがある
    - 二項分布: 整数（<span style="color:red">離散型確率分布</span>）
    - ガウス分布: 実数（<span style="color:red">連続型確率分布</span>）

![bg right:30% 100%](./figs/bin_and_gauss2.png)

---

## ポアソン分布

- ある事象が一定時間に起こる回数がしたがう分布
    - 式: $P(x) = \dfrac{n^x e^{-n}}{x!}  = \eta \dfrac{n^x}{x!}$
        - $n$: ある期間にその事象が起こる回数
- 事象の例
   - 1ヶ月以内の地震の数など
- 分布の形
    - $n$が大きいとガウス分布に近づく
        - なんででしょう？
            * 大量のコインを投げて何枚表になるでしょうかという問題と等価になる

![bg right:30% 80%](./figs/poisson.png)


---

### 問題

- 問題: 年1回大きな地震が起こる地域で、次の3つの確率を求めてみましょう
    - ある年に起こらない確率
    - 1回起こる確率
    - 3回以上起こる確率
- ポアソン分布の式（再掲）: $P(x) = \dfrac{n^x e^{-n}}{x!}$
    - $0! = 1$に注意
- 答え
    * $P(0) = e^{-1} = 0.36789744... \approx 0.37$
    * $P(1) = e^{-1} = 0.36789744... \approx 0.37$（きっちり1回の年は4割もない）
    * $\text{Pr}(3$回以上$) = 1 - \left\{P(0) + P(1) + P(2)\right\}$
    $\qquad\qquad\qquad= 1 - (e^{-1} + e^{-1} + e^{-1}/2) \approx 0.08$

---

## 指数分布

- ある事象が起こってから次に起こるまでの間隔がしたがう分布
    - 例: 地震と地震の間の時間間隔
    - ポアソン分布と表裏一体（違いはちゃんと説明できるようにしましょう）
- 式: $P(x) = \dfrac{1}{t}\exp\left\{-\dfrac{x}{t}\right\}$
    - $t$: 間隔の平均値（$1/t$はポアソン分布の$n$に）

![bg right:30% 90%](./figs/exp_dist.png)
