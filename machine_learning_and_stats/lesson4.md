---
marp: true
---

<!-- footer: "機械学習（と統計）第4回" -->

# 機械学習

## 第4回: 様々な分布II

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 離散型確率分布と連続型確率分布の違い
- 二項分布、ガウス分布以外の重要な分布について確認
    - ポアソン分布
    - 指数分布
    - ベータ分布
- 多次元の分布

<center>式も重要ですけど現象との関係に注目しましょう</center>

---

## 離散、連続

- 確率変数が整数のときと実数（小数）のときがある
    - 二項分布: 整数（<span style="color:red">離散型確率分布</span>）
    - ガウス分布: 実数（<span style="color:red">連続型確率分布</span>）
- 両者の共通点と相違
    - 共通していること: 確率の合計は1
    - 違うところ
        - 離散型の場合は各変数の確率を足せば1に
        - 連続型の場合は積分しないといけない
            - グラフの縦軸は確率ではなく<span style="color:red">密度</span>
            - 変数の範囲$\times$密度$=$確率（次ページ）

![bg right:30% 100%](./figs/bin_and_gauss2.png)

---

### 連続型確率分布からの確率の求め方

- 実のところ積分する機会は少ない（安心）
- 累積分布関数（の表）を使用
    - $\text{Pr}\{$変数の値が$x$以下$\}$のグラフや表
    - 例: 右図の青色の線
        - ガウス分布の累積分布
        - 緑色の線（ガウス分布の<span style="color:red">確率密度関数</span>）の積分値
- [表の例](https://unit.aist.go.jp/mcml/rg-orgp/uncertainty_lecture/normsdist.html)（左側からの積分値になっている）
- もちろん確率密度関数から表計算ソフトで求めてもよい（右図はExcelで描画）

![bg right:40% 100%](./figs/gauss_accum.png)

---

### 問題

- [前ページの表](https://unit.aist.go.jp/mcml/rg-orgp/uncertainty_lecture/normsdist.html)を使って、ガウス分布にしたがう変数が、ガウス分布の$2\sigma～3\sigma$の範囲に入る確率を計算してみましょう
    - 当該範囲は両側にあるので注意
* 答え: $2(0.02275-0.00135)=0.0428$

---

## さまざまな分布

- いろんな自然、社会現象に現れる分布を見ていきましょう

---

### ポアソン分布

- ある事象が一定時間に起こる回数がしたがう分布
    - 式: $P(x) = \dfrac{n^x e^{-n}}{x!}  = \eta \dfrac{n^x}{x!}$
        - $n$: ある期間にその事象が起こる回数
- 事象の例
   - 1ヶ月以内の地震の数など
- 分布の形
    - $n$が大きいとガウス分布に近づく
        - なんででしょう？
            * 大量のコインを投げて何枚表になるでしょうかという問題と等価になる

![bg right:30% 80%](./figs/poisson.png)


---

### 問題

- 問題: 年1回大きな地震が起こる地域で、次の3つの確率を求めてみましょう
    - ある年に起こらない確率
    - 1回起こる確率
    - 3回以上起こる確率
- ポアソン分布の式（再掲）: $P(x) = \dfrac{n^x e^{-n}}{x!}$
    - $0! = 1$に注意
- 答え
    * $P(0) = e^{-1} = 0.36789744... \approx 0.37$
    * $P(1) = e^{-1} = 0.36789744... \approx 0.37$（きっちり1回の年は4割もない）
    * $\text{Pr}(3$回以上$) = 1 - \left\{P(0) + P(1) + P(2)\right\}$
    $\qquad\qquad\qquad= 1 - (e^{-1} + e^{-1} + e^{-1}/2) \approx 0.08$

---

### 指数分布

- ある事象が起こってから次に起こるまでの間隔がしたがう分布
    - 例: 地震と地震の間の時間間隔
    - ポアソン分布と表裏一体（違いはちゃんと説明できるようにしましょう）
- 確率密度関数: $P(x) = \dfrac{1}{t}\exp\left\{-\dfrac{x}{t}\right\}$
    - $t$: 間隔の平均値（$1/t$: ポアソン分布の$n$）
- 累積分布関数: $\text{Pr}\{$値が$x$以下$\} = 1 - \exp(-x/t)$

![bg right:30% 90%](./figs/exp_dist.png)

---

### 問題

- 1年に1回地震が起こるとき、半年以内に起こる確率は$0.5$より大きい？
- ヒント: 累積分布関数（再掲）
    - $1 - \exp(-x/t)$
* 答え
    * $1 - \exp(-1/2)= 1 - 1/\sqrt{e} \approx 0.393$
        * $0.5$より小さい

---

### ベータ分布

- 式: $p(x) = \dfrac{ x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)} = \eta x^{\alpha-1}(1-x)^{\beta-1}$
    - $B$はベータ関数というややこしい関数
- コインの表、裏がそれぞれ$(\alpha-1)$、$(\beta-1)$回出たときに、表が出る確率の分布
    - 投げるほど分布が尖っていく
        - 数学的な解釈: ある確率に収束していく
        - 生物的な解釈: ある確率なのではないかとだんだん確信していく

![bg right:30% 90%](./figs/beta.png)

---

## 多次元の分布

- 世の中の状態、現象は互いに絡み合っている
    - 例: 身長の高い人は（そうでない場合もあるけど）体重も重い
- 次の資料で関係していそうな項目を見つけてみましょう
    - [日本病院薬剤師会のサイトにあるデータ](https://www.jshp.or.jp/activity/zasshi-toko/kaiseki-6.xls)（Excelファイル）

---

### 関係のありそうな項目

- 例外も多いが、どっちかが大きいともう一方も大きい
- いろいろ考えることがある
    - 世の中には逆のパターンもありそう
    - 中性脂肪が血圧にかかわらず以上に多い人たちがいるけどなに?
    - 例外のせいでSNSで喧嘩が起きてない?
    - <span style="color:red">数学的にはどう扱う?</span>

![bg right:40% 100%](./figs/relations.png)


---

### 共分散

- ふたつの変数の大小の傾向が一致しているかどうかを調べる統計値
- データがあるときの計算方法
    - データを$(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n)$とすると
    $s_{xy} = \dfrac{1}{1-n}\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})$
        - $\bar{x}, \bar{y}$: それぞれ$x$、$y$の平均値

