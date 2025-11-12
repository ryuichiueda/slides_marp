---
marp: true
---

<!-- footer: 確率ロボティクス第9回 -->

# 確率ロボティクス第9回: 行動決定（その1）

千葉工業大学 上田 隆一

<br />

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 今日やること

- なにかをやるということはどういうことかを考える
- Q学習

---

## 自分がやってることの根拠

- あります?
    - なんで朝飯食ったのか?
    - なんで朝飯はそれを食ったのか?
    - なんで大学来たのか
    - なんで講義受けているのか
- たぶん以下の理由でやってる
    - そうすると良いことがありそうだから
        - 良いこと: 楽しいなども含む
    - そうしないと悪いことがありそうだから

---

### 行動決定のモデル

- 「なにか行動をするといい/悪いことがある」は行動を決めるときの手がかり
    - ロボットの行動を計算するときにも必要
        - 行動の結果の良し悪しを数値化して評価しないと行動が選べない
- いいこと/悪いことの数値化（2種類）
    - その時その時に良いこと/悪いことがある
        - 食べている/勉強している/遊ぶ
    - 行動の結果、よい/悪い状態になる
        - 満腹になる/賢くなる/無意味に歳をとる

---

### 記号化しましょう

- 状態$\boldsymbol{x}$: 行動に関係する変数を並べたベクトル
- 行動$a$: 状態を変えるなにか
- 損失$\ell$: 行動$a$の結果被る（行動は疲れる）
    - 学習の場合には$\ell$に$-1$をかけた報酬$r$で考えることが多い
- 終端状態$\boldsymbol{x}_\text{f}$とその価値$V(\boldsymbol{x}_\text{f})$
    - 一連の行動が終わった状態と、その状態の良さ

![w:600](./figs/reward_model.png)

---

### 「よい行動」

- 状態$\boldsymbol{x}$、行動$a$、損失$\ell$、終端状態の価値$V(\boldsymbol{x}_\text{f})$でどう表現するか？
- こたえ: 一連の行動がおわったときの$\ell$と$V(\boldsymbol{x}_\text{f})$の和
    - たとえばある状態$\boldsymbol{x}_\text{f}$に行きつくのに10回行動が必要だった$\Rightarrow$
    $\ell_1 + \ell_2 + \dots + \ell_{10} + V(\boldsymbol{x}_\text{f})$
- あくまで主観
    - ひとそれぞれ。何をやってもいつか死ぬので難しい話
    - 問題: これからの人生をモデル化してみましょう！
        - 趣味に生きるか、スキルをつけるか、人のために生きるか、タバコを吸うか、酒を飲むか、あるいはその全部か・・・

![w:500](./figs/reward_sum.png)

----

### 補足

- 数値ひとつで行動が決められるのか？
    - 行動は同時にできず1つしか選べない
        - 選んだ行動がなんらかの点数付けの上で一番良いから選ばれていると解釈することは可能
- 行動決定問題の面白さ
    - 「損して得とれ」という構造がよく出現する
        - その場で一番良い行動が将来的に一番良い行動とはならないので難しい
            - 依存症は一種の「バグ」
- 行動決定問題を解く鍵
    - 「今は損な行動でも、将来的には良い」という確証をどう計算で得るか？
       - なにかの将来的な<span style="color:red">期待値</span>を計算することに

---

## 強化学習

- 評価がよりよくなる行動をロボット（エージェント）に選ばせるように学習させる仕組み
    - エージェントには感情がないが、ステップ数が多く、
    行動の損失が大きい課題を解くのは難しい（計算が難しい）
- 学習するもの: <span style="color:red">$\Pi$: 方策</span>
    - ある状態$\boldsymbol{x}$でどの行動$a$を選ぶかを決める関数
    - $a = \Pi(\boldsymbol{x})$
- 損失関数
    - $J(\Pi | \boldsymbol{x}) = \left\langle \ell_1 + \ell_2 + \dots + \ell_i + V(\boldsymbol{x}_\text{f}) \right\rangle_{\Pi}$
        - $\boldsymbol{x}$: 最初の状態

