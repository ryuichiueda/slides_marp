---
marp: true
---

<!-- footer: 確率ロボティクス第11回 -->

# 確率ロボティクス第11回:<br />マルコフ決定過程と動的計画法

千葉工業大学 上田 隆一

<p style="font-size:50%">
図の一部は詳解確率ロボティクスから転載しています．
</p>

$$\newcommand{\V}[1]{\boldsymbol{#1}}$$
$$\newcommand{\jump}[1]{[\![#1]\!]}$$
$$\newcommand{\bigjump}[1]{\big[\!\!\big[#1\big]\!\!\big]}$$
$$\newcommand{\Bigjump}[1]{\bigg[\!\!\bigg[#1\bigg]\!\!\bigg]}$$

---

<!-- paginate: true -->

### ロボットの行動決定

- 移動ロボットの場合，経路計画問題として扱われることが多い
    - ある地点からある地点までの移動を最短経路で<br />　
- もっと知的にしたい
    - 例
        - 危険のある近道と危険でない回り道を柔軟に選択
        - 目的地に行くことを諦める

<center>
<span style="color:red">マルコフ決定過程</span>と<span style="color:red">動的計画法</span>の枠組みで考える
</center>

---

## マルコフ決定過程（詳解10.1節）

- やること
    - ロボットが行動決定するという現象や問題を定式化


---

## 状態遷移と観測（詳解10.1.1項）

- ロボットの行動
    - 状態遷移モデル: $\V{x}_t \sim p(\V{x} | \V{x}_{t-1}, a_t)\quad (t=1,2,\dots,T)$
        - $T$: タスクが終わる時間（不定）
        - $\V{x}_T$: 終端状態
        - $a_t \in \mathcal{A} = \\{a_0, a_1, \dots, a_{M-1}\\}$: 行動
            - これまでの制御指令$\V{u}$のようにベクトルでもよいし，「走る」，「投げる」などの複合的な動作でもよい。なんなら「食う」，「寝る」，「遊ぶ」などでもよい
            - 添字が時刻だったり行動の種類のIDだったりするので注意　
- ロボットの観測
    - 常に真の状態$\V{x}_t^*$は既知とする
    - 未知の場合については詳解12章で扱われている


---

### マルコフ性の仮定

- 状態遷移が遷移前の状態よりも前の状態に左右されない場合を考える
    - $\V{x}_t \sim p(\V{x} | \V{x}_{t-1}, a_t)$の形を見るとそうなっている
    - $\V{x}_{t-2}$以前の状態は何の影響も与えない　
- そうでない場合はどうする？
    - マルコフ性を満たすように状態の定義をしなおす
    - 例: $\V{x}_{t-2}$まで散々動いてモータが熱々のロボットと$\V{x}_{t-1}$から
    スタートするロボットでは動きが違う
    $\Longrightarrow$モータの温度を$\V{x}$の変数として扱う

---

## 評価関数（詳解10.1.2項）

- ロボットの行動を評価する
    - 自己位置推定やSLAMの性能は（ロボットに人格があれば）自律ロボットにとっては手段でしかない。うまく行動できるかどうかが重要。　
- 評価関数: $J(\boldsymbol{x}_{0:T}, a_{1:T}) \in \mathbb{R}$
    - やったこと（$a_{1:T}$），起こったこと（$\boldsymbol{x}_{0:T}$）で評価
    -  評価は時間，消費エネルギー，危険性など多岐にわたるはずであるが，うまく式を作ってスカラ1個で評価することとする
        -  行動はひとつしか選べないのでこれで十分

---

## 報酬と終端状態の価値（詳解10.1.3項）

- 評価関数$J(\boldsymbol{x}_{0:T}, a_{1:T})$を次の形式で考える
    - $J(\boldsymbol{x}_{0:T}, a_{1:T}) = \sum_{t=1}^T r(\boldsymbol{x}_{t-1}, a_t, \boldsymbol{x}_t) + V_\text{f}(\boldsymbol{x}_T)$
        - $r(\boldsymbol{x}_{t-1}, a_t, \boldsymbol{x}_t) \in \mathbb{R}$: 状態遷移ごとに与える評価を決める関数
            - 報酬モデルと呼ぶ
            - 値を<span style="color:red">報酬</span>と呼ぶ
            - $t=0$から$t=T$までの状態遷移，行動履歴，
            報酬をまとめて<span style="color:red">エピソード</span>と呼ぶ
        - $V_\text{f}(\boldsymbol{x}_T)$: <span style="color:red">終端状態</span>の評価　
- 終端状態
    - 良くも悪くもタスクが終わった状態
    - $V_\text{f}(\boldsymbol{x}_T)$でどのような終わりが良いのか点数をつけておく

---

## 方策と状態価値関数（詳解10.1.4項）

- 同じ初期状態$\V{x}_0$からタスクを行うと，$J(\V{x}_{0:T}, a_{1:T})$の値は毎回変化
    - 状態遷移が確率的なので　
- 行動ルールがあったときにどうやって評価する？
    - 行動ルールのことを$\Pi$と表記して<span style="color:red">方策</span>と呼びましょう
        - 方策の例: ロボットを動かすための自作のプログラム
    - 良い方策: $J$の期待値が高い　
- $\V{x}_0$から$\Pi$でロボットを動かしたときの$J$の期待値を<span style="color:red">価値</span>$V^\Pi(\V{x}_0)$と表記
    - 価値の性質を調べてみましょう


---

### 価値の性質

- $V^\Pi(\V{x}_0) = \left\langle \sum_{t=1}^T r(\V{x}_{t-1}, a_t, \V{x}_t) + V(\V{x}_T) \right\rangle_{p(\V{x}_{1:T}, a_{1:T}|\V{x}_0, \Pi)}$
    - $T$は可変だが，固定として扱える
        - 早くタスクが完了したら，終端状態で何もしない状態遷移（報酬ゼロ）を繰り返して評価を先延ばしにすればよい
        - この先延ばしで$T=0$（初期状態=終端状態の場合）でも上式が成立
    - 終端状態の評価は価値の定義に含まれる　
- $\V{x}_0$は必ずしも初期状態である必要がない
    - マルコフ性の前提から，$\V{x}_{-1}$以前のことは$V^\Pi(\V{x}_0)$に無関係
    - 方策でも$\V{x}_{-1}$以前を考慮する意味はない
    - タスクのどの時点の状態でも価値$V^\Pi(\V{x})$が考えられる　
- <span style="color:red">関数$V^\Pi: \mathcal{X} \to \mathbb{R}$の存在$\Longrightarrow$状態価値関数</span>


---

### 逐次式による価値の表現

- 価値の式を逐次式にしてみましょう
    - <span style="font-size:80%">$V^\Pi(\V{x}_0) = \left\langle r(\V{x}_0, a_1, \V{x}_1) + \sum_{t=2}^T r(\V{x}_{t-1}, a_t, \V{x}_t) + V(\V{x}_T)  \right\rangle_{p(\V{x}_{1:T}, a_{1:T} |\V{x}_0, \Pi)}$
$= \Big\langle r(\V{x}_0, a_1, \V{x}_1) \Big\rangle_{p(\V{x}_{1:T}, a_{1:T} |\V{x}_0, \Pi)} + \left\langle \sum_{t=2}^T r(\V{x}_{t-1}, a_t, \V{x}_t) + V(\V{x}_T)  \right\rangle_{p(\V{x}_{1:T}, a_{1:T} |\V{x}_0, \Pi)}$
$= \Big\langle r(\V{x}_0, a_1, \V{x}_1) \Big\rangle_{p(\V{x}_1 , a_1 | \V{x}_0, \Pi )} + \left\langle \sum_{t=2}^T r(\V{x}_{t-1}, a_t, \V{x}_t) + V(\V{x}_T)  \right\rangle_{p(\V{x}_{2:T}, a_{2:T} |\V{x}_1, a_1, \V{x}_0, \Pi)p(\V{x}_1, a_1 | \V{x}_0, \Pi)}$
（↑第一項: 余計な変数の消去. 第二項: 乗法定理）
$= \Big\langle r(\V{x}_0, a_1, \V{x}_1) \Big\rangle_{p(\V{x}_1 , a_1 | \V{x}_0, \Pi )} + \left\langle \sum_{t=2}^T r(\V{x}_{t-1}, a_t, \V{x}_t) + V(\V{x}_T)  \right\rangle_{p(\V{x}_{2:T}, a_{2:T} |\V{x}_1, \Pi)p(\V{x}_1, a_1 | \V{x}_0, \Pi)}$
（↑第二項: マルコフ性から$\V{x}_1$が分かれば条件$\V{x}_0,a_1$は不要）</span>

次ページに続く

---

### 逐次式による価値の表現（続き）

- 逐次式になる
    - <span style="font-size:80%">$=\Big\langle r(\V{x}_0, a_1, \V{x}_1) \Big\rangle_{p(\V{x}_1, a_1 | \V{x}_0, \Pi )} + \left\langle \left\langle \sum_{t=2}^T r(\V{x}_{t-1}, a_t, \V{x}_t) + V(\V{x}_T)  \right\rangle_{p(\V{x}_{2:T}, a_{2:T}|\V{x}_1, \Pi)} \right\rangle_{p(\V{x}_1, a_1 | \V{x}_0, \Pi)}$
$= \Big\langle r(\V{x}_0, a_1, \V{x}_1) \Big\rangle_{p(\V{x}_1, a_1 | \V{x}_0, \Pi )} + \left\langle V^\Pi(\V{x}_1) \right\rangle_{p(\V{x}_1, a_1 | \V{x}_0, \Pi)}$
 （↑第二項: $\V{x}_1$は$\V{x}_0$と同様, 初期状態である必要がない）
$=\Big\langle r(\V{x}_0, a_1, \V{x}_1) + V^\Pi(\V{x}_1) \Big\rangle_{p(\V{x}_1, a_1 | \V{x}_0, \Pi )}$
$= \Big\langle r(\V{x}_0, a_1, \V{x}_1) + V^\Pi(\V{x}_1) \Big\rangle_{p(\V{x}_1 | \V{x}_0, a_1, \Pi )P(a_1 | \V{x}_0, \Pi)}$
$= \Big\langle r(\V{x}_0, a_1, \V{x}_1) + V^\Pi(\V{x}_1) \Big\rangle_{p(\V{x}_1 | \V{x}_0, a_1 )P(a_1 | \V{x}_0, \Pi)}$</span>
- $\V{x}_0$が初期状態である必要はないので時刻を取り払う
    - $V^\Pi(\V{x}) = \left\langle r(\V{x}, a, \V{x}') + V^\Pi(\V{x}') \right\rangle_{p(\V{x}' | \V{x}, a )P(a | \V{x}, \Pi)}$
        - 価値は，報酬と遷移後の価値の期待値の和と釣り合う

---

### 決定論的方策

- $V^\Pi(\V{x}) = \left\langle r(\V{x}, a, \V{x}') + V^\Pi(\V{x}') \right\rangle_{p(\V{x}' | \V{x}, a )P(a | \V{x}, \Pi)}$
    - $a$は，そのときの状態$\V{x}$と方策$\Pi$から確率的に決まるという式になっているが，ロボットが自分で選択可能
    - $r(\V{x}, a, \V{x}'), V^\Pi(\V{x}'), p(\V{x}' | \V{x}, a )$の値が分かればベストな行動$a^*$が決まる
        - $\Pi$から方策を改善できる
        - 全状態で$\V{x}$に対して$a^*$を決定していくと$\Pi$より性能がよくなる
<span style="color:red">$\Longrightarrow$確率的な方策があると，それより性能がよい決定論的な方策が存在</span>　
- 方策を実装するときはこの形式で十分
    - $\Pi: \mathcal{X} \to \mathcal{A}$（<span style="color:red">決定論的方策</span>）
- $\Pi$が決定論的方策の場合の価値の逐次式
    - $V^\Pi(\V{x}) = \left\langle r(\V{x}, a, \V{x}') + V^\Pi(\V{x}') \right\rangle_{p(\V{x}' | \V{x}, a )} \qquad (a =\Pi(\V{x}))$

---

## マルコフ決定過程のまとめ（詳解10.1.5項）

- 系
    - 時間: $t = 0,1,2,\dots,T$（$T$は不定でよい）
    - 状態と行動: $\V{x} \in \mathcal{X}$, $a \in \mathcal{A}$
        - 一部の状態が終端状態: $\V{x} \in \mathcal{X}_\text{f} \subset \mathcal{X}$
    - 状態遷移モデル: $p(\V{x}' | \V{x}, a) \ge 0$
- 評価
    - 報酬モデル: $r(\V{x}, a, \V{x}') \in \mathbb{R}$
    - 終端状態の価値: $V_\text{f}(\V{x}) \in \mathbb{R} \quad (\V{x} \in \mathcal{X}_\text{f})$
    - 評価: $J(\V{x}_{0:T}, a_{1:T}) = \sum_{t=1}^T r(\V{x}_{t-1}, a_t, \V{x}_t) + V_\text{f}(\V{x}_T)$
- 解く問題
    - なるべく良い方策$\Pi: \mathcal{X} \to \mathcal{A}$を求めたい
        - 求めた価値の逐次式が解決に重要な役割

---

## 経路計画問題（詳解10.2節）

- 次のような問題を考えます
    - ロボットが最短時間でゴールに行く
    - 水たまりに入りたくない
    - とれる行動: 前進，右回転，左回転の3種類

![bg right:40% 100%](./figs/puddle_world4.gif)

---

## 報酬の設定（詳解10.2.1項）

- 「ゴールまで早く到達でき，かつ水たまりを避ける」移動を高く評価
    - $r(\V{x}, a, \V{x}') = -\Delta t - cw(\V{x}')\Delta t$
        - $\Delta t$: 1ステップの時間
        - $w(\V{x}')$: 遷移後の状態$\V{x}'$での水深
        - $c$: どれだけ水がいやなのかを表す係数　
- シミュレータでの実装
    - 水たまり: 時間の10倍の罰
        - ふたつ重なった部分: 20倍

![bg right:40% 100%](./figs/puddle_world4.gif)

---

## エピソードの評価（詳解10.2.2項）

- 単純に各ステップの$r$を積算して，$J$とする
    - ゴールした状態の価値を$0$に
    - $J$: かかった時間と水たまりのペナルティーの和　
- $r$は負なので$J$は$0$に近いほど良い

---

## 方策の評価（詳解10.3節）

- 価値が確定している終端状態からさかのぼっていくと$V^\Pi(\V{x})$の値が計算できる
    - 使う式: $V^\Pi(\V{x}) = \left\langle r(\V{x}, a, \V{x}') + V^\Pi(\V{x}') \right\rangle_{p(\V{x}' | \V{x}, a )}$
    - ただし$V^\Pi(\V{x})$はそのままでは計算不可能
        - $\V{x}$が無限にあるので
    - 詳解確率ロボティクスでは$\mathcal{X}$を格子状に区切って離散化して計算（次ページ）　
- 例題
    - スライド15ページにある，水たまりを無視して一直線にゴールに向かう方策（puddle ignore policyと呼びましょう）を評価

---

## 状態空間の離散化（詳解10.3.1項）

- $XY\theta$空間を図のように離散化
    - 各区画を$s_{(i_x,i_y,i_\theta)}$と番号づけ
        - $i_x,i_y,i_\theta$: 各軸の区画つけた$0,1,2,\dots$という番号
        - 実装での区間の幅: $X,Y$軸が200[mm]，$\theta$軸が10[deg]
- $s_{(i_x,i_y,i_\theta)}$: <span style="color:red">離散状態</span>

![bg right:40% 100%](./figs/10.4.jpg)

---

### 価値関数の初期化

- 終端状態の価値を0，それ以外を大きな負の値にしておく
- 図: $i_\theta$を固定したときの$XY$平面での価値関数
    - 白いところがゴール

![bg right:40% 100%](./figs/init_policy_evaluation.png)

---

## 離散状態間の状態遷移と状態遷移に対する報酬（詳解10.3.1項）

- 数式を$\V{x}$から$s$に離散化
    - 価値関数の式: $V^\Pi(s) = \big\langle R(s, a, s') + V^\Pi(s') \big\rangle_{ P(s' | s, a) }$
    $\qquad\qquad\qquad\qquad\ = \sum_{s'\in \mathcal{S}} P(s' | s, a) \left[ R(s, a, s') + V^\Pi(s') \right]$
        - $P(s' | s, a)$: 離散化した状態遷移関数（あとで計算）
        - $R(s,a,s')$: 離散化した報酬（これもあとで計算）　
    - 終端状態: 中に含まれるすべての$\V{x}$が終端状態のものを選ぶ　

---

### 方策の離散化

- 各離散状態の中心座標でのpuddle ignore policyの行動を，その離散状態の行動に
- 方策の形式: $\Pi: \mathcal{S} \to \mathcal{A}$

![bg right:40% 100%](./figs/init_policy.png)


---

### $P(s' | s, a)$の計算

- ある$i_\theta$に対して，下図のようにモンテカルロ法で求める
    - $i_x, i_y$については相対値でよい

<img width="100%" src="./figs/10.5.jpg" />

---

### $R(s, a, s')$の計算

- 元の式: $r(\V{x}, a, \V{x}') = -\Delta t - cw(\V{x}')\Delta t$
- $R(s, a, s')$: 状態$s'$での水の深さの平均値で$w(\V{x}')$を代用して計算

<img width="50%" src="./figs/depth.png" />

---

## 方策評価の実装（詳解10.3.3項）

- ある方策$\Pi$に対して終端状態以外で次の手続きをひたすら繰り返す
    - $V^\Pi(s) \longleftarrow \sum_{s'\in \mathcal{S}} P(s' | s, a) \left[ R(s, a, s') + V^\Pi(s') \right]$
    - すべての離散状態で一通り計算することをスイープと呼ぶ
- 下図: puddle ignore policyに対する計算

<img src="./figs/10.6.jpg" />

---

## 計算終了の判定（詳解10.3.4項）

- 次の手続きで計算を止める
    - $V^\Pi(s)$の変化量を記録
    - 全離散状態での変化量の最大値が閾値を下回ったら停止
- 右図: 閾値$0.01$sで止めて得られた$V^\Pi$
    - （参考: 92スイープで停止）

![bg right:40% 100%](./figs/policy_evaluation_end_sweeps.png)

---

## 価値反復（詳解10.4節）

- これまでやってきたこと
    - 水たまりに突っ込んでいく方策の状態価値関数を求めた　
- 方策はもっとよくできる
    - 方策を局所的に変えると状態価値関数の値を改善可能

---

### 方策改善

- <span style="color:red">行動価値関数</span>: 状態だけでなく行動も変数にした価値関数
    - $Q^\Pi(s, a)  = \Big\langle R(s, a, s') + V^\Pi(s') \Big\rangle_{ P(s' | s, a) }$
    $\qquad\qquad\ = \sum_{s'} P(s' | s, a) \left[ R(s, a, s') + V^\Pi(s') \right]$　
- 行動価値関数を利用した方策の改善
    - $\Pi(s) \longleftarrow \text{argmax}_{a \in \mathcal{A}} Q^\Pi(s, a)$
    - 価値の計算（方策評価）と，この計算（方策改善）を繰り返すと方策がよくなっていきそうだ

これを突き詰めると次ページのアルゴリズムに

---

### 価値反復

- 次のようなアルゴリズムを考える
    1. 全状態について適当に状態価値関数$V$を初期化
        - ただし終端状態の価値だけは決まった値に
    2. 各状態において, 全行動$a \in \mathcal{A}$の行動価値関数を求め, 最大の値を$V(s)$に代入
        - $V(s) \longleftarrow \max_{a \in \mathcal{A}} Q(s, a)$
    3. 2を何スイープも実行
    4. 収束後，各状態で行動価値関数を最大にする行動を記録
        - $\Pi^*(s) = \text{argmax}_{a \in \mathcal{A}} \sum_{s'} P(s' | s, a) \left[ R(s, a, s') + V^*(s') \right]$
            - $V^*$: 収束した状態価値関数（<span style="color:red">最適状態価値関数</span>）
            - $\Pi^*$: <span style="color:red">最適方策</span>

---

### 価値反復の実行

- 状態価値関数
<img width="70%" src="./figs/10.7.jpg" />
- 方策
<img width="70%" src="./figs/10.8.jpg" />

---

### 最適方策を用いた行動決定

- $\Pi^*$: どの状態に対しても最適な行動が記録されている
    - ロボットは$\Pi^*$を使って反射的に行動を選ぶと最適な経路でゴールに行ける

<img width="40%" src="./figs/optimal_policy.gif" /> 

---

## ベルマン方程式と最適制御（詳解10.5節）

- やること
    - いままでのことを数式を眺めながらおさらい

---

## 有限マルコフ決定過程（詳解10.5.1項）

- 離散状態でのマルコフ決定過程: <span style="color:red">有限マルコフ決定過程（finite MDP）</span>
- 系
    - 時間: $t = 0,1,2,\dots,T$（$T$は不定でよい）
    - 状態と行動: $s \in \mathcal{S}$，$a \in \mathcal{A}$
        - 一部の状態が終端状態: $s \in \mathcal{S}_\text{f} \subset \mathcal{S}$
    - 状態遷移モデル: $P(s' | s, a) \ge 0$
- 評価
    - 報酬モデル: $R(s, a, s') \in \mathbb{R}$
    - 終端状態の価値: $V_\text{f}(s) \in \mathbb{R} \quad (s \in \mathcal{X}_\text{f})$
    - 評価: $J(s_{0:T}, a_{1:T}) = \sum_{t=1}^T R(s_{t-1}, a_t, s_t) + V_\text{f}(s_T)$
- 最適方策$\Pi^*: \mathcal{S} \to \mathcal{A}$を求める
    - （計算量の話を抜きにすると）価値反復で求まる

---

## 有限マルコフ決定過程におけるベルマン方程式（詳解10.5.2項）

- 最適状態価値関数の性質
    - $V^*(s) = \max_{a \in \mathcal{A}} \sum_{s'} P(s' | s, a) \left[ R(s, a, s') + V^*(s') \right]$
        - 価値反復でもう価値が更新できない状態
        - <span style="color:red">ベルマン（最適）方程式</span>と呼ばれる　
- 最適方策
    - $\Pi^*(s) = \text{argmax}_{a \in \mathcal{A}} \sum_{s'} P(s' | s, a) \left[ R(s, a, s') + V^*(s') \right]$
    - そのときの状態だけで最適な行動が決まる
        - その前の状態がなんであろうと関係ないので，終端状態に近いところから部分問題を解いていくと$J$の期待値に対して最適な方策が得られる
        （<span style="color:red">最適性の原理</span>）

---

## 連続系でのベルマン方程式と最適制御（詳解10.5.3項）

- もう一度連続的な状態空間の話に戻る
    - ベルマン方程式: 
        - $V^*(\V{x}) = \int_{\mathcal{X}} p(\V{x}' | \V{x}, a) \left\{ r(\V{x}, a, \V{x}') +  V^*(\V{x}') \right\} d\V{x}'$
    - さらに$a$を$\V{u}$に戻し，時間を連続に
        - 上の式は<span style="color:red">ハミルトン-ヤコビ-ベルマン方程式</span>と呼ばれる，制御問題を扱うための統一的な式になる
            - ほとんどの制御の問題はHJB方程式を具体化したもので，ほとんどの制御の手法はHJB方程式を近似的に解くためのもの

<center>ロボットや人間の行動決定の問題と制御には本質的な違いはない</center>

---

## まとめ

- 今回やったこと
   - （有限）マルコフ決定過程の定式化
   - その具体例としてのロボットが水たまりを避けてゴールに向かう問題を定義し，価値反復で最適方策を計算
   - 最適性の原理やベルマン方程式について確認　
- 補足
   - 価値反復は速い/遅い
       - 状態空間全域で最適方策を得ようとすればこれ以上速いアルゴリズムはおそらくないので速い
       - 価値反復は簡単にいくらでも並列化できるので速い
       - 状態空間の次元が増えると離散状態が指数乗的に増えるので遅い（<span style="color:red">次元の呪い</span>）
   - 最適状態価値関数，最適方策を求めない手法は近似
       - 最悪，ロボットが無限ループに陥る

