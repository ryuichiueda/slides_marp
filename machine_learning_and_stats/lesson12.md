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

人工ニューラルネットワーク（ANN）でできる?$\rightarrow$できる

---

## もうひとつの話題: なんか自動で絵を描くやつが出現

実例は各自いろんなところで調査を

- こいつらはどういう仕組み?
    - 最近のは言語も駆使している（次回）
    - ちょっと古いけど基礎をやりましょう

---

## 視覚・画像とANN

- 映像、画像の特性に特化したANNが存在
    - 特性
       - 2次元（深度があれば3次元、動画でも時間軸を入れると3次元）
       - ある画素の周囲に似た画素がある
- おさらい: ディジタル画像
    - 平面が格子状に分割されて、数字の大小で色の濃さが表される
    （例: 右図。数字はてきとう）
    - カラーの場合はR、G、Bそれぞれについて格子状の数値データ

![bg right:40% 90%](./figs/cat_mono.png)

---

## 画像認識の難しさ

- 同じものが大きく写ったり小さく写ったり回転して写ったり
- 変形したり抽象化されたりデフォルメされたり

![](./figs/dots_varisous.png)

![bg right:30% 90%](./figs/cat_back.png)

---

## CNN

- convolutional neural network
    - テレビ局ではないです
