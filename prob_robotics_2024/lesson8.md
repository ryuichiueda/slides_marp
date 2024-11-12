---
marp: true
---

<!-- footer: 確率ロボティクス第8回 -->

# 確率ロボティクス第8回: パーティクルフィルタによる自己位置推定

千葉工業大学 上田 隆一

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>
<p style="font-size:50%">
図の一部は詳解確率ロボティクスから転載しています。
</p>

$$\newcommand{\V}[1]{\boldsymbol{#1}}$$
$$\newcommand{\jump}[1]{[\![#1]\!]}$$
$$\newcommand{\bigjump}[1]{\big[\!\!\big[#1\big]\!\!\big]}$$
$$\newcommand{\Bigjump}[1]{\bigg[\!\!\bigg[#1\bigg]\!\!\bigg]}$$

---

<!-- paginate: true -->

## 前回のおさらいと今回の内容

- ベイズフィルタ
    - 次の2つの式で構成
        - 移動時: $\hat{b}_t(\V{x}) =  \big\langle p(\V{x} | \V{x}', \V{u}_t) \big\rangle_{b_{t-1}(\V{x}')}$ 
        - 観測時: $b_t(\V{x}) = \eta p(\textbf{z}_t | \V{x}) \hat{b}_t(\V{x})$
    - <span style="color:red">問題: 式をどうやって実装する？</span>
- 今回: <span style="color:red">パーティクルフィルタ</span>というものを使いましょう
    - <span style="color:red">Monte Carlo localization（MCL）</span>[Fox 1999][Dellaert 1999]という方法

---

## パーティクルによる近似（詳解5.2節）

- 信念分布を<span style="color:red">パーティクル</span>（の集合）で表現
    - パーティクル: ロボットの分身
    - 分身をシミュレート$\Rightarrow$分身の分布が信念分布　
- 数式でのパーティクルの表現
    - <span style="color:red">$\V{x}_t^{(i)}$</span><span style="font-size:80%">$\quad(i=0,1,2,\dots,N-1)$</span>
        - 注意: あとから変えます
        - 分身なので姿勢を変数に持つ
        - $N$個ある　
- 右図の青の矢印
    - ロボットの初期姿勢に置いた<br />100個のパーティクル（まだ動かない）

![bg right:32% 100%](figs/particles.png)

---

## 移動後のパーティクルの姿勢更新（詳解5.3節）

- やること: ロボットの動きをシミュレートしてパーティクルを動かす
    - 実際のロボットの動きのばらつきを忠実に再現するのが理想的
        - パーティクルの分布が真の分布にしたがう
- ただし・・・
    - どんな誤差要因があるか、その量がどれだけかは特定が難しい
    - 次の日に変わるかもしれないし、1m先でも変わるかもしれない
- 環境が変わるとパラメータも変わるので、勘で設定してもよい
    - 最終的に推定できれば良いパラメータ
    - すこしばらつきを大きくとっておくとセンサで修正可能

---

## パーティクルの移動のための状態遷移モデルの例（詳解5.3.1節）

- 移動にともなう姿勢のばらつきをガウス分布で表現
    - 様々な誤差を考慮していると最終的にはガウス分布に（中心極限定理）　
    - （注意: パーティクルフィルタでは必ずしもガウス分布を使わなくてもよく、むしろセンシングでガウス分布を使いたくないから考えられている）
- ガウス分布を4つの標準偏差で表現
    - $\sigma_{\nu\nu}$: 直進1[m]で生じる道のりのばらつき
    - $\sigma_{\nu\omega}$: 回転1[rad]で生じる道のりのばらつき
    - $\sigma_{\omega\nu}$: 直進1[m]で生じるロボットの向きのばらつき
    - $\sigma_{\omega\omega}$: 回転1[rad]で生じるロボットの向きのばらつき　

<center>これらの値を実験で求めて（あるいは勘で設定して）パーティクルの挙動に反映</center>

---

## 位置や角度の雑音から速度、角速度の雑音への変換

- $\sigma_{\nu\nu}$のとき、$\nu$に乗せる雑音の量の決め方
    1. $\delta_{\nu\nu} \sim \mathcal{N}(0, \sigma_{\nu\nu}^2)$
        - $\delta_{\nu\nu}$: 1[m]あたりの誤差
    2.  $\delta_{\nu\nu}' = \delta_{\nu\nu}\sqrt{|\nu|/\Delta t}$
        - $\delta_{\nu\nu}'$: 速度に乗せる誤差
        - 分散（誤差の2乗）の大きさは移動距離に比例するので
$\delta_{\nu\nu}^2 : (\delta'_{\nu\nu}\Delta t)^2 = 1 : |\nu|\Delta t$
    3. $\sigma_{\nu\omega}, \sigma_{\omega\nu}, \sigma_{\omega\omega}$についても同様に
    4. <span style="font-size:80%">$\begin{pmatrix} \nu' \\ \omega' \end{pmatrix} = \begin{pmatrix} \nu \\ \omega \end{pmatrix} + \begin{pmatrix} \delta_{\nu\nu}\sqrt{|\nu|/\Delta t} + \delta_{\nu\omega}\sqrt{|\omega|/\Delta t} \\ \delta_{\omega\nu}\sqrt{|\nu|/\Delta t} + \delta_{\omega\omega}\sqrt{|\omega|/\Delta t} \end{pmatrix}$</span>
        - $(\nu \ \omega)^\top$: 制御指令
        - $(\nu' \ \omega')^\top$: 実際の速度

---

## 状態遷移モデルの実装（詳解5.3.2項）

- 前ページの式を実装して値を設定し、パーティクルを動かす
    - 右図: シミュレータのロボットの30[s]後の姿勢のばらつき
    - 下図: 右図のロボットに対するパラメータ設定の例
        - パラメータが小さすぎる/大きすぎる/ちょうど
- 値の設定方法は詳解確率ロボティクスの5.3.3項に
![bg right:22% 100%](figs/particles_vs_robots_robots.png)


<img width="33%" src="figs/mcl_motion_nocalib.gif" /><img width="33%" src="figs/mcl_motion_nocalib2.gif" /><img width="33%" src="figs/mcl_motion_update.gif" />


---

### パーティクルによる近似の数式上の解釈

- パーティクルの分布は信念分布の近似
- 次のような確率計算が可能
    - $P(\V{x}_t^* \in X ) = \int_{\V{x} \in X} \hat{b}_t(\V{x}) d\V{x} \approx \dfrac{1}{N} \sum_{i=0}^{N-1} \delta(\V{x}_t^{(i)} \in X)$
        - $X \subset \mathcal{X}$（状態空間$\mathcal{X}$の部分空間）
        - $\delta($事象$)$: 事象が正しければ1、違えば0を返す関数　
    - 式で書くとややこしいが、「ある領域$X$内にロボットの姿勢が含まれる確率は、その領域内にどれだけの割合のパーティクルが含まれるかで近似計算できる」ということ


---

### ベイズフィルタとの関係

- ベイズフィルタの移動時の式: $\hat{b}_t(\V{x}) =  \big\langle p(\V{x} | \V{x}', \V{u}_t) \big\rangle_{b_{t-1}(\V{x}')}$　
- パーティクルフィルタとベイズフィルタの対応
    - 移動前のパーティクル: $\V{x}^{(i)}_{t-1} \sim b_{t-1}$
    - 移動後のパーティクル: $\V{x}^{(i)}_t \sim p(\V{x} | \V{x}^{(i)}_{t-1}, \V{u}_t)$

<div style="color:red;text-align:center">期待値計算をサンプリングで実装</div>

---

## 観測後のセンサ値の反映（詳解5.4節）

- やること: センサ値の持つ情報をパーティクルの分布に反映する
    - ベイズの定理を利用

---

## 5.4.2 センサ値によるパーティクルの姿勢の評価

- センサ値$\V{z}_j$が得られたときに、ふたつのパーティクル$\V{x}^{(i)}, \V{x}^{(k)}$のどっちがどれだけ真値としてふさわしい？　
- 観測分布の値$p_j (\V{z}_j | \V{x})$の比で数値化可能
    - 例: $p_j (\V{z}_j | \V{x}^{(i)}) = 0.02, p_j (\V{z}_j | \V{x}^{(k)}) = 0.01$
    $\rightarrow \V{x}^{(i)}$の方が$\V{x}^{(k)}$より2倍<span style="color:red">尤もらしい</span>
    - $0.02$や$0.01$は確率ではないが確率的な比較は可能
    - 比: <span style="color:red">尤度比</span>、数値: <span style="color:red">尤度</span>　
- 観測モデル$p_j (\V{z}_j | \V{x})$は状態遷移モデルのときと同様、実験などで特定（後述）


---

### 尤度関数

- $p_j (\V{z}_j | \V{x})$について$\V{x}$を変数とみなす$\Longrightarrow$<span style="color:red">尤度関数</span>
    - $L_j(\V{x} | \V{z}_j ) = \eta p_j (\V{z}_j | \V{x})$
        - $\eta$は正ならなんでもよい（比でしか利用しないので）
        - 条件（パラメータ）と変数が入れ替わっただけで同じ式　
- ベイズの定理との関係
    - あえて尤度を使って考察したが、今の議論はベイズの定理でも説明可能
    - $b_t(\V{x}_t^{(i)}) = \hat{b}_t(\V{x}_t^{(i)} | \V{z}_{j,t}) = \eta p_j(\V{z}_{j,t} | \V{x}_t^{(i)}) \hat{b}_t(\V{x}_t^{(i)}) \\\\ = \eta L_j (\V{x}_t^{(i)} | \V{z}_{j,t} ) \hat{b}_t(\V{x}_t^{(i)})$



---

## パーティクルの重み（詳解5.4.3項）

- 尤度をどうパーティクルの分布に反映するか？
    - とりあえず<span style="color:red">重み</span>という変数を付加
- パーティクル（再定義）: $\xi_t^{(i)} = (\V{x}_t^{(i)}, w_t^{(i)})$
    - $\sum_{i=0}^{N-1} w^{(i)} = 1$　
- 次のように信念分布を近似
    - $P(\V{x}_t^* \in X ) = \int_{\V{x} \in X} b_t(\V{x}) d\V{x} \approx \sum_{i=0}^{N-1} w_t^{(i)} \delta(\V{x}_t^{(i)} \in X)$
        - $X$に真の姿勢が含まれる確率をパーティクルの重みの和で近似　
- 重みの計算
    - $w_t^{(i)} = L_j (\V{x}_t^{(i)} | \V{z}_{j,t} ) \hat{w}_t^{(i)}$（あとから正規化）

---

## 尤度関数の決定（紹介5.4.4項）

- 尤度関数（観測モデル）をどう決めるか
    - センサはブラックボックス
    - 状態遷移モデル同様、なにか雑音のモデルを作ってパラメータを調整
- 点ランドマークに対する尤度関数の設計の例
    - $L_j(\V{x} | \V{z}_j) = \mathcal{N}\left[ \V{z} = \V{z}_j | \V{h}_j(\V{x}), Q_j(\V{x}) \right]$
        - $Q_j(\V{x}) = \begin{pmatrix} [\ell_j(\V{x})\sigma_\ell]^2 & 0 \\ 0 & \sigma^2_\varphi \end{pmatrix}$
        - $\ell_j(\V{x})$: $\V{x}$とランドマーク$\text{m}_j$の距離
        - $\V{h}_j$: 観測関数　
    - 詳解確率ロボティクスでは$\sigma_\ell= 0.14$[m/m]、$\sigma_\varphi = 0.05$[rad]に

---

## 尤度関数の実装（詳解5.4.5）

- p.13の内容をそのままコードに
    - 下図: 重みを矢印の長さで表現したときの
    パーティクルの挙動
- 問題
    - 正規化していないので重みの和が無限大 or 0に
    - 正規化したとしても重みが一つのパーティクルに偏る

![bg right:30% 100%](./figs/mcl_sensor_update.gif)

---

## リサンプリング（詳解5.5節）

- 重みの偏りの解決
- やること
    - 重みの大きいパーティクルを複数に分割
    - 一方で、パーティクルの数を一定に保つ　
- 「リサンプリング」という方法で実装
    - サンプリング: アンケートなどをとるときに母集団から標本を選ぶこと
    - リサンプリング: サンプリングされた標本から、標本を使ってもう一度サンプリング
（ややこしいので具体例で説明）

---

## 単純なリサンプリングの実装（詳解5.5.1）

- 次のようなリサンプリングのアルゴリズムを考える
    1. パーティクルから一つパーティクルを選ぶ
        - 選ばれる確率 $\propto$重み
    2. 選んだパーティクルのコピーを作成
        - コピーの重みは$1/N$に
    3. 1, 2を$N$回反復。$N$個のコピーを新たなパーティクルの集合に

<center><img width="50%" src="./figs/resampling.jpg" /></center>

---

### リサンプリングの効果

- 重みの小さいパーティクル$\Longrightarrow$選ばれにくく消失
- 重みの大きいパーティクル$\Longrightarrow$何度も選ばれる
    - 重みは発散せずに抑えられる　
- 効果
    - 重みが偏らず推定が安定
    - 高確率の領域にパーティクルを集中
    - （低確率の部分は打ち切られる）

![bg right:30% 100%](./figs/mcl_simple_resampling.gif)

---

### 単純なリサンプリングの問題点

- コピーを作るときの計算量が$O(\log N)$
    - 全体で$O(N \log N)$
      $\Longrightarrow$ 2倍速い計算機を買ってきてもパーティクルの数を2倍にできない　
- パーティクルの選び方が偏る
    - 例: 重み$0.2$のパーティクル$5$個から$5$個選ぶ場合
$\Longrightarrow$それぞれが$1$個ずつきれいに選ばれる確率は低い

---

## 系統サンプリングによるリサンプリングの実装（詳解5.5.2項）

- 方法
    - パーティクルの重みを積み上げたリストを作成
    - リストの端から$1/N$ずつリストを進んでパーティクルを$N$個コピー
        - 最初の位置だけ$[0,1/N)$から乱数で選択
        - コピーの重みを$1/N$に変更
    - $N$個のコピーで元のパーティクルの集合を置き換え

<center><img width="70%" src="./figs/systematic_sampling.jpg" /></center>

---

### 系統サンプリングの効果

- 左: 単純なリサンプリング
    - 何も観測していないのにパーティクルが複数のクラスタに分離
        - 理由: 重みが全て同じでも選ばれないパーティクルが発生
- 右: 系統サンプリングによるリサンプリング
    - 全パーティクルの重みが同じなら全て選ばれる

<center><img width="30%" src="./figs/mcl_simple_resampling.gif" /><img width="30%" src="./figs/mcl_sys_resampling.gif" /></center>

---

## MCLの出力（詳解5.6節）

- パーティクルフィルタの出力はパーティクル
    - 推定姿勢ではない。分布を近似したもの
    - <span style="color:red">推定姿勢は絶対に一意に決まらない</span>
- 実際には・・・
    - 多くの行動決定ソフトは姿勢を求めるので推定姿勢を出力
        - ありえる出力値
            - 分布の平均値
            - 直近のセンサ値に対して最も重みが大きいパーティクルの姿勢

<center>本来は分布で行動を決めなければいけないことに注意（詳解12章）</center>

---

## 5.7 まとめ

- ベイズフィルタを導出　
- MCLというアルゴリズムでベイズフィルタを実装
    - サンプリングに関するアルゴリズムを駆使　
- 「正しい状態遷移モデル、観測モデル」に対する考察
    - 動かしたい環境でロボットが動くモデルが良いモデル
    - 実験室でチューニングの果てに得た精度には意義があまりないので論文を読むときに注意
