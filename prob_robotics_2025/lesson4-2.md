---
marp: true
---

<!-- footer: 確率ロボティクス第4回（その2） -->

# 確率ロボティクス第4回: 連続値と多変量（その2）

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

- ガウス分布
- 多変量ガウス分布

--- 

## ガウス分布

--- 

### 前半のおさらい

- 連続的な変数に対して確率密度関数を導入
    - 確率変数が離散でも連続でも分布が表現可能に
- 次に考えること: 分布が数式で表せないか？
    - 右図のように取得したデータだけで分布を作るのは無理がある
    - 考え方
        - データがなにかの法則にしたがって発生する
        - その法則は数式で表せるかもしれない
        $\rightarrow$<span style="color:red">実際に典型的な数式が存在</span>

![bg right:25% 95%](./figs/theta_hist.png)

--- 

### ガウス分布の導入

- 式: $p(x) = \dfrac{1}{\sqrt{2\pi \sigma^2 }} \exp\left\{ -\dfrac{(x-\mu)^2}{2\sigma^2} \right\}$
    - $\mu$: 平均値
    - $\sigma^2$: 分散
        - 右図の例: $(\mu, \sigma^2) = (5, 1)$
- 典型的な数式のなかで最も代表的なもの
    - $x$がこまかくばらつく原因が多い場合にこういう形に（<span style="color:red">中心極限定理</span>）

センサ値や前半にやったロボットの移動距離、向きの誤差は、大きなばらつきの原因がないとガウス分布に従う

![bg right:35% 95%](./figs/gauss.png)

--- 

### なんで典型的で代表的になるか？

- なにか値$x$を計測（センサ値としましょう）
- センサ値は多種多様な誤差要因でばらつく
    - 気温、湿度、振動、放射線、・・・
    - 誤差要因別の誤差$\varepsilon_{1:n}$を考える
        - 原因が違うので互いに独立と仮定
- 誤差のない計測値$x^*$を仮定すると
    - $x = x^* + \sum_{i=1}^n \varepsilon_{i}$
- $\varepsilon_{1:n}$の各値がすべて正になったり、すべて負になったりする確率は低い
<span style="color:red">$\rightarrow \sum_{i=1}^n \varepsilon_{i}$の値は$0$に近いほど高頻度</span>

![bg right:35% 95%](./figs/gauss.png)
