---
marp: true
---

<!-- footer: "アドバンストビジョン第3回" -->

# アドバイストビジョン

## 第4回: 画像の識別と生成の基礎II

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- GAN
- 変分オートエンコーダ
- 条件付き変分オートエンコーダ

---

## GAN（generative adversarial networks）

- 敵対的生成ネットワーク
    - 「絵を描く人工ニューラルネットワーク」のブームの発端
    - それ以外にも音声やソフトウェアを作り出すなどの用途
- 「敵対的」とは何?（人類の敵ではない）
    - ふたつのANNを準備
        - 生成ネットワーク（generator）: 何かを作るANN
        - 識別ネットワーク（discriminator）: 入力が生成ネットワークの生成物かどうかを判断するANN
    - 生成ネットワークと識別ネットワークが互いに競う
- [元の論文](https://papers.nips.cc/paper_files/paper/2014/file/f033ed80deb0234979a61f95710dbe25-Paper.pdf)

---

### ネットワーク構造の例（DCGAN）

- Deep Convlutional GAN（DCGAN）[[Radford 2015]](https://arxiv.org/pdf/1511.06434) <a href="https://www.researchgate.net/figure/The-architecture-of-the-generator-and-the-discriminator-in-a-DCGAN-model-FSC-is-the_fig4_343597759"><span style="font-size:70%">画像: Zhang et al. CC-BY 4.0</span></a>
    - 上: 生成ネットワーク<span style="font-size:70%">（FSC: fractionally-strided convolution)</span>
    - 下: 識別ネットワーク
![w:800](./figs/dcgan-cc-by-4.0-by_zhang.png)


---

### DCGANの生成ネットワーク

- 構造: オートエンコーダのデコーダ
    - 入力: ランダムなベクトル（100次元）
        - <span style="color:red">潜在空間のベクトルに相当</span>
            - ↑わからん人は前回のオートエンコーダに戻りましょう
    - 出力: 画像
- 出力の画像は最初はでたらめ
    - ある訓練をすると画像が生成されるように


![bg right:40% 100%](./figs/dcgan-cc-by-4.0-by_zhang.png)

---

### DCGANの識別ネットワーク

- 構造: エンコーダに似ているが出力は1bit
    - 入力: 生成ネットワークの画像 or 訓練のために用意した画像
    - 出力: 「本物」or「偽物」を表す数値（1か0）
        - 生成ネットワークの画像のとき「偽物」
        - 訓練の画像のとき「本物」
- 出力は最初はでたらめ
    - 当てずっぽう


![bg right:40% 100%](./figs/dcgan-cc-by-4.0-by_zhang.png)


---

### 生成/識別ネットワークを競わせる

- 損失関数
    - 識別ネットワークが正解したら生成ネットワークの損失
    - 識別ネットワークが不正解だったら識別ネットワークの損失
- 最初はどっちのネットワークもポンコツ
    - 生成ネットワーク: ノイズ画像
    - 識別ネットワーク: でたらめの識別結果
- 損失関数から学習
    - 生成ネットワーク: 識別ネットワークを欺くために画像に模様をつけていく
    - 識別ネットワーク: 識別能力を少しずつ上げていく

<center>これで生成ネットワークが画像を出力できるようになる <a href="https://arxiv.org/pdf/1511.06434">例</a></center>

---

## 変分オートエンコーダ[[Kingma 2013]](https://arxiv.org/abs/1312.6114)

- オートエンコーダをより表現力豊かにする方法
- 改善したいオートエンコーダの性質
    - 潜在空間でのベクトルの分布に隙間
        - 訓練データに対応するベクトルの間に
    - 隙間の問題
        - 隙間のベクトルをデコーダに渡すと、中間というよりは重ね合わせのような出力
            - 例: 犬と猫の中間のベクトルから、その中間のような動物の画像を出力したい
            $\rightarrow$単に足して2で割ったような不自然なものに

![bg right:30% 100%](./figs/latent_space_problem.png)

---

### 変分オートエンコーダでの潜在空間の扱い

- 仮定
    - 潜在空間のベクトル$\boldsymbol{z}$の分布は標準正規分布に従う
        - 空間が無限なのでデータが散らないように縛りを設ける
    - エンコーダへの入力$\boldsymbol{x}$に対し、$P(\boldsymbol{z}|\boldsymbol{x})$の分布も正規分布に従う
        - これは学習のための仮定
- 仮定に基づいて学習すると
    - $\boldsymbol{z}$の隙間があかずに原点付近に集まる
    - $P(\boldsymbol{z})$の分布のなかに$P(\boldsymbol{z}|$物の種別$)$のような分布ができる

![bg right:40% 100%](./figs/latent_space_dist.png)

---

### 隙間の問題の解決

- デコーダで生成されるデータに隙間ができにくい
    - [[Kingma 2013]](https://arxiv.org/abs/1312.6114)の中の図4
    - [Kingma氏のデモサイトの例](https://dpkingma.com/sgvb_mnist_demo/demo.html)
- ただしGANよりぼやけやすい

### 変分オートエンコーダの構造

- 右図（エンコーダの先に雑音の層を追加）
    - $P(\boldsymbol{z})$を標準正規分布に制限するための項は損失関数に
    - 本来は変分ベイズなどの理論が背景に
        - 確率ロボティクスの講義で一部説明

![bg right:35% 100%](./figs/vae.png)

---

### GANの応用

- [pix2pix](https://arxiv.org/pdf/1611.07004): 入力にノイズではなく画像を入力$\rightarrow$画像を変換するように学習
- ロボットでの使用例（深度カメラに映った植物の茎と葉を分別）
    ![w:870](figs/pix2pix.png)
 
---

### 拡散モデル

- GANと同じく画像を生成する技術
    - [Stable Diffusion](https://stablediffusionweb.com/ja/app/image-generator)の理論的な背景（の半分）
        - もう半分（言葉による指示）は来週
- 画像生成するANNの作り方
    - ANNに画像のノイズを消す訓練をさせる
    - ランダムなノイズ画像を入力すると元の画像を無理やり想像して画像を生成する


---

## まとめ

- CNN、GAN、拡散モデルなど画像を扱うANNを勉強
    - 他、vision transformerなど2, 3年に一度、画期的な手法が発表されている
        - transformerは次回
