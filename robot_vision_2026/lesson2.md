---
marp: true
---

<!-- footer: "ロボットビジョン第2回" -->

# ロボットビジョン

## 第2回: 人工ニューラルネットワークの学習

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 最小二乗法
- 人工ニューラルネットワークをどのように学習させるか

---

### 前回残った問題: どう学習するか?

- 動物は生まれたときにある程度プログラミングされた状態だが・・・
    - そのあと成長しても神経細胞は基本的に増えない
    - 猫を識別するにはニューラルネットワークに変更を加えないといけない
    - 頭を開けて配線するわけにはいかない

<center style="color:red">どうやるの?</center>

---

### 学習の方法: パラメータを変える

- 例題: $x_1 + 2 x_2 + 3 x_3 \ge 3$なら$1$を出力、そうでなければ$0$を出力するように人工ニューロンを学習させたい
    - 最初、パラメータはあてずっぽ（右図上）
- 基本的な方法
    1. 何か入力して出力と正解の「<span style="color:red">ずれ</span>」を観測する
        - 例えば上のニューロンに$(x_1, x_2, x_3) = (1, 0, 0)$を入れると$1$が出てくる（$0$が出てきてほしいのに）
    2. ずれを小さくするようにパラメータを変える
        - この場合はたとえば$w_1 = 1.9$とすると$0$に

これを全ニューロンに対してやる

![bg right:25% 90%](../machine_learning_2026/figs/simple_ann_learning.png)

---

### ずれ: <span style="color:red">損失関数</span>

- 損失関数の定義$\mathcal{L}(w_{1:n} |$データ$)$
    - $w_{1:n}$: パラメータ（前ページの例の場合は$b$も$w_4$などにして含める）
- ずれの減らし方
    - 損失関数を微分$\nabla \mathcal{L}(w_{1:n} |$データ$) = \left( \dfrac{\partial\mathcal{L}}{\partial w_0},  \dfrac{\partial\mathcal{L}}{\partial w_1}, \dots, \dfrac{\partial\mathcal{L}}{\partial w_n} \right)$
    - <span style="color:red">$\Delta w_{1:n} = - \alpha \nabla \mathcal{L}(w_{1:n}|$データ$)$</span>でパラメータを変更
- データは正解のものをたくさん準備
    - <span style="color:red">訓練データ</span>

---

### 損失関数の例

- 2ページ前のものの場合
    - ニューロンを関数で表すと$y = f(x_{1:3}| w_{1:3},b)$
        - $y$は$0$か$1$
