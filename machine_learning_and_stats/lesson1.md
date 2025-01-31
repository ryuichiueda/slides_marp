---
marp: true
---

<!-- footer: "機械学習（と統計）第1回" -->

# 機械学習と統計

## 第1回: イントロダクション

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 機械学習とはなに？
- 機械学習と統計と動物

---

## 機械学習とはなに？

- 英語にするとmachine learning
    - 同名の教科書: https://www.cs.cmu.edu/~tom/mlbook.html によると
        ```text
        Definition: A computer program is said to learn from
        experience E with respect to some class of tasks T
        and performance measure P, if its performance at tasks in
        T, as measured by P, improves with experience E.
        ```


<center>わからんので別の視点で考えてみましょう</center>


---

## 知能と機械学習

- これは何に見えますか
    - （点で絵を描いたものをここに）  
- なんで◯◯に見えるんでしょう？  

---

## 人間の眼の仕組み

- 目の奥底に視細胞がびっしり
- 視細胞ひとつひとつから脳に配線（シナプス）
- ドットの絵を見ると（単純化すると）黒と白のデジタル信号が各線からバラバラに入る

なんでバラバラなのに形がわかるの？ 

---

## さらなる疑問1

- 別の場所に見えても形がわかる
- 回転していても形が分かる
- 大きさが違っても形が分かる 

配線で考えると全然違う信号なのになんで？

---

## さらなる疑問2

- そもそも点々を実物の◯◯とみなすのはなぜ？
- みんななにも疑問に思ってないのはなぜ？
- ネズミは絵に描いた猫を嫌がるだろうか？

---

## 脳の機能

- バラバラなものから法則性を見つける
- 法則性のあるものを識別する

これがないと実世界で生きていけない

---


## 計算機（コンピュータ） に話を戻しましょう

- 今の話から機械学習というものを定義してみましょう（一般的ではないですが）

「実世界をコンピュータに理解させる。動物みたいに。」 

ということにしておきましょう

---

## で、どうやって？