---
marp: true
---

<!-- footer: "機械学習（と統計）第11回" -->

# 機械学習

## 第11回: 人工ニューラルネットワークの基礎

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 人工ニューラルネットワークってなに？

---

## 人工ニューラルネットワークってなに？

- まずは問題
    - なんで犬とか猫とか我々は認識できるのか?
    - 入出力はどうなってるの?
        - 入力は第1回に見せた通り（下図）
        - 犬・猫などの名前は出力
        - <span style="color:red">途中はどうなっているのか?</span>


![w:400](./figs/Retina-diagram.svg.png)<span style="font-size:40%">（https://commons.wikimedia.org/wiki/File:Retina-diagram.svg, by S. R. Y. Cajal and Chrkl, CC-BY-SA 3.0）</span>

![bg right:30% 100%](./figs/cat_and_dog.png)

