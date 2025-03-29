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
        - 分布を当てはめるため
- 今回、次回は別の問題を考える
    - 横軸の値（$x$）に対して、縦軸の値の傾向$y = f(x)$を求める<span style="color:red">（回帰）</span>
        - 横軸の値に対して縦軸の値はどういう傾向にあるか
        - ※分布を考えることと本質的な違いはそれほどない。道具の違い。

![bg right:40% 100%](./figs/relations.png)

---

### 回帰が便利な例

- 時系列データ
    - 時間を分布で扱う必要はない
- なにかしらの関数$y = f(x)$で縦軸の値が決まっていそうな場合

---

### 最小二乗法

- おそらくどこかで勉強したであろう、データへの式の当てはめ
