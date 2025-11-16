---
marp: true
---

<!-- footer: "2025年12月2日 RSJセミナー" -->

# 自律移動と最適制御

-大域計画, 障害物回避, 機械学習, 潜在空間, 伝統的な制御の統一的な理解のために-

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 本日の話の動機（これだけで終わらないようにします）
- 探索問題と最適制御の接続
- ベルマン方程式とポントリャーギンの最大原理
- 潜在空間での制御
- その先

---

## この発表の動機: 「みんな仲良く」

- 自身の経験
    - 制御ゴリゴリの人と学習の人で会話が合わない
        - 同じはずなんだけどなあ・・・
    - 価値反復使ってたら「なんで学習でやらないんですか？」と質問された
        - 同じはずなんだけどなあ・・・
    - 制御をポントリャーギンの最大（最小）限理から考えている人とベルマン方程式から考えている人で会話が合わない
        - 同じはずなんだけどなあ・・・
- 自分の頭の中ではみんな同じ
    - 頭の中をさらけだして皆さんにお前はおかしいと叱ってもらいたい
    - もし今日の話に一理でもあるなら相互に理解が深まるはず


---

## 今日の話がうまくできるかどうか分からないので

- 考えはこの本の9章に書いてあります
    - 誰も9章まで辿り着いてないのではないか？
        - 青色の本でもオレンジ色の本でも同じ現象
    - お食事中の方すみません


![w:600](senden.png)

![bg right:30% 95%](robot_and_stats.jpg)


---

## 探索から制御問題へ


---

### 話の出発点: ロボットの計画問題（探索）

- 占有格子地図上にロボットの現在地から目的地まで線を引く
    - 次元が低く古典的な方法でも解ける
    - ダイクストラ、A*、RRT、...
        - いまだ現役
- 一方、移動ロボットや自動車を自律移動させることは難しい
    - 自己位置推定がずれる（今回は直接扱わず）、 障害物をうまく避けれない、・・・

