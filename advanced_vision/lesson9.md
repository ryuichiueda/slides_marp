---
marp: true
---

<!-- footer: "アドバンストビジョン第9回" -->

# アドバンストビジョン

## 第9回: 画像と言語、ロボット制御の融合

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 本題の前に
    - flow matching
- VLA（vision-language-action model）

---

## Flow matching（FL）[[Lipman 2022]](https://arxiv.org/abs/2210.02747)

- 拡散モデルを一般化したもの
- 拡散モデル（下図。再掲）
    - 現実（実際には訓練データ）の分布をガウス分布に変換・逆変換
        - 変換にはノイズを乗せていく方法が取られた


![w:900](./figs/ddpm.svg)
