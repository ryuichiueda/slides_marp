---
marp: true
---

<!-- footer: 確率ロボティクス第6回 -->

# 確率ロボティクス第6回: 動く確率分布（その1）

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

- 動く物体と確率
    - 台風の予報円のようなものを考える


![bg right:30% 95%](https://upload.wikimedia.org/wikipedia/commons/d/d1/2022%E5%B9%B4%E5%8F%B0%E9%A2%A814%E5%8F%B7%E3%81%AE%E4%BA%88%E5%A0%B1%E5%86%86_%28%E6%B0%97%E8%B1%A1%E5%BA%81%29.jpg)

<span style="font-size:50%"><a href="https://ja.wikipedia.org/wiki/%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB:2022%E5%B9%B4%E5%8F%B0%E9%A2%A814%E5%8F%B7%E3%81%AE%E4%BA%88%E5%A0%B1%E5%86%86_(%E6%B0%97%E8%B1%A1%E5%BA%81).jpg">画像: 気象庁 CC BY-SA 4.0</a></span>

---

## 動く物体と確率

- おさらい
    - 4章ではロボットが動いたあとの位置、向きの確率分布を考えた
- 今回考えること
    - この確率分布はロボットと一緒に動いてきた
        - ロボットが動けば中心も動く
        - ロボットの動きには雑音があるので分布が広がる


$\Longrightarrow$<span style="color:red">どんなふうに動いてきたんだろう？</span>

![bg right:30% 95%](./figs/robot_final_pos_ellipse.png)

---

### 準備1: 離散時間系の導入

- ロボットの「考える周期」で時間を離散化しましょう
    - 連続的な時間で確率分布の変化を考えるのは大変なので
    - 人が操作するロボットではなく自律ロボット
- 「考える周期」
    - 動きの判断をする1周期に番号をつけて時間の1単位に
        - $t=0,1,2,\dots$
- ロボットの位置の表現（下図）
    - $\boldsymbol{x}_0, \boldsymbol{x}_1, \boldsymbol{x}_2, \dots$
- 位置・向き（あわせて「<span style="color:red">姿勢</span>」あるいは「<span style="color:red">状態</span>」）の分布
    - $p_0, p_1, p_2, \dots$ <span style="color:red">$\Longleftarrow$これを計算したい</span>
    - 補足: 「姿勢」はロボティクス用語、「状態」は制御用語

![bg right:20% 95%](./figs/trajectory.png)

---

### 準備2: ロボットの移動のモデル化

- 離散時刻ごとに、ロボットはモータに送る制御指令を変えると仮定
    - 時刻$t$の制御指令を$\boldsymbol{u}_{t+1}$と表現（添え字がずれるので注意）
        - 「時刻$t+1$までの制御指令」と解釈
- $\boldsymbol{u}_{t+1}$の具体例はあとで
    - しばらく一般化して考えましょう

![bg right:30% 95%](./figs/control_input.png)

---

### $\boldsymbol{x}$と$\boldsymbol{u}$の関係性の表現

- 本講義では2つの表現方法を使い分け
- その1: <span style="color:red">状態方程式</span>（現代制御的）
    - $\boldsymbol{x}_t = \boldsymbol{f}( \boldsymbol{x}_{t-1}, \boldsymbol{u}_t) + \boldsymbol{\varepsilon}$
        - $\boldsymbol{\varepsilon}$: 移動量の想定と実際とのズレ（雑音）
- その2: 確率分布による表現（<span style="color:red">確率ロボティクス</span>）
    - $\boldsymbol{x}_t \sim p( \boldsymbol{x} | \boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$
        - $p( \boldsymbol{x} | \boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$: <span style="color:red">状態遷移分布</span>
- 前者で済む場合は前者で済ますが、後者のほうが抽象的で扱える範囲が広い
    - 雑音が大きくてもよい/遷移後の分布が分裂してもよい/$\boldsymbol{\varepsilon}$と$\boldsymbol{f}$が独立していなくてもよい・・・

![bg right:30% 100%](./figs/motion_error_representation.png)

---

### マルコフ性

- いずれの表現方法でも$\boldsymbol{x}_{t-2}$や$\boldsymbol{u}_{t-1}$が式中にない
    - $\boldsymbol{x}_t = \boldsymbol{f}( \boldsymbol{x}_{t-1}, \boldsymbol{u}_t) + \boldsymbol{\varepsilon}$
    - $\boldsymbol{x}_t \sim p( \boldsymbol{x} | \boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$
    $\Longrightarrow$つぎの姿勢は$\boldsymbol{x}_{t-1}$と$\boldsymbol{u}_t$だけで決まる（<span style="color:red">あくまで仮定</span>）
