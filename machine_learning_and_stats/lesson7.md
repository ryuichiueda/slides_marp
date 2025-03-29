---
marp: true
---

<!-- footer: "機械学習（と統計）第7回" -->

# 機械学習

## 第7回: 法則性の発見: 最小二乗法と回帰											

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- データの法則性
- 最小二乗法
- 回帰

---

### データの法則性

- 右図: 第4回でとりあげたデータ
    - 出典:  [日本病院薬剤師会](https://www.jshp.or.jp/)
    - 共分散を求めた
        - 分布を求めるため
- 今回、次回は別の問題を考える
    - 横軸の値（$x$）に対して、$y = f(x)$を求める
        - 横軸の値に対して縦軸の値はどういう傾向にあるか
        - 横軸のデータの分布は考えない（一様分布状と仮定）

![bg right:40% 100%](./figs/relations.png)

---

### 最小二乗法

- おそらくどこかで勉強したであろう、データへの式の当てはめ
