---
marp: true
---

<!-- footer: "アドバンストビジョン第11回" -->

# アドバンストビジョン

## 第11回: SfMとNeRF

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- SfM（structure from motion）
- NeRF（neural radiance fields）

---

## SfM

- カメラ画像からカメラの位置・姿勢と被写体の3次元形状を復元する問題・技術
    - 位置・姿勢は以後あわせて「姿勢」と表現
    - 参考: https://demuc.de/papers/schoenberger2016sfm.pdf
- SLAMとの違い
   - Visual SLAMとあまり変わらないが、より被写体の形状に興味がある
       - SLAMはロボットの移動する空間にも興味がある

---

### 特徴点を利用したSfMの処理の流れ

- カメラを用意（内部パラメータをキャリブレーションしておく）
- 被写体をいろんなところから写して画像を得る
    - 画像$I_{1:N_I}$を得る
- 各画像からSIFT等の特徴点をとる
    - 画像$I_i$に対し、$(\boldsymbol{x}, \boldsymbol{f} )_{1:N_{F_i}}$

