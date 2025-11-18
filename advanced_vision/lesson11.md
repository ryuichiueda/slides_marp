---
marp: true
---

<!-- footer: "アドバンストビジョン第11回" -->

# アドバンストビジョン

## 第11回: NeRFと3D Gaussian splatting

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- SfM（structure from motion）
    - 本当は細かくやるべきだけど概要だけ
- NeRF（neural radiance fields）

---

## SfM

- カメラ画像からカメラの位置・姿勢と被写体の3次元形状を復元する問題・技術
    - 位置・姿勢は以後あわせて「姿勢」と表現
    - 参考: https://demuc.de/papers/schoenberger2016sfm.pdf
- SLAMとの違い
   - Visual SLAMとあまり変わらないが、より被写体の形状に興味がある
       - 基本的なSfMはカメラの移動量を画像だけから求めようとする
       - SLAMはロボットの移動する空間にも興味がある
       - SLAMでは同じ被写体が念入りに撮れないことがある
- ここではCOLMAP[[Schönberger2016]](https://ieeexplore.ieee.org/document/7780814)に基づいて説明
    - [同作者の別の論文のデモ](https://www.youtube.com/watch?v=11awtGWSqQU)

---

### 特徴点を利用したSfMの処理の流れ

- カメラを用意
- 被写体をいろんなところから写して画像を得る
    - 画像$I_{1:N_I}$を得る
- 各画像からSIFT等の特徴点をとる
    - 画像$I_i$に対し、$(\boldsymbol{x}, \boldsymbol{f} )_{1:N_{F_i}}$を得る
        - $\boldsymbol{x}$が画像上の座標、$\boldsymbol{f}$が特徴量のベクトル
- 共通の特徴点を持つ画像のペアを見つけていく
    - ペア: $(I_a, I_b)_{1:N_\text{pair}}$（$1 \le a < b \le N_I$）
    - 特徴量のペアもできる
    （右図。SfMのものじゃないけど）

![bg right:30% 90%](https://upload.wikimedia.org/wikipedia/commons/3/3d/Matching_of_two_images_using_the_SIFT_method.jpg)

<span style="font-size:70%">画像: [CC BY-SA 3.0 by Indif](https://commons.wikimedia.org/wiki/File:Matching_of_two_images_using_the_SIFT_method.jpg)</span>

---

### 特徴点を利用したSfMの処理の流れ（続き）

- 各画像のペア: $(I_a, I_b)$について互いが撮影されたときのカメラの相対位置を計算
    - 相対位置の計算方法（手法により異なる）
        - 基本行列$E$を求める（カメラのキャリブレーションが済んでいる場合）
        - 基礎行列$F$を求める（↑済んでいない場合に対応するとき）
        - 他、ホモグラフィー行列や三焦点テンソルなど
- 世界座標系にひとつずつカメラの姿勢を置いていく
- バンドル調整<span style="color:red">$\Rightarrow$この出力をNeRFに使う</span>
    - graph-based SLAMの要領（最小二乗法）で全カメラの姿勢を調整
- 各画像のピクセルの位置を世界座標系で確定させていく

---

## NeRF（neural radiance fields）[[Mildenhall2020]](https://arxiv.org/abs/2003.08934)

- 前ページのように、カメラの姿勢と画像のペアから3次元空間を復元していく
- 従来のSfMの手法と何が違う？
    - 光の透過も扱えて再現性が高い（論文中に多くの例、比較あり）
- 使用例
    - https://youtu.be/0zE6NXpTNBQ
    - https://youtu.be/lR7XpLLbm0s

---

### 色の表現方法

- ある3次元空間中の点の光（radiance、輝き）を次の関数で表現
    - $(r, g, b) = \text{RGB}(x, y, z, \theta, \phi)$
        - 点の位置と視線の向きで色を決める
        - 図4に視点で色を変える効果の例
    - $\sigma = \sigma(x, y, z)$
        - 点の位置で「密度」を決める
            - 密度が低いほど光が透過
- まとめて$(r, g, b, \sigma) = \boldsymbol{f}_{\boldsymbol{w}}(x,y,z,\theta,\phi)$をANNで表現

![bg right:28% 100%](./figs/color_difference.svg)

---

### 学習方法

1. SfMでどこから撮影したか分かっている画像を用意
2. 画像が撮られた姿勢から$\boldsymbol{f}_{\boldsymbol{w}}$を使って画像を復元
    - 視線上の$(r,g,b,\sigma)$の値から各画素の色を決定
3. 1の画像と2の画像の各ピクセルの2乗誤差を損失関数に

![bg right:40% 100%](./figs/nerf_training.svg)

---

### 構造（論文の図7）

- 基本は全結合層+ReLUで構成
    - 図中の「$\gamma$」についてはあとで
- 入力（3箇所）
    - 最初に位置$\boldsymbol{x} = (x,y,z)$を入力
    - 中間で再度、位置$\boldsymbol{x} = (x,y,z)$を連結
    - 後ろの層で$\boldsymbol{d} = (\theta, \phi)$を連結
- 出力（2箇所）
    - $\boldsymbol{d}$を連結する層の1つを$\sigma$値に
    - 最終層の出力を$(r,g,b)$値に


---

### 図中の「$\gamma$」

- 位置や向きのベクトルを$2L$倍に拡張
    - 論文の実装では$L=10$
        - $\boldsymbol{x}$（3次元）を60次元に
        - $\boldsymbol{d}$（2次元）を40次元に
- 拡張の式（位置埋め込みに似ている）
    - $\boldsymbol{\gamma}(p) = [\sin (2^0\pi p), \cos(2^0\pi p), \sin (2^1\pi p), \cos(2^1\pi p), \dots,$
    $\qquad\qquad\sin (2^{L-1}\pi p), \cos(2^{L-1}\pi p)]$
        - $p$には$x,y,z,\theta,\phi$が入る
- なんで拡張するのか？
    - 値の桁の小さいところも強調して、色の変化量が大きいところの解像度を上げたい（図4に比較）

---

## 3D Gaussian splatting[[Kerbl2023]](https://arxiv.org/pdf/2308.04079)

- NeRFのような光の表現を、ガウス分布を空間中に置いて表現
   - 人工ニューラルネットワークは使わない（使う必要がなかった）
       - 講師の解釈: たぶん局所的な計算で済むのでそんなに複雑な関数（ANN）の表現が不要だった
       - 計算時間も少ない（論文の図1）: NeRFの48時間に対して6分
- [使用例](https://www.youtube.com/watch?v=mD0oBE9LJTQ)
   - 水面への映り込みなどに注目

---

### 空間中に置くガウス分布

- $\mathcal{N}(\boldsymbol{\mu}, \Sigma)$