<center>どんな値なのでしょうか？いくつかの例で計算してみましょう</center>

---

### 共分散の計算1

- 右のデータの場合の共分散は?
- 答え
    * $(\bar{x}, \bar{y}) = (1, 0)$なので
    * $s_{xy}=(1+2 + 0 + 10$$-4 + 0 + 7)/6 = 8/3$


![bg right:50% 100%](./figs/cov1.png)

---

### 共分散の計算2

- じゃあこのデータはどうでしょう？
- 答え
    * $(\bar{x}, \bar{y}) = (1, 1)$なので
    * $s_{xy}=(2+1-10-8$
    $-8-21)/6 = -22/3$


![bg right:50% 100%](./figs/cov2.png)


---

### 共分散の計算3

- このデータは？
- 答え
    * $(\bar{x}, \bar{y}) = (1, 1)$なので
    * $s_{xy}=(2-2+2+5-4$
    $+0-7/6 = -2/3$


![bg right:50% 100%](./figs/cov3.png)


---

### 共分散の値の性質

- 正負が重要
    - 片方が大きいともう片方も大きい$\Longrightarrow$正
    - 片方が大きいともう片方は小さい$\Longrightarrow$負
    - 双方の大小にあまり関係がない$\Longrightarrow$ゼロに近く
- なんでそうなるか式をもう一度見てみましょう
    - $s_{xy} = \dfrac{1}{1-n}\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})$

---

### 二次元のガウス分布

- $n$個の変数がそれぞれガウス分布にしたがう場合、<span style="color:red">$n$次元のガウス分布</span>を当てはめることができる
- 二次元のガウス分布の場合（形状の例は次のページ）
    - $P(x,y | \mu_x, \mu_y, \Sigma) = - \eta \exp \left\{ -\frac{1}{2}(x-\mu_x \ y-\mu_y)\Sigma^{-1}\begin{pmatrix}x-\mu_x \\ y-\mu_y\end{pmatrix}\right\}$
        - $(\mu_x \ \mu_y)$: 中心
        - $\Sigma = \begin{pmatrix}\sigma_{xx} & \sigma_{xy} \\ \sigma_{xy} & \sigma_{yy}\end{pmatrix}$: <span style="color:red">共分散行列</span>
            - $\sigma_{xx}, \sigma_{yy}$: それぞれ$x$、$y$の分散
            - $\sigma_{xy}$: 共分散
    - ソフトウェアを使う上では$\mu_x, \mu_y, \sigma_{xx}, \sigma_{yy}, \sigma_{xy}$で形が決まることが重要


---

### 二次元のガウス分布

- 共分散の値だけ変えて描画したもの（縦軸は密度）
    - 共通のパラメータ: $(\mu_x, \mu_y) =(5,5), (\sigma_{xx}, \sigma_{yy}) =(2,1)$
    - 上: <span style="color:red">$\sigma_{xy}=1$</span>
    - 下: <span style="color:red">$\sigma_{xy}=-1$</span>

![bg right:40% 100%](./figs/2d_gausses.png)
