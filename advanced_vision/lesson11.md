---
marp: true
---

<!-- footer: "アドバンストビジョン第11回" -->

# アドバンストビジョン

## 第11回: CLIP (Contrastive Language-Image Pretraining)

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- CLIP

---

## 画像認識の方法

- よく行われてきた方法
    - 写真をあつめる
    - 写真に写っているものをラベル付けする
- 上記方法の問題
    - めんどくさい
    - ラベルのあるものしか認識できない

---

### Contrastive Language-Image Pre-training (CLIP)

- テキストと画像の関連性を学習したモデル（[論文](https://arxiv.org/pdf/2103.00020)）
- [図](https://en.wikipedia.org/wiki/Contrastive_Language-Image_Pre-training)
- 学習方法
    1. 画像と画像の内容を説明する文を準備
    2. ViTを使って画像をエンコーディング
    3. Transformerを使って文をエンコーディング
    4. エンコーディングされたデータ（埋め込み）同士の相関を学習
$\rightarrow$画像から文、文から画像などの変換が可能
