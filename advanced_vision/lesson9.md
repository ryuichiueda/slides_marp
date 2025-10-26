---
marp: true
---

<!-- footer: "アドバンストビジョン第9回" -->

# アドバンストビジョン

## 第9回: 画像と言語、ロボット制御の融合

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 本題の前に
    - flow matching
- VLA（vision-language-action model）

---

## Flow matching（FL）[[Lipman 2022]](https://arxiv.org/abs/2210.02747)

- 拡散モデルとは別のアプローチで分布の変換を実現
- 拡散モデル（下図。再掲）
    - 現実（実際には訓練データ）の分布をガウス分布に変換・逆変換
        - 変換にはノイズを乗せていく方法が取られた
- FL: <span style="color:red">別にノイズを乗せなくても変形していけばいいんじゃないか？</span>

![w:900](./figs/ddpm.svg)

---

### 前ページのアイデアの問題

- 任意の時刻のノイズ画像が生成できない
    - 下図（再掲）
    - 各時刻の学習に支障
- FMはこれをなんとかした

![bg right:32% 100%](./figs/ddpm_training_data.png)

---

### FMのアイデア

- ガウス分布$p_0$と画像の分布など意味のある分布$p_1$の相互変換
    - <span style="color:red">ベクトル場</span>$\boldsymbol{u}_t$（$0\le t \le 1$）で考える
        - 各時刻で分布をひっぱる速度場を仮定
    - このベクトル場を再現する関数$\boldsymbol{v}_t(\boldsymbol{w})$をANNが学習
    - $\boldsymbol{v}_t(\boldsymbol{w})$と$\boldsymbol{u}_t$の差（2乗誤差）を損失関数に
- 問題としては最適輸送問題をANNに解かせることに
    - 最適輸送問題: 分布を一番楽な方法で変形する問題
$\qquad\qquad$![w:700](./figs/flow_matching_problem.svg)

---

### 問題の分解: 条件つきフローマッチング

- 拡散モデル同様、途中の$t$の画像（やデータ）が必要
    - 分布全体で考えると難しい
- $p_t$を条件付き確率に分解
    - $p_t(\boldsymbol{x}) = \int_{X_1} p_t(\boldsymbol{x} | \boldsymbol{x}_1)q(\boldsymbol{x}_1) \text{d}\boldsymbol{x}_1$
        - $q$: 訓練データの分布
            - $\boldsymbol{x}_1$の添え字: データの番号ではなく時刻
            - <span style="color:red">訓練データごとに損失関数を最小化しても全体の損失関数を最小化できる</span>
- ベクトル場$\boldsymbol{u}_t$も計算できる（重み付き平均）
    - $\boldsymbol{u}_t(\boldsymbol{x}) = \int_{X_1} \boldsymbol{u}_t(\boldsymbol{x}|\boldsymbol{x}_1) \dfrac{p_t(\boldsymbol{x} | \boldsymbol{x}_1)q(\boldsymbol{x}_1)}{p_t(\boldsymbol{x})} \text{d}\boldsymbol{x}_1$

![bg right:27% 95%](./figs/flow_matching_method.svg)

---

### フローの設計

- ひとつの条件付き確率に対し、途中の経路（分布）の定式化が必要
- とりあえずガウス分布を選択
    - $p_t(\boldsymbol{x}|\boldsymbol{x}_1) = \mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}_t(\boldsymbol{x}_1), \sigma_t(\boldsymbol{x}_1)^2I)$
        - $\boldsymbol{\mu}_t(\boldsymbol{x}_1), \sigma_t(\boldsymbol{x}_1)$は時間の関数と解釈したほうがよい
        - $\boldsymbol{\mu}_0(\boldsymbol{x}_1) = \boldsymbol{0}, \sigma_0(\boldsymbol{x}_1) = 1$
        - $\boldsymbol{\mu}_1(\boldsymbol{x}_1) = \boldsymbol{x}_1, \sigma_1(\boldsymbol{x}_1) = \sigma_\text{min}$

