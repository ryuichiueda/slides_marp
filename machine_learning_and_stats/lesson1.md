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


<center>わからん</center>





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



---

## 機械学習の例

- スパムフィルタ
    - 来たメールを迷惑メールかそうでないかを分別
        - どうやって？