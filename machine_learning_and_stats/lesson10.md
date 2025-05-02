---
marp: true
---

<!-- footer: "機械学習（と統計）第10回" -->

# 機械学習

## 第10回: クラスタリングとベイズ推論

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 変分推論

---

## 前回のおさらい

- k-means、EM法をやった
    - EM法は確率の考えを導入していたが、第6回でやったような「分布の分布」までは考えられていない

<center>「分布の分布」は考えられるのか?→できる（ただしかなりややこしい）</center>

---

## 第6回のおさらい

- 実験の成功、失敗の結果から、「成功率の分布」を考えた
    - ベータ分布: $p(x) = \eta x^{\alpha-1}(1-x)^{\beta-1}$
    - 実験の結果を1つずつ反映していくと、成功率の分布が変化していった
        - 下図: 成功、成功、失敗、失敗の場合の分布の推移
            - <span style="color:red">成功率1/2と決めつけない</span>
    - 分布の変化はベイズの定理で計算できた

![](./figs/success_distribution.png)

---

## 混合ガウス分布のベイズ推定

- 「混合分布の分布」を考える
    - 右図のような様々な分布に確率（の密度）を与える
    - 最尤なものでなく、分布の分布自体を計算
- 第6回との違い
    - パラメータの数が膨大
        - ガウス分布が$n$個（$n$: クラスタの数）
        - 潜在変数が$Nn$個（$N$: データの数）
    - （単純な）ベイズの定理で計算できない
- どうするか?
    - EM法のように少しずつ分布（の分布）を変えていく

![bg right:20% 85%](./figs/various_mixture_gauss.png)

---

### 推定対象のパラメータ

- 各ガウス分布のパラメータ: $\boldsymbol{\mu}_j, \Sigma_j, \pi_j$
    - （おさらい）混合ガウス分布:
        - $p(\boldsymbol{x} | \boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n})$
        $=  \sum_{j=1}^n \pi_j \mathcal{N}(\boldsymbol{\mu}_j, \Sigma_j)$
        （$\pi_1 + \pi_2 + \dots + \pi_n = 1$）
- 各データ$\boldsymbol{x}_i$（$i=1,2,\dots,N$）の所属$k_{i}$
    - どのガウス分布に所属しているか
    - 潜在変数

![bg right:40% 100%](./figs/gauss_mixture.png)


---

### 混合ガウス分布の分布のモデル化（分布の分布）

- 混合比率$\pi_{1:n} = (\pi_1, \pi_2, \dots, \pi_n)$の分布: ディリクレ分布
    - ディリクレ分布: $\text{Dir}(\pi_{1:n} | \alpha_{1:n}) = \eta \pi_1^{\alpha_1-1}\pi_2^{\alpha_2-1}\dots\pi_n^{\alpha_n-1} = \eta \prod_{j=1}^n \pi_j^{\alpha_j - 1}$
        - ベータ分布をコインの裏表だけでなくもっと多くの変数
        （例: さいころなら6）に拡張したもの
        - 様々な混合比率のパターンに確率の密度を与える
    - $\alpha_{1:n}$: $\pi_{1:n}$のばらつきを決めるパラメータ
        - $\alpha_{1:n}$の合計値が大きくなるほど値が定まってくる
            - 合計値が大きくなる=さいころをたくさん投げて出目の傾向が分かってきた状態

---

### 混合ガウス分布の分布のモデル化（分布の分布。続き）

- 各ガウス分布のパラメータ$\boldsymbol{\mu}_j, \Lambda_j$の分布: ガウス-ウィシャート分布
    - $\Lambda_j$（精度行列）$= \Sigma_j^{-1}$（計算しやすいので考える）
    - ガウス-ウィシャート分布: $p(\boldsymbol{\mu}_j, \Lambda_j) = \mathcal{N}(\boldsymbol{\mu}_j|\boldsymbol{m}_j, (\beta_j \Lambda_j)^{-1})\mathcal{W}(\Lambda_j | W_j, \nu_j)$
        - ウィシャート分布: 精度行列の分布
    - 各ガウス分布の分布を決めるパラメータ: $\boldsymbol{m}_j, \beta_j, W_j, \nu_j$


---

### これからやること