- $\mathcal{L}(w_{1:3}, b | x'_{1:3}, y') = \{f(x'_{1:3}| w_{1:3},b) - y'\}^2$
    - 実際に観測された入出力$(x'_{1:3}, y')$に対し、$x'_{1:3}$に対する正解$f(x_{1:3}| w_{1:3},b)$との2乗誤差をとる

![bg right:25% 90%](../machine_learning_2026/figs/simple_ann_learning.png)

---

### ANNのパラメータ更新: <span style="color:red">誤差逆伝播法</span>


- 出力側の誤差をどんどん入力側に送っていく
    - 送られてきた誤差が小さくなるように各層のパラメータを変える
        - <span style="color:red">各層で偏微分しても前ページの計算が成立</span>

<center><img width=700 src="../machine_learning_2026/figs/back_propagation.png" /></center>

---

### 誤差の送り方

- 1入力1出力の層の場合
    - ある層の計算: $y = f(x | w_{1:n})$のとき
    （$x$: 入力、$y$: 出力）
    - 上流に送る誤差: <span style="color:red">$\Delta\mathcal{L}_x = \dfrac{\partial f}{\partial x}\Delta\mathcal{L}_y$</span>
        - 下流から来た誤差: $\Delta \mathcal{L}_y$
- アフィンレイヤーの例: $f(x) = w x - b \Longrightarrow \Delta\mathcal{L}_x = w \Delta\mathcal{L}_y$
    - 考え方: $w$倍になって出ていく層は入力の誤差の影響力が$w$倍

![bg right:25% 90%](../machine_learning_2026/figs/back_propagation_diff.png)

---

### 多入力・多出力のアフィンレイヤーの場合

- $\boldsymbol{y} = \boldsymbol{f}(\boldsymbol{x}) = \boldsymbol{x}W - \boldsymbol{b}$
- 行列の計算に
    - <span style="color:red">$\Delta\mathcal{L}_\boldsymbol{x} = \Delta\mathcal{L}_\boldsymbol{y} \dfrac{\partial \boldsymbol{f}}{\partial \boldsymbol{x}} = \Delta\mathcal{L}_\boldsymbol{y} W^\top$</span>


![bg right:35% 90%](../machine_learning_2026/figs/back_propagation_affine.svg)

---

### 閾値処理の層の誤差逆伝播（1/2）

- ステップ関数は微分できないので無理
- 代わりにシグモイド関数で微妙にアナログに
    - $y_i = \dfrac{1}{1 + e^{-x_i}}$（$i$: 入出力のインデックス）
- 下図青線: シグモイド関数のグラフ
    - 緑はこれまでのステップ関数
    ![w:300](../machine_learning_2026/figs/sigmoid.png)
    - 注意: 現在は本来は微分できない関数も使用されることがある

![bg right:30% 100%](../machine_learning_2026/figs/sigmoid_layer.png)

---

### 閾値処理の層の誤差逆伝播（2/2）

- シグモイド関数について、上流に送る誤差を計算してみましょう
    - $y_i = f(x_i) = (1 + e^{-x_i})^{-1}$
    - 上流に送る誤差（再掲）: $\Delta\mathcal{L}_x = \dfrac{\partial f}{\partial x}\Delta\mathcal{L}_y$
- $f$を（偏）微分してみましょう
    - $\dfrac{\partial f}{\partial x} = -1\cdot(1 + e^{-x})^{-2}(-e^{-x})$
    $= (1+e^{-x})^{-2}e^{-x} = h^2(h^{-1}-1) = h(1 - h)$
- $y_i = h(x_i)$なので<span style="color:red">$\Delta\mathcal{L}_x = y_i(1 - y_i)\Delta\mathcal{L}_y$</span>


---

### パラメータをどう変えるか?

- 伝播してきた誤差$\Delta \mathcal{L}_y$が減る方向にパラメータを変える
- 1入力1出力の層の場合
    - ある層の計算: $y = f(x | w_{1:n})$のとき
    （$x$: 入力、$y$: 出力）
    - パラメータの変更: $w_i \longleftarrow w_i - \alpha \dfrac{\partial f}{\partial w_i}\Bigg|_x \Delta \mathcal{L}_y$
- 右のアフィンレイヤー（$y = wx - b$）の例
    - $w = 2$<span style="color:red">$- \alpha 9/10\cdot 1/3$</span>（重みが減る）
    - $b = 1/10$<span style="color:red">$+ \alpha 1/3$</span>（閾値が上がる）


![bg right:25% 90%](../machine_learning_2026/figs/back_propagation_diff.png)


---

### アフィンレイヤーでのパラメータ更新（一般的な式）

- アフィンレイヤー（再掲）: $\boldsymbol{y} = \boldsymbol{f}(\boldsymbol{x}) = \boldsymbol{x}W - \boldsymbol{b}$
    - $W  \longleftarrow  W -  \alpha\Delta \mathcal{L}_\boldsymbol{y} \dfrac{\partial \boldsymbol{f}}{\partial W} = W- \alpha\boldsymbol{x}^\top \Delta \mathcal{L}_\boldsymbol{y}$
    - $\boldsymbol{b} \longleftarrow \boldsymbol{b} - \alpha \Delta\mathcal{L}_\boldsymbol{y} \dfrac{\partial \boldsymbol{f}}{\partial \boldsymbol{b}} =  \boldsymbol{b} + \alpha \Delta \mathcal{L}_\boldsymbol{y}$

![bg right:35% 90%](../machine_learning_2026/figs/back_propagation_affine.svg)

---


### 問題: 先述のANNのパラメータ修正

- $x_1 + 2 x_2 + 3 x_3 \ge 3$なら$1$を出力、そうでなければ$0$を出力させたい
    - 右図上の状態から右図下の状態にもっていきたい
- 修正のための式（p. 23のもの）: 
    - $w_i \leftarrow w_i- \alpha$入力値$\cdot$誤差
    - $b \leftarrow b+ \alpha$誤差
- $\alpha=0.5$で（早く収束させるため大きめ）
- $(x_1, x_2, x_3) = (1, 0, 0)$を入力してパラメータを修正してみましょう


![bg right:25% 90%](../machine_learning_2026/figs/simple_ann_learning.png)


---

### 答え

- 計算（再掲）
    - $w_i \leftarrow w_i- \alpha$入力値$\cdot$誤差
    - $b \leftarrow b+ \alpha$誤差

- $(x_1, x_2, x_3) = (1, 0, 0)$を入力$\rightarrow$出力$1$、誤差$1$
    - $w_1 = 2 - 1/2 \cdot 1 \cdot 1 = 1.5$（$1$に近づく）
    - $w_2 = w_3 = 2$（そのまま）
    - $b = 2 + \alpha1 = 2.5$（$3$に近づく）
- 次に$(x_1, x_2, x_3) = (0, 0, 1)$を入力すると？

![bg right:30% 90%](../machine_learning_2026/figs/simple_ann_learning_modify.png)

---

### 答え

- 計算（再掲）
    - $w_i \leftarrow w_i- \alpha$入力値$\cdot$誤差
    - $b \leftarrow b+ \alpha$誤差

- $(x_1, x_2, x_3) = (0, 0, 1)$を入力$\rightarrow$出力$0$、誤差$-1$
    - $w_1, w_2$はそのまま
    - $w_3 = 2 - 0.5 \cdot 1 \cdot (-1) = 2.5$（$3$に近づく）
    - $b = 2.5 + 0.5 (-1) = 2$
        - $b$は$3$から遠ざかる。そういう場合もある。
- できる人は前方のニューロンに送る誤差も計算を

![bg right:30% 90%](../machine_learning_2026/figs/simple_ann_learning_modify2.png)


---

## まとめ

- 人工ニューラルネットワーク
    - ニューロンの組み合わせでプログラムできる
    - 誤差逆伝播で学習ができる
- 次回以降で応用を見ていきましょう

---

## 補足: スキップ（残差）接続

- あるレイヤーの出力を次の層だけでなく、
別の層にも入力する接続方法
    - 入力に挟まれた層は入出力の差分を
    学習することに
- スキップ接続の有無: 初期の学習の容易さに影響
    - スキップ接続なし: 最初は$\boldsymbol{y}$がランダム
    - スキップ接続あり: （途中の層の出力が最初ゼロだと）最初は$\boldsymbol{y}=\boldsymbol{x}$に
- ResNet（2015年）

![bg right:30% 90%](../advanced_vision/figs/skip.png)

