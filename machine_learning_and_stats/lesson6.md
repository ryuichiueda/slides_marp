---
marp: true
---

<!-- footer: "機械学習（と統計）第6回" -->

# 機械学習

## 第6回: 推定値のあいまいさ

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 共役

---

### ベータ分布（再掲）

- 式: $p(x) = \dfrac{ x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)} = \eta x^{\alpha-1}(1-x)^{\beta-1}$
    - $B$はベータ関数というややこしい関数
- コインの表、裏がそれぞれ$(\alpha-1)$、$(\beta-1)$回出たときに、表が出る確率の分布
    - 投げるほど分布が尖っていく
        - 数学的な解釈: ある確率に収束していく
        - 生物的な解釈: <span style="color:red">ある確率なのではないかとだんだん確信していく</span>


<center>今日はこれを掘り下げます</center>

![bg right:30% 90%](./figs/beta.png)

---

### 問題

- 題材: ボールを投げて頭上の籠に入れる玉入れロボットを作りました。これから実験で籠に入る確率を求めます。
    <br />
- 最初の問題: まず1回実験したら成功しました。成功率はどれだけでしょうか?
    - 話し合ってみましょう

