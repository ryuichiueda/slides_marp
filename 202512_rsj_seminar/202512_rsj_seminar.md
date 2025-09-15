---
marp: true
---

<!-- footer: "RSJセミナー" -->

# ロボットの制御問題の整理

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 本日の話の動機（これだけで終わらないようにします）
- 探索問題と最適制御の接続
- ベルマン方程式とポントリャーギンの最大原理
- 潜在空間での制御

---

## この発表

- 同じ問題を別のアプローチで解くことによる悲劇
    - 「こっちの方法使えば簡単なのに」
    - ↑人間には大変難しい（自分の専門というものがある）
        - 最近はみなさま超優秀だけど細分化が激しい
- たまには別の分野もみていきましょう
    - 関係性を理解すればすんなり他分野の知見も取り入れられるはず
        - 同じ問題を解いているので
