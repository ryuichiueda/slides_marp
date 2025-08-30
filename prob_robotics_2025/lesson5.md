---
marp: true
---

<!-- footer: 確率ロボティクス第5回 -->

# 確率ロボティクス第5回: 試行回数と信頼性

千葉工業大学 上田 隆一

<br />

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 今回の内容

- 実験結果の信頼性
- ベイズの定理
- 尤度


---

## 実験結果の信頼性


---

### 質問: この実験について議論してみましょう

- C君がロボットをある地点からある地点まで自動で走らせるソフトウェアを改良して、評価するために実験
- 実験内容: 改良前後のソフトウェアで5回ずつロボットを走行させる
- 実験結果: 
    - 改良前: 完走$\rightarrow$失敗$\rightarrow$失敗$\rightarrow$完走$\rightarrow$完走
    - 改良後: すべて完走
- C君の結論: 改良後のソフトウェアの方が優れている

<center style="padding-top:2em">ほんと？</center>

---

### 実験が足りないような気がするが・・・

- このあと試行を重ねると結果が逆転するかもしれない
    - 今回はこの問題について扱う
- 問題へのアプローチ: <span style="color:red">完走率の確率分布を推定する</span>
    - つまり確率（完走率）自体を確率変数として扱う
    - 背景となる考え: 無限回の試行をしないと完走率はそもそも不確か
    $\rightarrow$完走率は確率的

---

### 完走率の確率分布（の予想）

- 完走率（確率変数）を$t$とすると、$p(t)$はたぶん下図のようになる
    - (a) 試行前: 一様分布に（なにも情報がない）
    - (b) 何回か試行: 「完走回数/試行回数」のところにピークが来るが、まだ曖昧
    - (c) たくさん試行: 完走率がはっきりして、分布が鋭く

$\qquad\qquad\qquad$![w:700](./figs/prob_t.png)

<center>この分布で改良前後の結果を比較してみましょう
<br />（どうこの分布を計算するかはさておき）</center>

---

### 完走率の確率分布を考えると比較ができる

- たくさん試行すると(c)のように改良前後の完走率の分布が（ほぼ）重ならない
    - どちらが優れているか（ほぼ）分かる
- 試行が5回ずつ程度だと(b)のように分布が重なっていそう
    - 改良前後の完走率が逆転している可能性が無視できないほどある

$\qquad\qquad\qquad$![w:800](./figs/prob_t_compare.png)

<center>どうやって計算するの？</center>

---

### 事前分布・事後分布

- 完走率の分布を求めるため、次の分布を考える
    - $i$回目の試行前の分布: $p_{i-1}$
    - $i$回目の試行後の分布: $p_{i}$
- 次の関係: <span style="color:red">$p_i(t) = p_{i-1}(t | x_i)$</span>
    - $x_i$: $i$回目の試行の成否（1: 完走、0: 失敗）
    - $p_{i-1}$に$i$回目の成否を伝えると、分布が$p_i$に変化
    - <span style="color:red">条件付き確率の条件には「加わる情報」という側面がある</span>
- $p_{i-1}, p_i$のことを一般に「事前分布」、「事後分布」と呼ぶ

---

### 事後分布の導出の方法

- $p(t, x)$という分布を考える
    - $t, x$がなんなのかはとりあえず考えない
- 乗法定理で2通りの等式を作成
    - $p(t, x) = p(t|x)p(x)$
    - $p(t, x) = p(x|t)p(t)$
- 右辺どうしで等式を作り、$p(x)$で割る$\Longrightarrow p(t|x)= \dfrac{p(x|t)}{p(x)}\cdot p(t)$
    - $p(x|t), p(x)$がなんなのかは置いておくと完走率の分布$p(t)$に、試行の成否$x$の情報が入ったときに成立する等式になっている
- 添字をつける
    - $p_{i-1}(t|x_i)= \dfrac{p_{i-1}(x_i|t)}{p_{i-1}(x_i)}\cdot p_{i-1}(t)$

---

### さらに計算

