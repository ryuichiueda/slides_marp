---
marp: true
---

<!-- footer: "アドバンストビジョン第9回" -->

# アドバンストビジョン

## 第9回: 画像と言語、ロボット制御の融合I

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 本題の前に
    - PaLM、PaLI
- ANNによるロボットの制御
    - VLA（vision-language-action model）という言葉ができる以前のもの
        - VLAという言葉が出た後の話については次回

---

## PaLM[[Chowdhery2022]](https://arxiv.org/abs/2204.02311)

- Pathways Language Model（Googleの大規模言語モデル）
    - Transformerのデコーダで構成されているのでGPTのように機能
    - 後述のようにGoogleのロボット制御モデルに用いられている
    - 新しいバージョンのPaLM 2[[Anil2023]](https://arxiv.org/abs/2305.10403)は100以上の言語を使いこなす（多言語翻訳が可能）

---

## PaLI[[Chen2022]](https://arxiv.org/abs/2209.06794)

- Pathways Language and Image model
    - 構造: 論文の図1（ViT+Transformerエンコーダ+Transformerデコーダ）
        - 言葉のトークンもViTの出す画像の特徴量のトークンも同じ長さのベクトルにしてTransformerに入力
        - 交差注意機構も使うらしい（未調査）

---

## ANNによるロボットの制御

---

### 基本的な考え方

- 様々なモーダルの情報を動作に変換
    - 画像、センサ
    - 言葉による指示
    - 自身の内部状態

---

### ANNによるロボットの制御の課題

- 訓練データどうするの？
    - たぶんCLIPのときのようなネットのデータはない
    - <span style="color:red">先に答えを言うと、人間がひたすらデータを生成</span>
        - テーブル
- 方策（制御則）等の表現方法
    - Transformerのデコーダだと1つずつ細かい動きを出していくことに
- 汎化
    - 教えた動作から外れた動作もできる
    - おそらく言葉の存在（意味の理解）が可能にする

---

### Robotics Transformer-1（RT-1）[[Brohan 2022]](https://arxiv.org/abs/2212.06817)（[動画](https://www.youtube.com/watch?v=UuKAp9a6wMs)）

- 構造・入出力の概要: 論文の図3（まだVLAという言葉はない）
    - Universal Sentence Encoder: FiLMのパラメータを出力
    - FiLM EfficientNet-B3とTokenLearner
        - 入力: 時間差のある6枚の画像と言葉によるロボットへの指示
        - 出力: 512次元の48個のトークン
    - Transformer（デコーダー）
        - 入力: 48個のトークンに位置埋め込みしたもの
        - 出力: ロボットの行動（11次元の離散空間中の点）
            - ロボット: モバイルマニピュレータ（[Everyday Robots](https://x.company/projects/everyday-robots/)）
            - モード1次元、腕の動き7次元、位置・向き3次元
            - 3Hz

---

### RT-1の訓練データ（力づく）

- 図2のようなキッチン（3種類）やテーブルのような環境で
ロボットを動かして訓練データを採取
    - 人が遠隔操作
    - やった作業に人間がテキストの解説をつける
        - これで画像とテキストと動作のセットができる
- 採取した訓練データ
    - 744タスク（論文は「skill」と表現）（論文の表1）
    - 13のロボット
    - 13万エピソード

---

### Universal Sentence Encoder（[[Cer 2018]](https://arxiv.org/abs/1803.11175)）

（重要そうだけど概要だけ）

- 文をベクトルにする
    - 似たような文のベクトルの内積が大きくなるように
- 構造: Transformer（エンコーダ）or Deep Average Network Encoder（[[Iyyer 2015]](https://aclanthology.org/P15-1162/)）
- 学習方法
    - 前後の文の予測
    - 質問文への返答文の予測
    - 前提と仮説の文が矛盾しているかどうか

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
- 6枚の画像の各8トークンが順番に並べられて文のような入力に
    - これが何をすべきかを示す時系列情報に
- 出力: 先述のようにロボットを動かすために必要な次元分のパラメータとモード
    - モード: arm, base, terminate
- 訓練データでの学習
    - 言語による指示と画像から次のステップの行動を予測
        - デコーダのマスク機能を使った学習と思われる
        （注意: Transformerだけでなくモデル全体が学習）

---

### RT-1の達成事項

- 学習した種類のタスクを97\%の成功率で達成
    - 動作の例: 論文の図5
- ロバスト性
    - 学習したキッチンと異なるキッチンでのタスク
    - 様々なテーブルクロス
- 学習したものより長い/抽象化されたタスクへの対応
    - 例
        - "how would you throw away all the items on the table?"
        - "near a sink"などの直接的でない場所の指定
- 他
    - シミュレーション or 異なるロボットから得られる訓練データの使用

---

### PaLM-E[[Driess2023]](https://arxiv.org/abs/2303.03378)

- 身体性マルチモーダル言語モデル
    - 身体性: ロボットの身体の情報を織り込むということ
- Googleの大規模言語モデルPaLMに画像やロボットの知覚情報を入力できるようにして、タスクのやりかたを作文できるようにしたモデル
- 構成: 論文の図1

