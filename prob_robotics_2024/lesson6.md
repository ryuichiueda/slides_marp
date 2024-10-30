---
marp: true
---

<!-- footer: 確率ロボティクス第6回 -->

# 確率ロボティクス第6回: 不確かさのモデル化

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

## 練習問題

- [ガウス分布に従う2変数の和の分布](https://b.ueda.tech/?page=robot_and_stats_questions#ガウス分布に従う2変数の和の分布)

---

## 今回やること（詳解4.1節）

- 状態方程式・観測方程式を実世界に近づける
    - 状態方程式: $\boldsymbol{x}_t = \boldsymbol{f}(\boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$
    - 観測方程式: $\boldsymbol{z}_j = \boldsymbol{h}_j (\boldsymbol{x})$（$j$: ランドマークのID）
- トラブルのない世界$=$未来が予測可能な世界
    - 確率ロボティクスは必要ない
    - そんな世界はない

<center>雑音や外乱を加えて未来を不確かにしましょう</center>

---

## ロボットの移動に関する不確かさの要因（詳解4.2節）


- とにかく様々なことが起こる
    - 小石への片輪の乗り上げ、走り出し、停止時の揺れ、縁石への乗り上げ、走行環境の傾斜、左右の車輪が同じように回らない、穴に車輪が嵌る、人が移動する、・・・

<center>
<iframe width="560" height="315" src="https://www.youtube.com/embed/Oz2wIDD02LY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

シミュレータへ実装しているときりがない
</center>

---

### 雑音や誤差の分類

- アクシデントは次の3軸（詳解よりひとつ増やしました）で分類可能
    - どれだけ継続期間があるか
        - <span style="color:red">短いと雑音、長いとバイアスの性質を帯びる</span>
            - 例: 小石に車輪が乗り上げた（一瞬）$\leftrightarrow$縁石に乗り上げた（数秒）$\leftrightarrow$右車輪の空気が少ない（ずっと継続）
    - どれだけ$\boldsymbol{x}$がずれるか
        - ずれが大きいと厄介
            - 例: 小石に車輪が乗り上げた（小）$\leftrightarrow$人がロボットを移動（大）　
    - どれだけよく起こるか
        - 例: 小石に車輪が乗り上げた（高）$\leftrightarrow$人がロボットを移動（低）　
            - <span style="color:red">頻度が低いほどよいが、低いと考慮するかどうか悩むケースも多い</span>

---

## 移動ロボットの研究でよく想定される雑音、誤差（移動編）

|雑音・誤差|説明|性質|
|:--------------|:-----------------------|:--------------------|
|動きの雑音|突発的にロボットの向きを少し変化|短時間、誤差小、高頻度|
|動きのバイアス|制御指令値と実際の出力値を常に一定量ずらす|長時間、誤差小|
|スタック|ロボットを同じ姿勢に抑留|長時間、誤差大、低頻度|
|誘拐|ロボットを別の場所に突然ワープ|短時間、誤差大、低頻度|

一つずつ見ていきましょう


---

## 移動に対して発生する雑音のモデルの一例（詳解4.2.1）

- 次のようなモデルを考える
    - 環境にランダムに何か（小石としましょう）が落ちている
    - ロボットがそれを踏むと向き$\theta$が少しずれる　
- 詳解確率ロボティクスでのシミュレータへの実装方法（1, 2の繰り返し）
    1. ロボットが小石を踏んだら、次に踏むまでの道のりを計算
    1. 計算した道のりに達したら$\theta$をずらして再度道のりを計算
        - これはガウス分布で


「次に踏むまでの道のり」: どんな計算をすればよいか？


---

### 指数分布の利用

- 指数分布って何？
    - ランダムなイベントが次に起こるまでの時間などがしたがう分布
       - 例: 「ある川の堤防が10年以内に決壊する確率」など
- 指数分布の式: $p(x | \lambda ) = \lambda e^{-\lambda x} \quad (x \ge 0)$
    - $x$: イベントが起こるまでの時間
    - $\lambda$: 一定時間に起こるイベントの数の期待値
        - $1/\lambda$: イベントが一定時間に起こる数の期待値

<center>一定区間内の石の数を石をふまない距離に変換できる</center>

---

### 指数分布の確率密度関数

- 下図のような確率密度関数（左: $\lambda = 1$、右: $\lambda = 2$）
    - 右のほうが小石が多いので踏むまでの時間は短くなる

<center>
<img width="35%" src="./figs/expon_lambda1.png" /><img width="35%" src="./figs/expon_lambda2.png" />
</center>

- 累積分布を書いてみましょう


---

### 雑音のシミュレーションの例

- 道のりの計算: $x \sim p(x | \lambda ) = \lambda e^{-\lambda x}$
    - $\lambda = 5$（200[mm]に1回小石を踏む）
- $\theta$への雑音混入: $\theta \sim \mathcal{N}(\theta | \theta_\text{before}, \sigma_\theta)$
    - $\theta_\text{before}$: 小石を踏む前のロボットの向き
    - $\sigma_\theta = \pi/60$<br />（小石を踏むと標準偏差3[deg]で$\theta$がずれる）

![bg right:30% 110%](./figs/motion_noise.gif)

---

## 移動速度に混入するバイアスのモデルの例（詳解4.2.2）

- 次の二つの値を違うものとして扱う
    - モータへの制御指令値: $\boldsymbol{u}_t = (\nu_t \ \omega_t)^\top$
    - 実際のロボットの速度: $\boldsymbol{u}_t^* = (\nu_t^* \  \omega_t^*)^\top$　
        - ここで$(\nu_t^* \  \omega_t^*)^\top = (\delta_\nu \nu_t \ \delta_\omega\omega_t)^\top$
        - $\delta_\nu, \delta_\omega$はシミュレーションの開始時に決めて、以後一定
	      $\rightarrow$<span style="color:red">系統誤差</span>となる
- 実際の例

<iframe width="180" height="315" src="https://www.youtube.com/embed/wNm9dhWBqZM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

---

### バイアスのシミュレーションの例

- シミュレータでの$\delta_\nu, \delta_\omega$の決め方
    - いずれも平均値$0$、標準偏差$0.1$のガウス分布からドロー
    - 右図: 灰色がバイアスなし、赤があり　
- バイアスの存在
    - 推定に悪影響
        - 多くアルゴリズムは無視
        - 対策が難しい
    - キャリブレーションで小さくすることは可能
    - 根絶は無理

![bg right:33% 100%](./figs/motion_bias.gif)

---

## スタックのモデル（詳解4.2.3）

- スタック: ロボットが何かに引っかかり動けなくなる現象　
- モデルの例（小石のときと同じ）
    - 次にスタックするまでの時間を指数分布からドロー
    - スタックしたら抜け出すまでの時間を指数分布からドロー

---

### スタックのシミュレーション

- パラメータ
    - スタックまでの時間の期待値: 60[s]
    - 抜け出す時間の期待値: 60[s]　
- 図 
    - 赤: スタックのないロボット
    - 青: スタックするロボット（100台）　

![bg right:40% 100%](./figs/jamming.gif)

「誤差」と呼ぶには大きすぎる誤差が発生

---

## 4.2.4 誘拐のモデル

- 誘拐
    - 動いているロボットが人に強制移動させられる
    - <span style="color:red">誘拐ロボット問題（kidnapped robot problem）</span>からの用語　
- 実装方法
    - 誘拐のタイミング: 指数分布を利用
    - 誘拐後のロボットの姿勢$\boldsymbol{x}$: <span style="color:red">一様分布</span>を利用　
- 一様分布
    - $\mathcal{U}(\boldsymbol{x} | X) = \begin{cases} \eta^{-1} & (\boldsymbol{x} \in X)  \\ 0 & (\boldsymbol{x} \not\in X) \end{cases}$
        - $\eta = \int_{X} 1 d\boldsymbol{x}'$（面積や体積）
        - $X$: ロボットの姿勢$\boldsymbol{x}$が存在する範囲（そして$X$内のどこか情報がない）

---

### 誘拐のシミュレーションの例

- パラメータ
    - 誘拐が起こるまでの時間の期待値: 5[s]
    - 誘拐先の姿勢: $-5<x<5$[m], $-5<y<5$[m], $-\pi<\theta<\pi$

![bg right:35% 100%](./figs/kidnap.gif)

過去の情報を使う自己位置推定には致命的

---

## 状態方程式と確率的な状態遷移モデル（詳解4.2.5）

- 状態方程式の従来の形式（雑音つき）
    - $\boldsymbol{x}_t = \boldsymbol{f}(\boldsymbol{x}_{t-1}, \boldsymbol{u}_t) + \boldsymbol{\varepsilon}_t$
        - <span style="color:red">「本来あるべき状態遷移があって、それに雑音$\boldsymbol{\varepsilon}_t$が加わる」</span>という表現
    - 問題
        - 表記上、各時刻で$\boldsymbol{x}_t$が決まってしまうように見える$\rightarrow$不確かさの表現に限界
        - 「$\boldsymbol{\varepsilon}_t$」のイメージよりも大きい雑音が表現しずらい

<br />
<center>もっと一般化した表現が必要</center>

---

### 確率的な表現の導入


- 状態遷移関数$\boldsymbol{f}$に雑音をつけたものを次の確率密度関数で置き換え
    - $p(\boldsymbol{x}|\boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$
        - <span style="color:red">状態遷移分布</span>と呼びましょう
        （詳解確率ロボティクスでは「状態遷移モデル」と言っていますが）
- 状態方程式に相当する式
    - $\boldsymbol{x}_t \sim p(\boldsymbol{x}|\boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$
        - <span style="color:red">状態遷移モデル</span>と呼びましょう

---

### 状態方程式と状態遷移モデル

- 同じことを表現しているが、場合に応じて使い分け
        - 加法定理、乗法定理など確率の演算は状態遷移モデルで 
        - 変数レベルの計算や実装などは状態方程式で

<img width="100%" src="./figs/fig4.2.jpg" />

---

## 観測に関する不確かさの要因（詳解4.3節）

- 移動と同じくセンシングでも様々なことが起こる
    - 詳解2章参照（センサの問題、外的要因）　
- センサ処理で実用上求められること
    - 偶然誤差、系統誤差、過失誤差をバランスよく考慮
        - ロボットでの過失誤差: 観測対象の取り違えなどで発生

---

### 移動ロボットの研究でよく想定される雑音、誤差（センシング編）

太字、赤字の用語については次ページで解説

|雑音・誤差|説明|性質|
|:--------------|:-----------------------|:--------------------|
|計測値のばらつき|値が**独立同分布**でばらつく（たいていガウス分布）|偶然誤差|
|計測値のズレ|平均値が少しずれている|系統誤差|
|ファントム|見えないはずのランドマークを観測する|過失誤差（<span style="color:red">偽陽性</span>） |
|見落とし|見えるはずのランドマークを見落とす|過失誤差（<span style="color:red">偽陰性</span>） |
|オクルージョン|ランドマークの一部が障害物等に隠れてセンサ値に異常|系統誤差（一瞬なら偶然誤差）|

---

### 独立同分布

- データ$x_1, x_2, x_3, \dots$が互いに同じ分布から発生しており、かつデータが互いが独立していること
    - 「互いに独立していない」の例: $x_1$が大きい値だと$x_2$の値も大きい、など
        - <span style="color:red">ロボットに関しては成立しないことが多い</span>けど、研究として扱われないなら仮定として与えられることが多い
- そういう名前の分布があるわけじゃありません（形容詞のように使います）
- $x_1, x_2, \dots \overset{\text{i.i.d.}}{\sim} p$などと表記
    - i.i.d.: **i**ndependent and **i**dentically **d**istributed

---

### 擬陽性・偽陰性

- 擬陽性（false positive）
    - ニセの陽性ということで、ないものをあると判断してしまうこと
- 擬陰性（true negative）
    - ニセの陰性ということで、あるものをないと判断してしまうこと
- 擬陽性・偽陰性でない事象: 真陽性、真陰性と表現される

<center>ロボット工学だとあまり重要ではないが、医学・薬学などではとても重要</center>


---

## センサ値に混入する雑音のモデルの例（詳解4.3.1項）

- 計測距離$\ell$と向き$\varphi$に、それぞれ独立したガウス分布状の雑音を付加
    - $\ell$は真の距離に比例した大きさの標準偏差で
        - 遠くに行くほど距離計測が不確か
    - $\varphi$は距離に関係なく一定の大きさの雑音を　
- 数式
    - $\ell_t \sim \mathcal{N}\left[\ell | \ell^*_t, (\ell^*_t \sigma_\ell)^2 \right]$ 
    - $\varphi_t \sim \mathcal{N}\left(\varphi | \varphi^*_t, \sigma_\varphi^2\right)$
        - $^*$付きの変数は真の値
        - $\sigma_\ell, \sigma_\varphi$はパラメータ

![bg right:33% 100%](./figs/sensor_noise.gif)

---

## センサ値に混入するバイアスの例（詳解4.3.2項）

- 原因: カメラの取り付けの誤差、環境光、湿度、不十分なキャリブレーションなど（詳解2章）
    - 人間の場合: 低気圧の日に山が近く見える場合など　
- ロボットを扱っているとよく起こり、しかも厄介
    - 自己位置推定の出力がずっと同じ傾向でずれる
    - キャリブレーション地獄


---

### バイアスのシミュレーション

- モデルの例（詳解確率ロボティクスの例）
    - 計測距離$\ell$と向き$\varphi$を一定量ずらす
        - $\ell$については真の距離に比例した大きさで
    - シミュレーション開始時にずらす量を決定
        - これもガウス分布からドロー
        - 数式は省略　
- 右図: 計測距離が実際より短く出力される例
    - 全計測値が全時間帯で　

![bg right:30% 100%](./figs/sensor_bias.png)

---

## ファントム（詳解4.3.3項）

- ないはずのものが見える　
- モデル化の例
    - ある一定の確率で、ランドマークの位置を偽の位置にすり替え
        - 偽の位置: 一様分布からドロー
        - カメラの視界に合わない偽センサ値は除去
    - 図: 確率$0.5$ですり替え
        - （視界に入らないと除去されるので頻度はそれより低い）

![bg right:30% 100%](./figs/phantom.gif)

<center>graph-based SLAMなどで厄介に<br />（<span style="color:red">外れ値・アウトライアー</span>）</center>

---

## 見落とし（詳解4.3.4項）

- 見えるはずのものが見えない　
- モデル化の例
    - ある確率でランドマークを見落とす
    - 図: 確率$0.1$で見落とし発生　

![bg right:30% 100%](./figs/lost.gif)

「$\circ\circ$が見えたら$\times\times$する」というようなプログラムで深刻な問題に

---

## オクルージョン（詳解4.3.5項）

- 観測対象が物陰に
- センサによって様々な悪影響
    - 例: センサの前を人や別のロボットが横切ると・・・
        - LiDAR: 壁が近づいたような出力が得られる
        - カメラ: 物が欠けて小さく見える
- モデル化の例: ある一定の確率でセンサ値を書き換え
    - $\ \ell_t' \sim \mathcal{U}(\ell | \ell_t \le \ell < \ell_\max)$
        - $\ell_t$: もとの計測距離
        - $\ell_t'$: 書き換えられた計測距離
    - 一定時間バイアスを加えると、もっとタチの悪い系統誤差に

---

### オクルージョンのシミュレーションの例

- 図: 前ページのモデル化で、確率$0.5$で発生
    - この例では偶然誤差扱いであるが、実際は何秒か継続する大きな系統誤差になることが多い

![bg right:30% 100%](./figs/occlusion.gif)

---

## 観測方程式と確率的な観測モデル（詳解4.3.6項）

- 観測方程式の従来の形式（雑音つき）
    - $\boldsymbol{z}_t = \boldsymbol{h}_j (\boldsymbol{x}_t) + \boldsymbol{\varepsilon}_j$
        - $j$はランドマークID
    - 問題: 状態方程式と状態遷移モデルのときと同じ　

<center>状態遷移モデルと同じように確率的な表現が必要</center>

---

### <span style="color:red">観測モデル</span>の導入

- ランドマーク$j$を観測したときのモデル: $\boldsymbol{z}_t \sim p_j (\boldsymbol{z} | \boldsymbol{x}_t)$
- すべてのセンサ値に関する観測モデル　: $\textbf{z}_t \sim p (\textbf{z} | \boldsymbol{x}_t)$
    - $\textbf{z}$: センサ値のリスト　
    - $p$は<span style="color:red">観測分布</span>と呼びましょう
- 各ランドマークから得られるセンサ値が互いに独立なら
    - $\textbf{z}_t \sim p (\textbf{z} | \boldsymbol{x}_t) = \prod_{j=0}^{N_\textbf{m} -1} p_j (\boldsymbol{z} | \boldsymbol{x}_t)$

<conter>バイアスがある場合は「仮定」になるので注意</center>

---

## まとめ

- 移動ロボットにおける移動やセンシングに関する雑音や誤差を確認
- モデルの導入
    - 状態遷移モデル: $\boldsymbol{x}_t \sim p(\boldsymbol{x}|\boldsymbol{x}_{t-1}, \boldsymbol{u}_t)$
    - 観測モデル　　: $\textbf{z}_t \sim p (\textbf{z} | \boldsymbol{x}_t)$　

<center>次回以降、このモデルを前提にアルゴリズムを考えていく</center>
