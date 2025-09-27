---
marp: true
---

<!-- footer: "アドバンストビジョン第6回" -->

# アドバンストビジョン

## 第8回: 画像とTransformer

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- Vision Transformer
- CLIP

---

### Vision Transformer（ViT）

- Transformerを画像に転用
    - 画像をブロック状に切って単語のように扱う（右図）
    - 右図のCLS: クラストークン
        - 文の分類と同じ
- 画像をブロック状に扱うのはCNNと同じだが、そのあとが違う
    - CNNは遠くのブロックの関係性を見るのが苦手

[<span style="font-size:70%">画像: CC-BY-4.0 by Daniel Voigt Godoy</span>](https://commons.wikimedia.org/wiki/File:Vision_Transformer.png)

![bg right:40% 100%](https://upload.wikimedia.org/wikipedia/commons/9/93/Vision_Transformer.png)



---

### ViT（補足）

- 位置の埋め込みのパラメータは学習対象
- 位置の埋め込みは学習対象

