---
marp: true
---

<!-- footer: "機械学習（と統計）第3回" -->

# 機械学習

## 第3回: 様々な分布I

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 二項分布
- ガウス分布

---

### 実験

1. ノートか定規を用意
    - ノートの場合は1, 2, 3, 4, 5, ....と罫線に数字を書く
2. 以下を繰り返す
    - ペンを右の写真のようにセット
    - 指で根本を弾いてペン先の位置を記録（四捨五入で）

- なにか傾向が出てくるまでやってみましょう
    - 本当は結果を見ながら試行したらダメなんだけど
    - 何回か練習してからやりましょう

![bg right:25% 100%](./figs/pengame.png)

---

### 結果の例

- 講師が10を狙って100回試行した結果
- 疑問
    - こういう試行の「分布」をどう数学で扱う？
    - なんでこういう形になるんだろう？

![bg right:50% 100%](./figs/pengame_freq.png)

---

### 理由

- 狙ったところにいかない理由はたくさんある
    - 具体的な理由が気になるけどここでは取り上げません
- 例えば10個の理由A, B, C, ..., Jがあるとして、その理由で発生する誤差を$e_\text{A}, e_\text{B}, ..., e_\text{J}$とする
- これらの誤差が一斉にマイナス、あるいはプラスになると大きな誤差が出るけど、そんな偶然が起こる確率は低い

→ 必然的に真ん中に山ができる

---

### 二項分布

- 