$\qquad\qquad$![w:300](astar.gif)![w:300](rrt.gif)<span style="font-size:70%">図: [AtsushiSakai/PythonRobotics](https://github.com/AtsushiSakai/PythonRobotics)で作成</span>

---

### 一般的なアプローチ: 問題の分割

- 大域計画+諸問題の解決
    - 大域計画+障害物回避
- だいたいの場合、これで問題ない
    - 現場であれば問題が出たらまた潰せば良い
- 本当にこれで問題ない？
    - 理論上解決できないのか？
    - 根本から解決する方法はないのか？

<span style="color:red">$\Longrightarrow$問題を整理しましょう</span>

![bg right:35% 95%](avoidance.svg)


---

### 最適制御問題（計画からいきなり話が飛びますが・・・）

- 問題（とりあえず離散時関系で考えます）
    - いま、なにか制御したいものの<span style="color:red">状態</span>が$\boldsymbol{x}$です
        - （注意: $\boldsymbol{x}$には速度や時間も変数として入れられる）
    - $\boldsymbol{x}$を<span style="color:red">終端状態</span>の集合$\mathcal{X}_\text{f}$の任意の要素$\boldsymbol{x}_\text{f}$まで導きたい
    - 制御対象には$\boldsymbol{u} \in \mathcal{U}$という力をかけると次の時刻に状態$\boldsymbol{x}$が$\boldsymbol{x}'$に遷移します
        - $\boldsymbol{x}' = \boldsymbol{f}(\boldsymbol{x}, \boldsymbol{u})$（決定論的）
        - $\boldsymbol{x}' \sim p(\boldsymbol{x} |\boldsymbol{x}, \boldsymbol{u})$（確率的）
    - 「時間消費」、「エネルギー消費」、「危険性」などの評価があるとき、評価を最小にするためには$\mathcal{U}$からどのように$\boldsymbol{u}$を選んでいけばいいでしょうか？

![bg right:20% 95%](optimal_control_problem.svg)

---

### 大域計画（や他の多くの制御問題）は最適制御問題のサブセット

- <span style="color:red">今いるところは目的地じゃない$\rightarrow$目的地にいる状態に持っていきたい</span>
    - なるべく悪路を走らないで最短時間で
- 制御の問題はほとんどが最適制御問題のサブセット
    - 機械が振動している$\rightarrow$振動してない状態に戻したい
    - ライントレースのロボットがラインからずれた$\rightarrow$ライン中央に戻したい
    - 洗濯物が洗濯機の中に$\rightarrow$畳んで収納したい
        - <span style="font-size:80%">（※VLAは目的の状態を言葉から自律的に設定）</span>
- 前ページの定式化はマルコフ決定過程（MDP）でもあるけど最適制御と言います

<center style="color:red">制御対象の見かけ、計算リソース・時間の制約、解法で違う問題に見えるだけ</center>

---

### 最適制御問題の解の性質（どう解くかという話とは別）

- ある制御則の解（方策）$\boldsymbol{u} = \boldsymbol{\pi}(\boldsymbol{x})$に対し、ひとつひとつの状態から終端状態までのコストの期待値が計算できる
    - 実数を返す関数$V^\boldsymbol{\pi}(\boldsymbol{x})$: <span style="color:red">状態価値関数（値関数）</span>
- 大域計画の問題で考えると、別に難しい話ではない
    - ある場所$\boldsymbol{x}$にいるとき、行き方$\boldsymbol{\pi}(\boldsymbol{x})$が決まっていれば、目的地までの時間の期待値$V^\boldsymbol{\pi}(\boldsymbol{x})$が見積もれる

$\qquad\qquad\qquad$![w:400](search.svg)

---

### $V$の性質（状態遷移が決定論的な場合）

- $\boldsymbol{x}$の価値は遷移先$\boldsymbol{x}'$の価値に遷移したときのコスト$\ell$を足したもの
    - $V^{\boldsymbol{\pi}}(\boldsymbol{x}) = V^{\boldsymbol{\pi}}(\boldsymbol{x}')+\ell(\boldsymbol{x}, \boldsymbol{u}, \boldsymbol{x}')$
       - ここで$\boldsymbol{u} = \boldsymbol{\pi}(\boldsymbol{x})$、$\boldsymbol{x}' = \boldsymbol{f}(\boldsymbol{x}, \boldsymbol{u})$
    - 例
       - ゴールまで10歩のところから1歩歩いたら、次の状態はゴールまで9歩に
- 終端状態$\boldsymbol{x}_\text{f} \in \boldsymbol{X}_\text{f}$の扱い
    - それ以上状態遷移しない状態
    - $V^\boldsymbol{\pi}(\boldsymbol{x}_\text{f}) = 0$など、価値を固定しておく
- 他の状態の$V^\boldsymbol{\pi}$は$V^\boldsymbol{\pi}(\boldsymbol{x}_\text{f})$にしたがって決まる
    - <span style="color:red">$V^\boldsymbol{\pi}(\boldsymbol{x}_\text{f})$を底とするポテンシャル場に</span>


---


### 方策の改善と最適性

- もっと良い行き方$\boldsymbol{\pi}'(\boldsymbol{x})$があれば、時間の期待値が$V^{\boldsymbol{\pi}'}(\boldsymbol{x})$に短縮される
    - 方策を改善していくと収束
        - 収束した$V$: <span style="color:red">最適状態価値関数$V^*$</span>
            - $V^*(\boldsymbol{x}) = \min_\boldsymbol{u} \{ V^*(\boldsymbol{x}')+\ell(\boldsymbol{x}, \boldsymbol{u}, \boldsymbol{x}') \}$
            - まったく停留点のないポテンシャル関数に
        - $V^*$を与える方策: <span style="color:red">最適方策$\boldsymbol{\pi}^*$</span>
            - $\boldsymbol{\pi}^*(\boldsymbol{x}) = \arg\!\min_\boldsymbol{u} \{ V^*(\boldsymbol{x}')+\ell(\boldsymbol{x}, \boldsymbol{u}, \boldsymbol{x}') \}$


---

### $V$の性質（状態遷移が確率的な場合）