- 教科書は離散化していますが、そのまま計算してみます
- $p_{i-1}(t|x_i)= \dfrac{p_{i-1}(x_i|t)}{p_{i-1}(x_i)}\cdot p_{i-1}(t)$の各要素を見ていきましょう
    - $p_{i-1}(x_i|t)$: 完走率が$t$のときに、$x_i$となる確率
        - $x_i$が完走: $t$
        - $x_i$が失敗: $1-t$
        - 上記をまとめると <span style="color:red">$p_{i-1}(x_i|t) = t^{x_i}(1-t)^{1-x_i}$</span>
    - $p_{i-1}(x_i) = \int_{t=0}^1 p_{i-1}(x_i,t)\text{d}t= \int_{t=0}^1 p_{i-1}(x_i|t)p_{i-1}(t)\text{d}t$
    $=\langle p_{i-1}(x_i|t) \rangle_{p_{i-1}(t)}=\langle t^{x_i}(1-t)^{1-x_i} \rangle_{p_{i-1}(t)}$
        - 意味はあとで
        - 上の式では定数扱い（$t$は積分で消える）

---

### 事後分布の導出（完了）

- したがって次が成立
    - $p_{i-1}(t|x_i)= \eta \ t^{x_i}(1-t)^{1-x_i} p_{i-1}(t)$
    - 意味: $x_i$が成功だと事前分布に$t$、失敗だと$t-1$をかけて
    正規化すると事後分布に
- これまでに$a$回成功、$b$回失敗したとすると
    - $p_{a+b}(t) = \eta \ t^a (1-t)^b p_0(t)$
- $p_0$が一様分布だとすると
    - <span style="color:red">$p(t) = \eta \ t^a (1-t)^b$</span> が、$a+b$回試行したあとの完走率の分布

---

### 事後分布の描画

- 改良前のソフトウェアの試行での分布の推移を描いてみましょう
    - 完走$\rightarrow$失敗$\rightarrow$失敗$\rightarrow$完走$\rightarrow$完走
    - $p(t) = \eta \ t^a (1-t)^b$
    * こうなる
    $\qquad\qquad\qquad$![w:700](./figs/post_prob.png)

---

### 分布の比較

- 5回ずつ試行が終わった時点での改良前後での分布の比較
    - これも余裕があれば描いてみましょう
    * こうなる
    $\qquad\qquad\qquad$![w:400](./figs/prob_comp.png)
        - 改良前の完走率のほうが高い可能性はある

---

### 改良前の完走率のほうが高い確率

- $p_\text{before}(t) = \eta t^3(1-t)^2 = 60 (t^5 -2 t^4 + t^3)$
- $p_\text{after}(t) = \eta t^5 = 6t^5$
- $\Pr\{ t_\text{before} > t_\text{after} \} = \int_{t_\text{before} > t_\text{after}} p(t_\text{before}, t_\text{after})\text{d}(t_\text{before},t_\text{after})$
$= \int_{t_\text{before} > t_\text{after}} p_\text{before}(t_\text{before})p_\text{after}(t_\text{after})\text{d}(t_\text{before}, t_\text{after})\quad \because t_\text{before} \perp\!\!\!\!\perp t_\text{after}$
$= \int_0^1 p(t_\text{after})\int_{t_\text{after}}^1 p(t_\text{before})\text{d}t_\text{before}\text{d}t_\text{after}$
$= \int_0^1 p_\text{after}(t)\int_{t}^1 p_\text{before}(t')\text{d}t'\text{d}t$
$= \int_0^1 6t^5 [ 10t'^6 -24t'^5 + 15t'^4 ]_{t'}^1 \text{d}t$
$= \int_0^1 6t^5 (1 - 10 t^6 + 24 t^5 - 15t^4)\text{d}t$
<span style="color:red">$= 1/11$</span>
$\Longrightarrow$ 9\%の確率で改良前のほうが完走率が高い

---

### もし改良後の試行で1回失敗があったら

- $p_\text{after}(t) = \eta t^4(1-t)$
- 同様に計算すると$\Pr\{ t_\text{before} > t_\text{after} \} = 0.28$
$\qquad\qquad\qquad$![w:400](./figs/prob_comp2.png)
- （試行回数は実験前に決めないといけないので）試行回数は全然足りない

---

### どれくらいの試行回数が必要か？

- 右のグラフ: $\Pr\{ t_\text{before} > t_\text{after} \}$の値
    - 改良が無意味な確率
    - 条件
        - 改良前の完走率: $t^*_\text{before} = 0.6$（固定）
        - 改良後の完走率: $t^*_\text{after} = 1.0, 0.9, 0.8, 0.7$のいずれか
- 無意味な確率が5\%以下になる試行回数
    - $t^*_\text{after} = 0.8$だと30回程度
    - $t^*_\text{after} = 0.7$だと100回以上
        - 100回で10\%は下回る
- （学科の学生の感覚よりも）かなり試行回数が必要

![bg right:30% 100%](./figs/false_prob_reduction.png)