1. 適当に初期のクラスタと混合ガウス分布の分布を決める
    - $k_{ij}=1$となる確率$r_{ij}$を初期化
    - パラメータ$\boldsymbol{m}_{1:n}, \beta_{1:n}, W_{1:n}, \nu_{1:n}, \alpha_{1:n}$の初期値を与える
        - $\boldsymbol{m}'_{1:n}, \beta'_{1:n}, W'_{1:n}, \nu'_{1:n}, \alpha'_{1:n}$としましょう
2. 上記の初期値から、混合ガウス分布の事後分布のパラメータ$\boldsymbol{m}_{1:n}, \beta_{1:n}, W_{1:n}, \nu_{1:n}, \alpha_{1:n}$を計算
    - EM法のMステップに相当（<span style="color:red">変分Mステップ</span>）
3. 計算した$\boldsymbol{m}_{1:n}, \beta_{1:n}, W_{1:n}, \nu_{1:n}, \alpha_{1:n}$から$k_{i,1:n}$の事後分布を計算
    - EM法のEステップに相当（<span style="color:red">変分Eステップ</span>）
- 注意: $\boldsymbol{m}'_{1:n}, \beta'_{1:n}, W'_{1:n}, \nu'_{1:n}, \alpha'_{1:n}$は固定
    - 事前分布を固定して、繰り返し事後分布の解を良くしていく

---

### 変分Mステップ

- 補助の数値を計算
    - $N_j = \sum_{i=1}^N r_{ij}$
    - $\bar{\boldsymbol{x}}_j = \dfrac{1}{N_j} \sum_{i=1}^N r_{ij}\boldsymbol{x}_i$
    - $\Sigma_j = \dfrac{1}{N_j} \sum_{i=1}^N r_{ij}(\boldsymbol{x}_i - \bar{\boldsymbol{x}}_j)(\boldsymbol{x}_i - \bar{\boldsymbol{x}}_j)^\top$
- 事後分布のパラメータを計算
    - $(\alpha_j, \beta_j, \nu_j) =(\alpha_j', \beta_j', \nu_j') + (N_j, N_j, N_j)$（データの個数だけ増大） 
    - $\boldsymbol{m}_j = (\beta_j' \boldsymbol{m}_j' + N_j \bar{\boldsymbol{x}}_j ) /\beta_j\qquad\qquad\qquad$（$\boldsymbol{\mu}_j$の中心の調整）
    - $W^{-1}_j = W'^{-1}_j + N_j \Sigma_j + \dfrac{\beta'_j N_j}{\beta'_j+ N_j} (\bar{\boldsymbol{x}}_j - \boldsymbol{m}_j')(\bar{\boldsymbol{x}}_j - \boldsymbol{m}_j')^\top$
        （各ガウス分布の共分散行列の調整）

---

### 変分Eステップ

- $k_{i,1:n} =(k_{i1}, k_{i2},\dots,k_{in})$の分布: 次の計算で導出
    - $q(k_{i,1:n}) = \langle p(\boldsymbol{x}_i, k_{i,1:n}, \pi_{1:n}, \boldsymbol{\mu}_{1:n}, \Lambda_{1:n}) \rangle_{\pi_{1:n}, \boldsymbol{\mu}_{1:n}, \Lambda_{1:n}}$
- 計算結果: 次の$r_{ij}$が、$k_{ij}$が$1$になる確率
    - $r_{ij} = \eta \rho_{ij}$
        - $\log_e \rho_{ij} = -\dfrac{1}{2} d \beta_j^{-1} -\dfrac{1}{2} \nu_j(\boldsymbol{x}_i - \boldsymbol{m}_j)^\top W_j (\boldsymbol{x}_i - \boldsymbol{m}_j)$
         $\quad+ \dfrac{1}{2} \sum_{j=1}^d \psi\left(\dfrac{\nu_j + 1 - j}{2}\right) + \dfrac{1}{2}\log_e | W_j | + \eta'$
        $\quad+\psi(\alpha_j) - \psi\left( \sum_{j=1}^K \alpha_j \right)$
        - 式中の変数はすべて一時的に値が決まっているか既知なので計算可能
            - $d$: $\boldsymbol{x}$の次元
            - $\psi$: ディガンマ関数という関数（高級な言語にはライブラリあり）
