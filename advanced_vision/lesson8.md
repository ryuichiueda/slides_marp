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
- Diffusion Transformer
- CLIP

---

## Vision Transformer（ViT）[[Dosovitskiy 2020]](https://arxiv.org/abs/2010.11929)

- Transformerのエンコーダを画像に転用
    - 画像をブロック状に切って単語のように扱う（右図）
    - 右図のCLS: クラストークン
        - 文の分類と同じ
- 画像をブロック状に扱うのはCNNと同じだが、そのあとが違う
    - CNNは遠くのブロックの関係性を見るのが苦手

[<span style="font-size:70%">画像: CC-BY-4.0 by Daniel Voigt Godoy</span>](https://commons.wikimedia.org/wiki/File:Vision_Transformer.png)<span style="font-size:70%">（[[Dosovitskiy 2020]](https://arxiv.org/abs/2010.11929)のFig.1にも構成図）</span>

![bg right:40% 100%](https://upload.wikimedia.org/wikipedia/commons/9/93/Vision_Transformer.png)


---

### ViTの構造

- オリジナルの論文には複数の構造
    - ViT-Base: 層の数12、ベクトルの長さ: 768、識別用の全結合層の大きさ3072
- 全結合層: 2層、GeLUを使用


---

### トークンに対応するベクトルの作り方

- 画像を$P \times P$画素のブロックに区切る
    - 例: $P=16$: ベクトルの次元は$16\times 16 \times 3 = 768$に
        - 3はチャンネルの数（RGB）
    - 位置の埋め込みも行う
        - ただし固定値ではなく、パラメータは学習対象
- 画像の理解
    - 局所的な理解: ベクトルの中
    - 大域的な理解: 自己注意機構で学習

---

### 事前学習の方法 

- 教師あり学習で分類問題を解く
    - 言語と違って教師なし（BERTのような穴埋め）はあまり効果がない
- オリジナルの論文で用いられた訓練データ
    - JFT-300M
        - 3億枚の画像、18291クラスのデータセット
    - ImageNet-21k
        - 1400万枚の画像、21841クラスのデータセット
- 訓練データが多いと高い性能を発揮（JFT-300Mのほうがよかった）


---

### ViTの機能のしかた

- 位置の埋め込みに関して
    - [[Dosovitskiy 2020]](https://arxiv.org/abs/2010.11929)のFig. 7左
    - 画像処理で使われる基底関数のようなものができている
- どこを見て判断しているか
    - [[Dosovitskiy 2020]](https://arxiv.org/abs/2010.11929)のFig. 6、Fig. 7右
    - 自己注意機構のヘッド（マルチヘッド注意機構のヘッド）には、入力に近い層ですでに大域的なものとローカルなものなどバリエーションが出る
        - 大域的なものはCNNの入力に近い方のたたみ込み層に類似
    - 入力から遠ざかるとより大域的に

---

## Diffusion Transformer（DiT）[[Peebles 2022]](https://arxiv.org/abs/2212.09748)

- 拡散モデル+Transformer
    - さらに潜在空間に情報を圧縮する潜在拡散モデルも使用
    - ラベルを入力して出力をコントロール
- 入力
    - 自己注意機構への入力
        - ノイズを載せた訓練画像（VAEで圧縮されているもの）
            - サイズを落とすためにVAEを使用
    - 層正則化のあとの出力に注入（AdaLN機構）
        - 時刻
        - ラベル

### Adaptive Instance Normalization（AdaIN）
