---
marp: true
---

<!-- footer: 確率ロボティクス第8回 -->

# 確率ロボティクス第8回: 機械学習（その1）

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

- ベイズ線形回帰

---

### 教科書第7章のおさらい

- 情報を統合するからものごとが（確率的に）分かる
- ベイズフィルタだけでなくて、もっと有効に活用できないか？
$\rightarrow$できる


---

## 関数を自在に生成する（人工ニューラルネットワーク）

- 問題: デジタル画像の犬と猫（とそれ以外）を識別する「関数」はどう数式で書けるでしょうか？
    - 引数（入力）は？
    - 答え（出力）は？

![bg right:35% 100%](./figs/cat_and_dog.svg)
