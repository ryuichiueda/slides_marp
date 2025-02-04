---
marp: true
---

<!-- footer: "機械学習（と統計）第2回" -->

# 機械学習

## 第2回: 期待値

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 確率の使い方
- 期待値の使い方
- 期待値の利用


---

## 確率の使い方

---

### 確率ってなに？

- 聞いたことはあると思うけど、何？
- よくある例
    - コインを投げて表が出る確率は1/2
    - サイコロを振って1の目が出る確率は1/6


---


- 引き続き、代表値で誰を代表にするか議論しましょう
    - 前回: 代表値で誰を代表にするか議論した$\rightarrow$理屈では決まらない

---

## 期待値ってなに

---

## 期待値

- （雑な）定義: なにかばらつく値の平均値を推定、予想した値
    - 問題: 3700円を払い、サイコロの出目に1000をかけただけお金がかえってくるギャンブルがありますが、1回の試行で儲かるお金の期待値は？

---

## 答え

- $1000/6 + 1000\cdot 2/6 + 1000\cdot 3/6 + 1000\cdot 4/6$
$+ 1000 \cdot 5/6 + 1000 \cdot 6/6 - 3700 = 1000(3.5) - 3700$ <span style="color:red">$= -200$</span>


