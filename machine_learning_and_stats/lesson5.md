---
marp: true
---

<!-- footer: "機械学習（と統計）第5回" -->

# 機械学習

## 第5回: ベイズの定理と推定

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- クイズ
- ベイズの定理

---

## クイズ

- なんのことをいっているのでしょう？ヒントをひとつずつ出すので候補をいろいろ書いてみてください。
    * 上に卵が乗っていることがある
    * スープに入っている
    * 日本人はズルズルいわせて食べる
    * 白い

---

### クイズの答えと、答えより重要なこと

- たぶん「うどん」が正解
    - ほかにあるかもしれませんが
- こたえよりも重要なこと: 我々の頭のなかはどうなってる？
    - 脳細胞がなにをやっているかはこの講義の範囲を超える
    - なんとなく「確率」を使ってないでしょうか？
    （どうやって使っているか議論してみましょう）