- $V^{\boldsymbol{\pi}}(\boldsymbol{x}) = \big\langle V^{\boldsymbol{\pi}}(\boldsymbol{x}')+\ell(\boldsymbol{x}, \boldsymbol{u}, \boldsymbol{x}')\big\rangle_{p(\boldsymbol{x}|\boldsymbol{u},\boldsymbol{x}')}$
    - $\langle f(x) \rangle_{p(x)}$: 分布$p$のときの$f$の期待値
- 最適なとき（ベルマン方程式）
    - $V^*(\boldsymbol{x}) = \min_\boldsymbol{u} \big\langle V^*(\boldsymbol{x}')+\ell(\boldsymbol{x}, \boldsymbol{u}, \boldsymbol{x}')\big\rangle_{p(\boldsymbol{x}|\boldsymbol{u},\boldsymbol{x}')}$
    - $\boldsymbol{\pi}^*(\boldsymbol{x}) = \arg\!\min_\boldsymbol{u} \big\langle V^*(\boldsymbol{x}')+\ell(\boldsymbol{x}, \boldsymbol{u}, \boldsymbol{x}')\big\rangle_{p(\boldsymbol{x}|\boldsymbol{u},\boldsymbol{x}')}$
- この定式化のおもしろいところ
    - $\boldsymbol{x}$や$\boldsymbol{u}$はベクトルで表記しているけどその必要はない
    - $p(\boldsymbol{x}|\boldsymbol{u},\boldsymbol{x}')$さえ厳密に決まっていればよい
        - 距離の定義が空間になくてもよい
    - むしろ解の$V^*$が距離のようなものの定義になっている

---

### 探索で得られる大域計画の解の性質

- 1本道の方策$\boldsymbol{\pi}$ができている
    - 右図の矢印
    - 最適である保証はない
    - ちょっと外れたところは基本無視
- $V$は方策を求めるついでに計算されている
    - 概算
    - 途中の計算で周辺の$V$も求められるが捨てられがち
- 状態遷移は確率的ではない

<center style="padding-top:2em">きっちり方策通りに行ければ問題はない、が</center>

![bg right:15% 95%](path_answer.svg)

---

### よく問題になること

- パスがチャタリング
- 経路上の障害物への対応
- 固定障害物への対応

---

### チャタリングの問題

- 経路を再計算したら変わった/また計算したら戻った
    - 再計算: 障害物の出現やもっと良いルートの探求
- 下手にプログラムすると真ん中のルートをたどって危険
    - 自動車だと中央分離帯で死ぬ（よくある事故）
    - なぜか自動車より遅い移動ロボットでもよく起こす
        - ROSのNavigation Stackのサンプル
- （小手先で解決できるかもしれないが）根本的な原因は？
    - 最適制御という面から考えると？

![bg right:20% 100%](chattering.svg)

---

### <span style="color:red">「事故もゴール（終端状態）」</span>という考え方の欠如

終端状態$\mathcal{X}_\text{f}$の設計に問題がある

- $V(\boldsymbol{x}_\text{f})$を大きく設定しておけば$\boldsymbol{\pi}$は
- 多くの制御手法でも「境界条件」と扱ってしまうが、それだと境界条件スレスレの制御が許容されてしまう/ペナルティーも恣意的に

![bg right:30% 100%](final_state.svg)

---

### 個人的な見解

- 「強化学習は安全性に疑問が・・・」という意見は本当か？
    - ほんとうに安全なエージェントはギリギリまでゆっくり障害物まで寄れる
    - 危険物に対するセンシングを「緊急停止」ではなく、適切な方策につなげられる
- むしろ「境界条件」がほんとに境界条件なのかあやしい


---

### 探索と制御（本発表の結論？）

- 各地点のコストの計算: 制御問題
- 最適制御問題
    - 状態空間と状態を考える

![bg right:30% 100%](optimal_control.svg)


---

### 探索が考えない問題

- ゴールに行くことは考えるが危険を避けることは制御レベルでは考えていない
- 環境の変化や不確かさ

---

### 探索で問題を解くと起こる問題

- 中央分離帯への衝突
    - 経路のチャタリング
    - メモしないこと、終端状態が正規のゴールしかないことで起こる
- 帯域計画と障害物回避の競合
    - $V$に停留点
    - 最大原理からの制御にも同じ側面

---

### 障害物との接触もゴール

---

中央分離帯ぶつかる問題集

価値関数だとぶつかるリスクも計算されている

どっちかを選ぶと引き込まれない

---

## LLMでの制御

- Robotics Transformer 2
   - ひとつずつ動きを出力
- とりあえず少しでも価値が上がる行動をしていれば最終的にタスクは達成できる

---
## その先の話

- 次元の呪いが克服されたら？
- 現在の計算機と性能のオーダーが違う計算機の登場

---

- コスト: 状態（位置）$\boldsymbol{x}$に対して$V(\boldsymbol{x})$