![bg right:30% 100%](./figs/reward_model.png)

---

### 簡単な例題で考えましょう

- タイルワールド（右図）の<span style="color:red">Q学習</span>を扱う
- こんな問題
    - ロボットは右か左どちらかを選択してサイコロを振って出たマスだけ移動
        - 端より先には行けず、そこに停留
    - ゴール or 穴のマスに止まれば終了
- 記号などの定義: 右図
- ある場所から出発したときに、損失の期待値を最小化したい（どうしましょう？）

![bg right:40% 100%](./figs/q_env.png)

---

### 一番よい方策（最適方策）

- おそらくこれ
（とにかく穴をさけたほうがよい）
    - $\boldsymbol{x}^{(1)}$以外では「左」を選択
    - $\boldsymbol{x}^{(1)}$で「右」を選択
- 最適方策:
    - $\Pi(\boldsymbol{x}^{(i)}) = \begin{cases}\text{右}\quad(i=1)\\\text{左}\quad(i=2,3,\dots,6)\end{cases}$
- これをどうやってコンピュータに解かせましょう？

![bg right:40% 100%](./figs/q_env.png)


---

### 問題の性質

- ある状態に対し、そこからスタートしたときの損失関数の期待値が計算可能
    - 損失関数: $J(\Pi | \boldsymbol{x}) = \left\langle \sum_{j=1}^{i} r_j + V(\boldsymbol{x}_\text{f}) \right\rangle_{\Pi}$
    - 右図: 計算したもの
- $\boldsymbol{x}$は最初の状態でなくてもよい
    - 別の状態からスタートしても、ある時点で$\boldsymbol{x}$にいたら、以後の$J$の期待値は右図の計算した値
    - <span style="color:red">過去のことはこれからの行動選択には無関係</span>
- <span style="color:red">損失関数の期待値を状態の関数にできる</span>
    - 終端状態の価値を拡張して
    関数$V^\Pi(\boldsymbol{x})$（<span style="color:red">状態価値関数</span>）を考える


![bg right:30% 100%](./figs/value.png)

---

### 状態価値関数の性質

