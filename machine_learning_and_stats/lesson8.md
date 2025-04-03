---
marp: true
---

<!-- footer: "機械学習（と統計）第8回" -->

# 機械学習

## 第8回: 法則性の発見+自信のなさの見積もり: ガウス過程回帰

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- ガウス過程回帰

---

## 前回のおさらい

- 回帰を勉強した
    - けど、少ないデータでもひとつにグラフを決めてしまう
- なにが足りないか
    - 第6回のようなベイズ的な考えが抜けている
- ベイズ的な考え方をとりいれた回帰がないか?
    - ある


---

## ベイズ線型回帰

- $y = f(x)$の分布を考える
    - 関数の分布ってなに? $\Rightarrow$ パラメータの分布
    - 例: $y = w_1 x + w_0$の場合: $w_1$と$w_0$の確率分布を考える
        - 右図: $w_1, w_0$それぞれをガウス分布で分布すると考えてサンプリング
            - どちらも平均値$0$、標準偏差$1$
            - データ（黒丸）に合うように、<span style="color:red">ベイズの定理で</span>$w_1, w_0$の分布を変更していく

![bg right:30% 100%](./figs/line_sampling.png)

---

## ベイズ線型回帰でよくなること

- データ数が少ないときに解を曖昧にしておける
- 事前分布に予測を盛り込める
- パラメータを多めにしておいても不要なものが消えるかもしれない


