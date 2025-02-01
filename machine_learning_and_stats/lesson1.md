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

- 右の図は何に見えますか
* なんで◯◯に見えるんでしょう？

![bg right:40% 60%](./figs/dots.png)

---

## 人間の眼の仕組み

- こんな構造
    ![w:400](./figs/Retina-diagram.svg.png)<span style="font-size:40%">（https://commons.wikimedia.org/wiki/File:Retina-diagram.svg, by S. R. Y. Cajal and Chrkl, CC-BY-SA 3.0）</span>
    - 左から光が入って右側の視細胞（2種類、1.3億個）で受け止め電気信号に
    - 電気信号は右に向かって処理されて図の下向きの赤い線から脳へ
        - 網膜の各部分の赤い線が「視神経（100万個）」の束になって脳に
- こんな構造なので
    - 何か見ると1.3億のバラバラな信号として入る
        - 白黒の絵の場合は1.3億のスイッチのON/OFFの信号に単純化できる

<center style="color:red">なんでバラバラなのに形がわかるの？</center>


---

## さらなる疑問1（形や大きさに関して）

- 別の場所に見えても形がわかる
- 回転していても形が分かる
- 大きさが違っても形が分かる 

スイッチのON/OFFで考えると全然違う信号なのになんで？

---

## さらなる疑問2（ものの識別や名前に関して）

- そもそも点々を実物の◯◯とみなすのはなぜ？
    - p.4の議論では、（私みたいによほどひねくれてない限り）誰もなにも疑問に思ってなかったはず
- ネズミは絵に描いた猫を嫌がるだろうか？
    - 絵や鏡に写ったものは実物ではない

---

## いまの話のまとめ

- 脳は刺激をたくさんのスイッチで受け取ってるらしい
    - 目のほか、耳や鼻や舌なども
    - おもいのほかデジタル
- 脳はデジタル信号になんらかの解釈を加えているらしい
    - 解釈ができるから、食べる、逃げるなど自分に利益のある行動が
      できるなのではないだろうか？


---

## 目のような機能を再現したい

- なんでか？: 便利だから


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