- 方策にしたがって行動をとったときに次の関係
    - $V^\Pi(\boldsymbol{x}) = \big\langle \ell(\boldsymbol{x}, a, \boldsymbol{x}')  + V^\Pi(\boldsymbol{x}' )\big\rangle_{P(\boldsymbol{x}' | \boldsymbol{x}, a)}$
        - $\boldsymbol{x}$: ある状態
        - $a$: 行動
        - $\boldsymbol{x}'$: 行動をとったあとの状態
        （複数の候補あり）
    - $\ell(\boldsymbol{x}, a, \boldsymbol{x}')$: 行動に対する損失の関数
- 右の例: 左端の2つの状態が分かりやすい
    - 問題: 左から3つめの状態について計算を
- もし別の行動をとって右辺のほうが左辺よりよかったら$\Rightarrow$<span style="color:red">もっと良い方策がある</span>


![bg right:30% 100%](./figs/value.png)


---

### 方策の改善

こういう方法が考えられる

- 最初に適当な$V$を設定
- $V^\Pi(\boldsymbol{x})$と$\big\langle \ell(\boldsymbol{x}, a, \boldsymbol{x}')  + V^\Pi(\boldsymbol{x}' )\big\rangle_{P(\boldsymbol{x}' | \boldsymbol{x}, a)}$を比較
- 後者のほうがよければ
    - $\Pi(\boldsymbol{x})$の行動を変える
    - $V^\Pi(\boldsymbol{x})\longleftarrow \big\langle \ell(\boldsymbol{x}, a, \boldsymbol{x}')  + V^\Pi(\boldsymbol{x}' )\big\rangle_{P(\boldsymbol{x}' | \boldsymbol{x}, a)}$
    - ※ただし、偶然良かっただけかもしれないので慎重に

<center style="color:red">これが強化学習の原理</center>

![bg right:30% 100%](./figs/value.png)

---

## Q学習

- 先ほどの原理でロボットを
学習させてみましょう
- ただし、<span style="color:red">行動価値関数</span>というものを考える
    - $Q(\boldsymbol{x}, a)$: $\boldsymbol{x}$で$a$をとるときの
    状態$\boldsymbol{x}$の価値
    - $V(\boldsymbol{x}) = \max_a Q(\boldsymbol{x}, a)$
- まず、$Q$を初期化（右図）

![bg right:45% 100%](./figs/q_init.png)

---

### 値の更新

- ロボットに適当に動いてもらって$Q$の値を更新
- 更新式
	- もとの$Q$の値を少しだけ変更
	- $Q(\boldsymbol{x}, a)\longleftarrow\alpha q(\boldsymbol{x}, a) + (1-\alpha) Q(\boldsymbol{x}, a)$
        - $\alpha$: 学習率（右図の例だと$\alpha=0.1$）
	    - $q(\boldsymbol{x}, a) = \ell + V(\boldsymbol{x}')$
	        - $V(\boldsymbol{x}') = \min_{a'} Q(\boldsymbol{x}', a')$


![bg right:35% 90%](./figs/q_update.png)


---

### 方策の工夫

- 方策が完全にランダムだとゴールに着かず
学習が進まない
- そのときに一番良い行動しかとらないと
別の可能性が探れない
    - 例: 右図のようになってしまうと$\boldsymbol{x}^{(3)}, \boldsymbol{x}^{(6)}$で左が選ばれなくなり学習が進まない
    - こういうことは日常でないだろうか？
- $\Rightarrow$方策を次のように確率的に
（$\varepsilon$-グリーディー方策）
    - 確率$(1-\varepsilon)$で$Q$値が一番良い行動をとる
    - 確率$\varepsilon$でランダムに行動選択

![bg right:35% 100%](./figs/q_ng.png)

---

### 学習の実行例

- 100試行までには最適方策が得られている
- $V$、$Q$はなかなか収束しない

![bg right:35% 100%](./figs/q_result.png)

---

### 少し大きな問題

- 右のロボットが、水たまりを避けてゴールに
行くように学習させたい
    - いまのところ水たまりに一直線
- 下図左: 方策（ロボットが左を向いている時のもの）
- 下図右: 状態価値関数（同上）

<img width="45%" src="./figs/init_policy.png" />
<img width="45%" src="./figs/policy_evaluation_end_sweeps.png" />

![bg right:30% 100%](./figs/puddle_world4.gif)


---

### ロボットに行動させる

- $\varepsilon$-グリーディ方策で
- 水たまりに入ると損失を与える
- Q学習の式で行動価値関数を書き換え
	- $Q(\boldsymbol{x}, a)\longleftarrow\alpha \{\ell + \min_{a'} Q(\boldsymbol{x}', a') \}$
    $\qquad\qquad\qquad + (1-\alpha) Q(\boldsymbol{x}, a)$

![bg right:30% 100%](./figs/agent_on_q_learning.gif)


---

### 学習の進行: 行動の変化

- 時間はかかるがだんだん水たまりを避けるように

![w:600](./figs/11.1.jpg)

---

### 学習の進行: 状態価値関数の変化

- ゴールまでの損失が減っていく

![w:600](./figs/11.2.jpg)

---

### もっと複雑な問題

- DQN (Deep Q-Network) [[Mnih 2013]](https://arxiv.org/abs/1312.5602)
    - ゲームをするエージェント（=コンピュータの中の体のないロボット）
    を実現して騒ぎに
- [ゲームの学習方法](https://huggingface.co/blog/deep-rl-dqn)
    - 画像（全体の）をCNNに通して特徴で分類して状態に
    - $Q$の表現にも人工ニューラルネットワークを使用


---

## まとめ

- 行動の評価方法（損失・価値）について
    - そのときの行動に対する損失と、最終的な状態に与えられる価値がある
        - 補足: 最終的な状態の価値の代わりにその直前の行動に対して与える場合もあるが等価
- 強化学習、その中のQ学習を見てきた
    - 行動と状態、損失の観察（=経験）から状態の「価値」を計算


