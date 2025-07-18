---
marp: true
---

<!-- footer: 確率ロボティクス第2回（その2） -->

# 確率ロボティクス第2回（その2）: <br />確率変数，確率質量関数と確率分布

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

- 確率変数
- 確率質量関数
- 確率分布
- 同時確率分布

---

## 確率変数

- 事象に数を対応させたもの
    - 例1: コインを投げて表が出る/裏が出るにそれぞれ$0$、$1$を割り当て
    - 例2（自然にそうなっている例）
        - サイコロを振って$n$の目が出る事象に$n$を割り当て
    - 例3（自然にそうなっている+連続的な変数の例）
        - ある人の身長が$x$[mm]であるという事象に$x$を割り当て
- 大抵は<span style="color:red">根元事象</span>に対して数値を対応
    - 根元事象: それ以上分けられない/分けない事象（サイコロの目など）
    - 確率変数の定義域は全ての根元事象を網羅している必要がある

---

### なんで確率変数を考えるのか

- 確率分布を考えるため（後述）
- その他計算のため（期待値など。次回。）
- 事象の扱いがめんどくさい
    - いちいち「$\circ\circ$という事象が起こった」と言うのがめんどくさい
    - 根元事象やそうでない事象が入り混じってめんどくさい

---

## 確率分布

- 確率変数を横軸にすると確率のグラフが描ける
    - 数直線上での確率の「分布」が分かる$\Longrightarrow$<span style="color:red">確率分布</span>
- 典型的な分布には名前
    - <span style="color:red">ベルヌーイ分布</span>（例: (a)）
        - 確率変数が2値だけ
    - <span style="color:red">一様分布</span>（例: (b)）
        - 確率変数のある範囲で確率が一定

![bg right:50% 90%](./figs/prob_dist.png)

---

## 確率質量関数

- 確率変数の値に対応する確率を返す関数
    - 表記: $P(x)$（厳密には$P$）
    - 要は確率分布のグラフの形を決める関数
    - <span style="color:red">これも確率分布と呼ばれる</span>
- $\Pr\{$ $\}$より定義がスッキリ
    - 変数がスカラー
- 補足
    - 「$P$」という記号は、本来は$f$だろうが
    $g$だろうが別になんでもよい
    - $x$が実数のときは密度の関数になるが
    今は考えない

![bg right:35% 90%](./figs/prob_dist.png)

---

{2.4.2}\SEVENjidori {確率質量関数}}{43}
{2.4.3}\SEVENjidori {確率分布}}{43}
{2.4.4}\SEVENjidori {確率分布と事象の関係}}{45}
{2.4.5}\SEVENjidori {同時確率質量関数，同時確率分布}}{46}
{2.5}\SEVENjidori {まとめと議論}}{47}

