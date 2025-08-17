---
marp: true
---

<!-- footer: 確率ロボティクス第4回 -->

# 確率ロボティクス第4回: 連続値と多変量

千葉工業大学 上田 隆一

<br />

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 今回の内容

- 連続値に対する確率分布の定義方法
- 多変量の確率分布

---

## ある実験

- ある位置から何度もロボットを4m前進させ、実際に到達した位置$(x,y)$と向き$\theta$の統計をとった
- 知りたいこと: ロボットの到達した座標$(x,y,\theta)$の分布は？
    - 右の図のような分布の図を描きたい
$\qquad\qquad\qquad\qquad$![w:600](./figs/robot_final_pos.png)

![bg right:30% 95%](./figs/prob_dist.png)

---

### 困ること

- 困ること1: $x,y,\theta$が「連続的」
    - 統計をとっても点になるから前ページのようなグラフが描けない
- 困ること2: 確率変数$x,y,\theta$が3つもある
    - こういうことは前回もあったが、分布の形については扱っていない

<center style="padding-top:100px;font-size:120%">どうしましょう？</center>

![bg right:30% 95%](./figs/robot_final_pos_b.png)
