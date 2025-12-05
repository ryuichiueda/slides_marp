---
marp: true
---

<!-- footer: "アドバンストビジョン第10回" -->

# アドバンストビジョン

## 第10回: 画像と言語、ロボット制御の融合II

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 本題の前に
    - flow matching
    - LoRA（low-rank adaptation）
- VLA（vision-language-action model）、ロボット基盤モデル
    - [河原塚先生のスライド](https://speakerdeck.com/haraduka/miru2025-tiyutoriarujiang-yan-robotutoji-pan-moderunozui-qian-xian)も参考になります

---

## Flow matching（FM）[[Lipman 2022]](https://arxiv.org/abs/2210.02747)

- 拡散モデルとは別のアプローチで分布の変換を実現
- 拡散モデル（下図。再掲）
    - 現実（実際には訓練データ）の分布をガウス分布に変換・逆変換
        - 変換にはノイズを乗せていく方法が取られた
- FM: <span style="color:red">別にノイズを乗せなくても変形していけばいいんじゃないか？</span>

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
- 全体のベクトル場$\boldsymbol{u}_t$も個々のもの（後述）が分かれば計算できる（重み付き平均）
    - $\boldsymbol{u}_t(\boldsymbol{x}) = \int_{X_1} \boldsymbol{u}_t(\boldsymbol{x}|\boldsymbol{x}_1) \dfrac{p_t(\boldsymbol{x} | \boldsymbol{x}_1)q(\boldsymbol{x}_1)}{p_t(\boldsymbol{x})} \text{d}\boldsymbol{x}_1$

![bg right:27% 95%](./figs/flow_matching_method.svg)

---

### フローの設計

- ひとつの条件付き確率に対し、途中の経路（分布）の定式化が必要
- とりあえずガウス分布を選択
    - $p_t(\boldsymbol{x}|\boldsymbol{x}_1) = \mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}_t(\boldsymbol{x}_1), \sigma_t(\boldsymbol{x}_1)^2I)$
        - 境界条件
            - $\boldsymbol{\mu}_0(\boldsymbol{x}_1) = \boldsymbol{0}, \sigma_0(\boldsymbol{x}_1) = 1$
            - $\boldsymbol{\mu}_1(\boldsymbol{x}_1) = \boldsymbol{x}_1, \sigma_1(\boldsymbol{x}_1) = \sigma_\text{min}$
    - フローはこうなる: $\boldsymbol{\psi}_t(\boldsymbol{x}) = \sigma_t(\boldsymbol{x}_1)\boldsymbol{x} + \boldsymbol{\mu}_t(\boldsymbol{x}_1)$
        - $t=0$の様々な箇所の$\boldsymbol{x}$が$\boldsymbol{x}_1$に向かう（右図）
        - まだ$\sigma_t(\boldsymbol{x}_1), \boldsymbol{\mu}_t(\boldsymbol{x}_1)$の形は決まっていない
            - 補足: いずれも$\boldsymbol{x}_1$ではなく時間の関数

![bg right:27% 95%](./figs/conditional_flow.svg)

---

### 最適輸送による設計

- この図のような一番素直なフローで分布を移したい$\Longrightarrow$最適輸送問題
   ![w:400](./figs/conditional_flow.svg)
- 条件つき最適輸送パス
    - フロー: $\boldsymbol{\psi}_t(\boldsymbol{x}) = \{1 - ( 1 - \sigma_\min)t\}\boldsymbol{x} + t \boldsymbol{x}_1$
        - $\boldsymbol{\mu}_t(\boldsymbol{x}_1)=t \boldsymbol{x}_1, \sigma_t(\boldsymbol{x}_1)=1 - (1- \sigma_\text{min})t$
