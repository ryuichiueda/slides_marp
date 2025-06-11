---
marp: true
---

<!-- footer: "機械学習（と統計）第14回" -->

# 機械学習

## 第14回: 強化学習

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- なにかを実行するということはどういうことかを考える

---

## 自分がやってることの根拠

- あります?
    - なんで朝飯食ったのか?
    - なんで朝飯はそれを食ったのか?
    - なんで大学来たのか
    - なんで講義受けているのか/講義の途中にゲームやるのか・やらないのか
- たぶん以下の理由でやってる
    - そうすると良いことがありそうだから
        - 良いこと: 楽しいなども含む
    - そうしないと悪いことがありそうだから

---

### 行動決定のモデル

- これも確率で考える
    - $a \sim \Pi(a | \boldsymbol{x})$
        - $a$: 機械のなんらかの出力や動物・人間の行動を漠然と記号化したもの
        - $\boldsymbol{x}$: 世の中の全変数を並べたベクトル（超膨大）
            - 実際には行動と独立でない変数だけしかいらない
        - <span style="color:red">$\Pi$: 方策</span>
            - 行動を決めているプログラムや脳の一部
- 例
    - $\boldsymbol{x}$: 昨夜酒飲んでて4時間しか寝てない
    - $\Pi($大学に行く$|\boldsymbol{x}) = 0.3$、$\Pi($そのまま布団で寝る$|\boldsymbol{x}) = 0.6$、
    $\Pi($とりあえず飲みなおす$|\boldsymbol{x}) = 0.1$

---

### 「良い方策」行動の定義

- 行動の結果に点数をつける$\rightarrow$良い点数をとれる$\Pi$が良い方策と考える
    - $J(\Pi) = \left\langle \left\langle \mathcal{L}(\boldsymbol{x},a,\boldsymbol{x}') \right\rangle_{p(\boldsymbol{x}' | a, \boldsymbol{x})} \right\rangle_{\Pi(a| \boldsymbol{x})}$
        - $\boldsymbol{x}'$: 行動$a$のあとの状態
        - $p(\boldsymbol{x}'|a, \boldsymbol{x})$: <span style="color:red">状態遷移分布</span>
            - $\boldsymbol{x}$で行動$a$をとったときの、次の状態$\boldsymbol{x}'$の分布
        - $\mathcal{L}$: 損失関数
            - $\boldsymbol{x}$で行動$a$をとって$\boldsymbol{x}'$に状態が変化したことに対する評価
            - いいことがあればマイナスに（マイナスの損失=報酬）
- 前のページの例で$\mathcal{L}$を考えてみましょう
    - 注意: 損失関数はあくまで主観で、ひとそれぞれ
        - 社会的にうまくいかないのは$\Pi$のせいではなく$\mathcal{L}$のせいと考えましょう

---

### 数値ひとつで行動が決められるのか？

- 頭の中はそうなってないかもしれないが、行動は同時にできず1つしか選べないし、なんらかの理由があって今その行動をしているので、なんらかの点数付けの上で行動していると解釈することは可能
- 「良くない」と社会的に思われている行動も、個人レベルではそのほうがいいという決定の上で行動していると解釈できる
    - 社会的ななにかより、個人的な苦痛の除去や快楽の追及、惰性で評価関数の点数が高くなる


---

## 多段の行動決定

- 行動決定の難しいところ: 「その先」がある
    - そのときは良くてもあとでひどい目に遭うなど、先のことを考えて行動したほうがいい場合が多い
        - 例: ギャンブルでお金を溶かして少しずつ横領を繰り返している等


---

### 多段の行動（状態遷移）のモデル

- このワンセットの繰り返し（$i=0,1,2,\dots$）
    - $a_{i+1} \sim \Pi(a | \boldsymbol{x}_i)$: 　　  　　状態$\boldsymbol{x}_i$から行動$a_{i+1}$を選択
    - $\boldsymbol{x}_{i+1} \sim p(\boldsymbol{x} |a_{i+1}, \boldsymbol{x}_i)$:　　状態が$\boldsymbol{x}_{i+1}$に遷移
    - $\ell_{i+1} = \mathcal{L}(\boldsymbol{x}_i, a_{i+1}, \boldsymbol{x}_{i+1})$: 損失を観測
- このような行動の履歴（エピソード）が残っていく
    - $\boldsymbol{x}_0, a_1, \boldsymbol{x}_1, \ell_1, a_2 \boldsymbol{x}_2, \ell_2, \dots, a_t, \boldsymbol{x}_t, \ell_t$
        - $t$: 現時刻

---

### 多段の行動の評価

今回は終わりのあるタスクを考えましょう

- 評価: $\sum_{i=1}^T \ell_i + V(\boldsymbol{x}_T)$
    - 最初の項: $\ell_1, \ell_2, \dots, \ell_T$の和（損失の積算）
    - 2番目の項: 最後の「ご褒美」
        - 最後の状態に対して与える（例:  「大学に合格した状態」など）
- この評価値は$\boldsymbol{x}_0$と方策$\Pi$で決まる
	- $J(\Pi| \boldsymbol{x}_0) = \left\{\sum_{i=1}^T \ell_i + V(\boldsymbol{x}_T)\right\}$の期待値


