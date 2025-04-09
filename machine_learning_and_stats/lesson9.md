---
marp: true
---

<!-- footer: "機械学習（と統計）第9回" -->

# 機械学習

## 第9回: 動物におけるクラスタリングの役割と古典的手法

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- クラスタリングの重要性
- 古典的手法

---

## クラスタリングの重要性

- 第1回のおさらい
    - 右の図は何に見えますか
    - なんで猫に見えるのか？
- たぶん丸い部分1つと三角の部分1つに点をまとめている
    - [研究例](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.riken.jp/medialibrary/riken/pr/press/2001/20010727_1/20010727_1.pdf)


![bg right:40% 60%](./figs/dots.png)

---

### まとめると何がわかるか

- たとえば目の前になにがあるかを知りたい場合
    - やらなければいけないこと: 視細胞の反応$\longrightarrow$認識対象（猫など）
        - 単なる多数の刺激$\longrightarrow$「猫」という単語
        - <span style="color:red">この過程で「まとめる」という作業が脳内で必要となる</span>
- 左図: 実物の畑の作物と、茎と葉を分類した画像
    - 人間は右のような分類結果を頭の中に持っているし、実際に（時間をかければ）描ける

![bg right:30% 78%](./figs/leaf_stem.png)

---

## クラスタリングの古典的手法

- k-means
- EM法


---

## k-means