- このときのベクトル場
    - $\boldsymbol{u}_t(\boldsymbol{x}|\boldsymbol{x}_1) = \dfrac{\sigma_t'(\boldsymbol{x}_1)}{\sigma_t(\boldsymbol{x}_1)}\{ \boldsymbol{x} - \boldsymbol{\mu}_t(\boldsymbol{x}_1) \} + \boldsymbol{\mu}_t'(\boldsymbol{x}_1) = \dfrac{\boldsymbol{x}_1 - (1-\sigma_\min)\boldsymbol{x}}{1-(1-\sigma_\min)t}$
- 損失関数
    - $\mathcal{L}_\text{CFM}(\boldsymbol{w}) = \big\langle \{ \boldsymbol{v}_t(\boldsymbol{\psi}_t(\boldsymbol{x}_0))  - [ \boldsymbol{x}_1 - (1 - \sigma_\min)\boldsymbol{x}_0 ] \}^2 \big\rangle_{t \sim \mathcal{U},q(\boldsymbol{x}_1), p(\boldsymbol{x}_0 )}$

---

### FMでできること

- [[Lipman 2022]](https://arxiv.org/abs/2210.02747)の図1、6、11〜
    - アルゴリズムの説明のための図だけど図4も面白い
- Stable Diffusion 3
- ロボットの制御（今回の後半にやります）
- 補足
    - 最適輸送の場合しか説明しませんでしたが、他にもいろいろ設計の余地があります

---

## Low-Rank Adaptation（LoRA）[[Hu2021]](https://arxiv.org/abs/2106.09685)

- 高効率なファインチューニング方法
- アイデア（一般的に<span style="color:red">アダプター</span>と呼ばれるもの）
    - 事前学習された行列状のパラメータを固定
    - 横にファインチューニング用のモデルを
    用意してパラメータの差分だけ計算
        - 下のモデルよりパラメータ数を小さく
            - 誤差逆伝搬の計算量が減る
        - どうやって少なくするかは次ページ

![bg right:32% 100%](./figs/LoRA.svg)

---

### パラメータの削減方法

- 事前学習された$\alpha \times \beta$行列$W$に対し
次の行列を準備
     - 行列$A$（$d\times \beta$）
     - 行列$B$（$\alpha \times d$）
- ファインチューニングされた行列: $W' = W + BA$
    - $W$のパラメータ数: $\alpha \beta$
    - $BA$のパラメータ数: $(\alpha + \beta)d$
        - 小さい$d$でパラメータ数削減
- 入力の次元が$A$で落ちて$B$で元通りに
    - 潜在空間による次元圧縮のようなもの

![bg right:40% 100%](./figs/lora_matrixes.svg)

---

### Robotics Transformer 2（RT-2）[[Brohan2023]](https://arxiv.org/abs/2307.15818)（[サイト](https://robotics-transformer2.github.io/)）

- この論文の概要: "We refer to such category of models as vision-language-action models (VLA) and ..."ということで、ここでVLAという言葉が出現
- 構造（2種類ある）
    - PaLIにいろいろくっつけたもの（RT-2-PaLI-X）
    - PaLM-Eベースのもの（RT-2-PaLM-E）
        - 以後はPaLM-Eの使用を前提に話します
        - なんでもトークンにして突っ込めてトークンを話すモデル

<center style="padding-top:2em">だとしたらPaLM-EとRT-2の違いはなに？</center>

---

### PaLM-Eとの違い（VLAと呼ぶ理由）

- ロボットの動作（言語レベルではなく<span style="color:red">数値レベル</span>のもの）も一緒に学習
    - 数値レベル: 関節の回転角や移動量などのこと
        - 例: 論文の図1の訓練データのペア（一番下のやつ）
            - Q: What should the robot do to `<task>`?
            - A: 変位: $(0.1, -0.2, 0)$、回転: $(10^\degree, 25^\degree, -7^\degree)$
- $\Longrightarrow$ PaLM-Eと違って直接的にロボットの動作を出力可能
    - 制御のレイヤーを考えるとRT-1の後継と考えることが妥当

---

### OpenVLA[[Kim2024]](https://arxiv.org/abs/2406.09246)

- その名の通りオープンなVLA
- オープンにするときの要件
    - ユーザーのロボットが違うのでファインチューニングしやすくすると便利
$\Longrightarrow$<span style="color:red">LoRAが使えるようになっている</span>
       - （補足: 多種のロボットの訓練データで学習したVLAは、ファインチューニングなしでも少しのロボットの違いをある程度吸収）

---

### 構造（[[論文]](https://arxiv.org/abs/2406.09246)の図2）

- 画像処理の部分: SigLIPとDINOv2という2つのモデルからそれぞれ独立にトークンを生成
    - SigLIP[[Zhai2023]](https://arxiv.org/abs/2303.15343): ゼロショットで画像分類するモデル
        - softmaxでの多数のものから物体を分類をするのではなく、画像と短文がどれだけ合っているか確率で出力
        - 画像全体の説明をトークンに
    - DINOv2[[Oquab2023]](https://arxiv.org/abs/2304.07193): 画像の基盤モデル
        - 画像の低レベルの特徴量を抽出してトークンに
- LLMのパート: Llama（Large Language Model Meta AI）
    - 下のAction De-tokenizerに入力するトークンを出力
- 行動の生成: 「Action De-tokenizer」（どんな実装か不明。コードを読め？）


---

### 訓練データ・訓練方法

- 事前学習の訓練データ: Open X-Embodiment dataset
    - 70台、200万のロボットの軌道
- ファインチューニング
    - 訓練データはユーザーが用意
    - 先述のようにLoRAが使える

---

### $\pi_0$[[Black 2024]](https://arxiv.org/html/2410.24164v1)（[サイト](https://www.physicalintelligence.company/blog/pi0)）

- Physical Intelligence社が開発したVLAモデル
- 片腕、双腕、移動マニピュレータなど多種のロボットのデータを一度に学習
    - 68種のタスクの独自データセットとOpen X-Embodiment dataset
        - それぞれ7種+22種のロボットのデータを含む
        - 1万時間超の長さ
- ACTで使われていたaction chunking architectureで50Hzの制御周期を達成
    - ただし、CVAEではなくconditional flow matching（CFM）を使用
- 使用例: 上記のサイトにいろいろ
    - 洗濯物を洗濯機から取り出して畳むなど複雑で細かい動作を実現

---

### 構造（[このページ](https://arxiv.org/html/2410.24164v3)の図3）

- PaliGemma
    - オープン、軽量なGoogleのVLM（30億パラメータ）
    - 入力: 画像と作業の指示
    - 出力: トークン
- action expert
    - ロボットの動作のシーケンスを出力（3億パラメータ）
    - 入力: PaliGemmaからのトークンとロボットの状態
    - 出力: 動作シーケンス
        - <span style="color:red">フローマッチングで</span>

---

### フローマッチングの使い方

- ニューラルネットの作るベクトル場の変数に観測データも入れて学習
    - 損失関数: $\mathcal{L}_\text{CFM}(\boldsymbol{w}) = \big\langle \{ \boldsymbol{v}_{\boldsymbol{w}}(A_t^\tau,\boldsymbol{o}_t)  - \boldsymbol{u}(A_t^\tau | A_t) \}^2 \big\rangle_{q(A_t^\tau | A_t), p(A_t | \boldsymbol{o}_t ), \tau \sim \text{Beta}}$
        - $\tau$がFMの時刻（$0 \le \tau \le 1$）
            - $t$は実際の時刻（ロボットの動作のステップ）
            - $\tau$が小さいときの損失関数を重視したい
            $\rightarrow$ベータ分布でバイアスをかけて重み付き平均で評価
        - $A_t$（時刻$t$での動作シーケンス）が訓練データ
            - 観測や指示$\boldsymbol{o}_t$と対になっている
        - $q(A_t^\tau | A_t ) = \mathcal{N}[\tau A_t, (1-\tau)I]$（最適輸送パス）
- 使用（推論）時
    - $A_t^0$に雑音を入れると$\boldsymbol{o}_t$に条件づけられた$\boldsymbol{v}_\boldsymbol{w}$に導かれて$A_t^1$が生成される

---

## まとめ

- VLAというものができた
    - この2, 3年でロボットが人間の指示が分かるようになってしまった
    - しかも相当細かい作業もできる
    - 今は性能が出ないタスクでもそのうち出るようになる
- 今後
    - 自身の研究テーマについてもういっぺんよく考えてみましょう
        - 自身はロボットの何を解決したいのか、それは未解決なのかもういっぺん考えてみる
