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
   - Visual SLAMとあまり変わらないが、SLAMのほうがより広い領域を対象に
