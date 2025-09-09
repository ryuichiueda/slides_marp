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
- その1: <span style="color:red">状態方程式</span>
    - $\boldsymbol{x}_t = \boldsymbol{f}( \boldsymbol{x}_{t-1}, \boldsymbol{u}_t) + \boldsymbol{\varepsilon}$
        - $\boldsymbol{\varepsilon}$: 移動量の想定と実際とのズレ（雑音）
        - $\boldsymbol{f}$: <span style="color:red">状態遷移関数</span>
- その2: 確率分布による表現
    - $\boldsymbol{x}_t \sim p( \boldsymbol{x} | \boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$
        - $p( \boldsymbol{x} | \boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$: <span style="color:red">状態遷移分布</span>

![bg right:30% 100%](./figs/motion_error_representation.png)

---

### $\boldsymbol{x}$と$\boldsymbol{u}$の関係性の表現（続き）

- 前者で済む場合は前者で済ませるが、後者のほうが抽象的で扱える範囲が広い
    - 前者（現代制御的）: $\boldsymbol{x}_t = \boldsymbol{f}( \boldsymbol{x}_{t-1}, \boldsymbol{u}_t) + \boldsymbol{\varepsilon}$
    - 後者（確率ロボティクス的）: $\boldsymbol{x}_t \sim p( \boldsymbol{x} | \boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$
        - 後者の利点
            - 雑音が大きくてもよい
            - 遷移後の分布が分裂してもよい
            - $\boldsymbol{\varepsilon}$と$\boldsymbol{f}$が独立していなくてもよい
            - ・・・
- 講師の個人的な見解:
確率ロボティクスとは現代制御の一般化

![bg right:25% 100%](./figs/motion_error_representation.png)

---

### マルコフ性

- 状態遷移の分布が遷移直前の状態（の分布）だけで決まること
- 前ページの2つの表現はどちらもマルコフ性を仮定
    - $\boldsymbol{x}_t = \boldsymbol{f}( \boldsymbol{x}_{t-1}, \boldsymbol{u}_t) + \boldsymbol{\varepsilon}$
    - $\boldsymbol{x}_t \sim p( \boldsymbol{x} | \boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$
    - いずれの表現方法でも$\boldsymbol{x}_{t-2}$や$\boldsymbol{u}_{t-1}$が式中にない
    $\Longrightarrow$つぎの姿勢は$\boldsymbol{x}_{t-1}$と$\boldsymbol{u}_t$だけで決まる（<span style="color:red">あくまで仮定</span>）
- 注意: ロボットでは必ずしも成り立たない
    - 長時間動かしてきた（状態遷移を経た）ロボットは熱で動きが悪くなる
    - 静止した状態のロボットと、すでに動いているロボットの挙動の違い
    （無視できない場合: 補正をかけたり温度や状況を表す変数を状態に組み入れたり）

---

### 状態遷移後の分布の形

- $p_{t-1}$と$p_{t}$の関係は？
    - 状態遷移分布$p( \boldsymbol{x} | \boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$を使って表現してみましょう
    - 期待値を使った表現にできます
- 答え
    * $p_t(\boldsymbol{x}) = p(\boldsymbol{x} | \boldsymbol{u}_{1:t}, p_0)$
    $= \int_{X} p(\boldsymbol{x}, \boldsymbol{x}_{t-1} | \boldsymbol{u}_{1:t}, p_0)\text{d}\boldsymbol{x}_{t-1}$
    $= \int_{X} p(\boldsymbol{x}| \boldsymbol{x}_{t-1} , \boldsymbol{u}_{1:t}, p_0) p(\boldsymbol{x}_{t-1} | \boldsymbol{u}_{1:t}, p_0) \text{d}\boldsymbol{x}_{t-1}$
    $= \int_{X} p(\boldsymbol{x}| \boldsymbol{x}_{t-1} , \boldsymbol{u}_t) p(\boldsymbol{x}_{t-1} | \boldsymbol{u}_{1:t-1}, p_0) \text{d}\boldsymbol{x}_{t-1}$
    $= \int_{X} p(\boldsymbol{x}| \boldsymbol{x}_{t-1} , \boldsymbol{u}_t) p_{t-1}(\boldsymbol{x}_{t-1}) \text{d}\boldsymbol{x}_{t-1}$
    $= \big\langle p(\boldsymbol{x}| \boldsymbol{x}_{t-1} , \boldsymbol{u}_t) \big\rangle_{p_{t-1}(\boldsymbol{x}_{t-1}) }$

<span style="color:red">上式を実装$\Rightarrow$ロボットの動きが予測できる（でもどうやって？）</span>

![bg right:20% 90%](./figs/distribution_motion.png)

---

## 線形なロボットの位置予測

- 右図のように向きがなくて$xy$平面を動き回るロボットを考える
- $\boldsymbol{u}$に対する移動量の分布$p(\Delta \boldsymbol{x} | \boldsymbol{u})$が既知でガウス分布
- $p_{t-1}$から$p_t$を導出してみましょう

![bg right:25% 100%](./figs/linear_motion.png)
