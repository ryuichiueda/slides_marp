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
- ANNによるロボットの制御
    - VLA（vision-language-action model）、ロボット基盤モデル
    - [河原塚先生のスライド](https://speakerdeck.com/haraduka/miru2025-tiyutoriarujiang-yan-robotutoji-pan-moderunozui-qian-xian)も参考になります

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
    - このときのベクトル場
        - $\boldsymbol{u}_t(\boldsymbol{x}|\boldsymbol{x}_1) =\dfrac{\sigma_t(\boldsymbol{x}_1)'}{\sigma_t(\boldsymbol{x}_1)}\{\boldsymbol{x} - \boldsymbol{\mu}_t(\boldsymbol{x}_1)\} + \boldsymbol{\mu}_t'(\boldsymbol{x}_1)$
            - $'$は時間の微分

![bg right:27% 95%](./figs/conditional_flow.svg)

---

### 最適輸送による定式化

（まだ講師の頭の整理がついていないので雰囲気だけ）

- 途中（時間の関数としての$\boldsymbol{\mu}_t(\boldsymbol{x}_1)$と$\sigma_t(\boldsymbol{x}_1)$）には自由度がある
    - なるべく素直なフローで分布を移したい$\Longrightarrow$最適輸送問題
- 条件つき最適輸送パス
    - $\boldsymbol{\mu}_t(x)=t x_1, \sigma_t(x)=1 - (1- \sigma_\text{min})t$
        - とても単純
    $\Longrightarrow \boldsymbol{u}_t(\boldsymbol{x}|\boldsymbol{x}_1) = \dfrac{\boldsymbol{x}_1 - (1-\sigma_\min)\boldsymbol{x}}{1-(1-\sigma_\min)t}$
- 損失関数
    - $\mathcal{L}_\text{CFM}(\boldsymbol{w}) = \big\langle \{ \boldsymbol{v}_t(\boldsymbol{\psi}_t(\boldsymbol{x}_0))  - [ \boldsymbol{x}_1 - (1 - \sigma_\min)\boldsymbol{x}_0 ] \}^2 \big\rangle_{t \sim \mathcal{U},q(\boldsymbol{x}_1), p(\boldsymbol{x}_0 )}$
        - ここで$\boldsymbol{\psi}_t(\boldsymbol{x}) = \{1 - ( 1 - \sigma_\min)t\}\boldsymbol{x} + t \boldsymbol{x}_1$（フロー）

---

### FMでできること

- [[Lipman 2022]](https://arxiv.org/abs/2210.02747)の図1、6、11〜
    - アルゴリズムの説明のための図だけど図4も面白い
- Stable Diffusion 3
- ロボットの制御（これからやります）

---

## ANNによるロボットの制御

---

### Vision-Language-Action（VLA）モデル

- 言語$\rightarrow$動作という変換が必要
    - 「言語$\rightarrow$画像」のようにできないだろうか？
- 従来のようにセンサ$\rightarrow$動作という変換も必要
    - センサ=視覚（や視覚と同等に扱える信号）と考えると
    「画像$\rightarrow$動作」という変換が必要となる

<center style="color:red;padding-top:2em">「画像、言語、動作（VLA）の相互変換」というアイデアに</center>

---

### ANNによるロボットの制御の課題

- 訓練データどうするの？
    - たぶんCLIPのときのようなネットのデータはない
    - <span style="color:red">先に答えを言うと、人間がひたすらデータを生成</span>
        - テーブル
- 方策（制御則）等の表現方法

---

### Robotics Transformer-1（RT-1）[[Brohan 2022]](https://arxiv.org/abs/2212.06817)（[動画](https://www.youtube.com/watch?v=UuKAp9a6wMs)）

- 構造・入出力の概要: 論文の図3
    - Universal Sentence Encoder: FiLMのパラメータを出力
    - FiLM EfficientNet-B3とTokenLearner
        - 入力: 時間差のある6枚の画像と言葉によるロボットへの指示
        - 出力: 512次元の48個のトークン
    - Transformer（デコーダー）
        - 入力: 48個のトークンに位置埋め込みしたもの
        - 出力: ロボットの行動（11次元の離散空間中の点）
            - ロボット: モバイルマニピュレータ
            - モード1次元、腕の動き7次元、位置・向き3次元
            - 3Hz

---

### Universal Sentence Encoder（[[Cer 2018]](https://arxiv.org/abs/1803.11175)）

（重要そうだけど概要だけ）

- 文をベクトルにする
- 構造: Transformer（エンコーダ） or Deep Average Network Encoder（[[Iyyer 2015]](https://aclanthology.org/P15-1162/)）
- 学習方法
    - 前後の文の予測
    - 質問文への返答文の予測
    - 前提と仮設の文が矛盾しているかどうか

---

### Transformerより前の部分

- FiLM EfficientNet-B3とTokenLearnerの2つの部分
- FiLM EfficientNet-B3: 各画像からトークンへの変換
    - EfficientNetというネットワークで画像の特徴量を抽出
        - 言葉をFiLMで変換して特徴量に強弱をつける
    - 1つの画像に対し、512次元の81個のベクトル（vision-language tokens）を出力
- TokenLearner[[Ryoo 2021]](https://research.google/pubs/tokenlearner-adaptive-space-time-tokenization-for-videos/)
    - トークンの数を減らす（圧縮する）役割
        - もともとViTの入力ベクトル数を減らすためのもの
    - $81\rightarrow8$（6枚の画像で48トークン。512次元）


---

### Transformerの部分

- 8個の自己注意機構の層、1900万パラメータ


---

### $\pi_0$[[Black 2024]](https://arxiv.org/html/2410.24164v1)

- Physical Intelligence社が開発したVLAモデル
- 「ロボット基盤モデル」と呼ばれるもののひとつ

