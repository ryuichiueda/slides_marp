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
    - に<span style="color:red">ベクトル場</span>$u_t$（$0\le t \le 1$）で考える
    - 各時刻で分布をひっぱる速度場を仮定
    - このベクトル場を再現する関数$v_t(\boldsymbol{w})$をANNが学習
    - $v_t(\boldsymbol{w})$と$u_t$の差（2乗誤差）を損失関数に
- 問題としては最適輸送問題をANNに解かせることに
    - 最適輸送問題: 分布を一番楽な方法で変形する問題

![bg right:27% 95%](./figs/flow_matching_problem.svg)

---

### 訓練データの作成

- 拡散モデル同様、途中の$t$の画像が必要

![bg right:27% 95%](./figs/flow_matching_method.svg)
