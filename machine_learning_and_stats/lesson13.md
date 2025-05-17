---
marp: true
---

<!-- footer: "機械学習（と統計）第13回" -->

# 機械学習

## 第13回: 言語と人工ニューラルネットワーク

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 機械学習での言葉の扱い方
- Transformer

---

## 機械学習での言葉の扱い方

- 単語の埋め込み
    - ひとつの単語を次元の大きな（数百〜数千次元の）ベクトルに置き換える
    - 「近い」単語は似たベクトル（内積の値が大きくなるよう）にする
        - 例（てきとうです）
            - おじさん$= (0.9, 0.32, 0.07)$
            - おばさん$= (0.7, 0.55, 0.08)$
            - 不動産$= (0.1, 0.05, 0.88)$
                - 当然、もっと単語は多いので次元は大きい必要がある
- Word2vec
