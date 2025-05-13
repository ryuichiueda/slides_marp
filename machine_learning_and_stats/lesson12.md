---
marp: true
---

<!-- footer: "機械学習（と統計）第12回" -->

# 機械学習

## 第12回: 画像と人工ニューラルネットワーク

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- CNN
- GAN

---

## 以前から触れていた話題

- 動物は視覚をどう行動や判断に必要な情報に変えているか
- それをコンピュータで再現できるか

![w:400](./figs/Retina-diagram.svg.png)<span style="font-size:40%">（https://commons.wikimedia.org/wiki/File:Retina-diagram.svg, by S. R. Y. Cajal and Chrkl, CC-BY-SA 3.0）</span>

人工ニューラルネットワークでできる?$\rightarrow$できる

---

## もうひとつの話題: なんか自動で絵を描くやつが出現

実例は各自いろんなところで調査を

- こいつらはどういう仕組み?
    - 最近のは言語も駆使している（次回）
    - ちょっと古いけど基礎をやりましょう

