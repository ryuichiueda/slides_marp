---
marp: true
---

<!-- footer: 千葉工業大学・松本工業高校連携授業 -->

# 移動ロボット入門

千葉工業大学 上田 隆一


---

<!-- paginate: true -->

## 自己紹介

- 上田隆一という名前です
- ロボットの研究者です
- 長くなるので[続きはウェブで](https://ja.wikipedia.org/wiki/上田隆一)

---

## 宣伝: 本買って

- 左から順に
    - Linuxの本
    - ロボットの本（今日話する内容）
    - ロボットで使う数学の本


<img width="20%" src="shellgei160.jpg" />  <img width="20%" src="lnpr.jpg" />  <img width="20%" src="robot_stats.png" />

---

## 今日のテーマ

- 知能ってなんだろ？

---

## ある問題

- 登場人物（人物じゃないけど）
    - うちの猫様
    - 美味しいおやつ
    - 通路・扉
        - 扉は猫には開けられません
- 猫様はおやつまでたどり着けるだろうか？

![bg right:44% 100%](problem.png)

---

## 答え: たまにしかできない

- だいたい扉の下に手を突っ込んでガリガリして諦める

<iframe width="560" height="315" src="https://www.youtube.com/embed/JmONWX1IWAk?si=kmL8VdtQict3X7Rn" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## ここで質問

- 人間なら簡単なのに猫には難しいのはなんで？
- 逆に言うと、おやつのところまで行くには何が必要？
    - 人間は何をしている？

---

## 答えあわせ

- 俯瞰ができていない疑惑
    - 頭の中に<span style="color:red">地図</span>はあるだろうか？
    - 自分の見ている風景が地図のどこに相当するだろうか？
- 計画ができていないのは確実
    - 頭の中でおやつの場所に行くまでの<span style="color:red">手順</span>が思い浮かぶだろうか？

![bg right:44% 100%](map.png)

---

## 移動ロボットをどう作る？

- 複雑な道を目的地まで行くロボットをプログラムしたい。どうやって？
    - 前のページと同じで「地図」と「手順の算出（計画）」が必要
    - さらには猫や人間の目に相当する機能を実装しなければならない
        - カメラだけじゃなくて画像から必要な情報を計算するソフトウェアも


---

## 頭の中の地図

