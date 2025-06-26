---
marp: true
---

<!-- footer: 確率ロボティクス第2回（その1） -->

# 確率ロボティクス第2回: 確率と信頼性工学（その1）

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

- 確率の基礎+信頼性工学
    - 確率を意識しながらロボットを運用する話

---

### こんな経験はありませんか？

- ロボットのなにかの大会に出た$\rightarrow$ロボットが始動しなくてリタイアになった
* <span style="color:red">$\uparrow$「運が悪かった」で済ませていませんか？</span>
* <span style="color:red">$\uparrow$ほんとに運が悪かったんですか？</span>
* <span style="color:red">$\uparrow$リタイアした原因だけつぶして満足していませんか？</span>
* <span style="color:red">$\uparrow$なんどもこんなことを繰り返していませんか？</span>
* そういう人はおそらくロボットへの知識ではなく<span style="color:red">信頼性工学</span>の知識が足りません
    - 勉強していきましょう
    - 信頼性工学は確率を駆使するので、確率の基礎もおさえていきましょう


---

### 確率の定義

- 数学的に厳密なものは難しいので、とりあえずこう考える
    - 何か事象が起こるかどうかを予測するときに、
    同じ状況で統計をとって、起こる割合を確率に
    - 例: ロボットの部品Aが、これまで100回ロボットを起動して
    90回だけ正常に立ち上がった$\Rightarrow$確率$90/100 = 0.9$と考える

<center>素朴すぎるのですが当面これで議論</center>

---

### 確率の表記

- 記号での表記: 事象Xの起こる確率を$\Pr\{$X$\}$と表記
（事象Aはなんでもよい）
    - 前ページの例: $\Pr\{$Aが正しく立ち上がる$\}=0.9$
- あとから出てくる$P(x), P(\boldsymbol{x})$との違い
    - この表記の場合は$x$や$\boldsymbol{x}$はそれぞれスカラやベクトル
        - $P$は定義域が数直線やベクトルの空間で厳密に決まった関数
    - 例: サイコロ
        - $P(1) = 1/6$と書けても$P($ 5以外の数 $)$とは書けない
- $\Pr\{$X$\}$のXは事象なので、なんでも書ける
    - 例: $\Pr\{$ 5以外の数 $\}$
    - 事象の集合に対する関数になっている


---

### 様々なタイプの事象1

- 根元事象
    - それ以上分けられない（と決めた）事象
        - サイコロの例: 1〜6の出目
        - 根元事象でない事象の例: サイコロの出目が偶数 
- 全事象
    - すべての事象を含んだ事象
        - サイコロの例: 1〜6のどれかが出る

---

### 様々なタイプの事象2

- 空事象
    - 起こらない事象で$\varnothing$あるいは$\phi$と表記
    - 集合論の空集合に相当（集合論で確率を定義するときに出てくる）
    - $\Pr\{\varnothing\} = 0$
- 余事象
    - 全事象からある事象Aを除いた事象
    - 事象Aに対して余事象はA$^c$と表記

---

{2.}\mokuSEVENjidori {確率 ---機械が動くという奇跡}}{22}
{2.1}\SEVENjidori {掛け算で動く可能性が減っていくロボット}}{23}
{2.1.1}\SEVENjidori {確率の導入}}{23}
{\hbox to2zw{{\rm (}\hfill 1\hfill {\rm )}}}確率の導入}{24}
{\hbox to2zw{{\rm (}\hfill 2\hfill {\rm )}}}確率の記号表現と事象}{24}
{2.1.2}\SEVENjidori {ロボットの起動率の計算}}{25}
{2.1.3}\SEVENjidori {乗法定理と独立}}{27}
{\hbox to2zw{{\rm (}\hfill 1\hfill {\rm )}}}乗法定理}{28}
{\hbox to2zw{{\rm (}\hfill 2\hfill {\rm )}}}独立}{29}
{2.2}\SEVENjidori {冗長化されたシステム}}{30}
{2.2.1}\SEVENjidori {加法定理}}{31}
{2.2.2}\SEVENjidori {冗長化されたA$_1$の起動率}}{32}
{\hbox to2zw{{\rm (}\hfill 1\hfill {\rm )}}}排反な事象への分解}{33}
{\hbox to2zw{{\rm (}\hfill 2\hfill {\rm )}}}加法定理を使った式の整理}{33}
{\hbox to2zw{{\rm (}\hfill 3\hfill {\rm )}}}余事象を使った導出}{34}
{\hbox to2zw{{\rm (}\hfill 4\hfill {\rm )}}}冗長化の効果}{34}
{2.3}\SEVENjidori {部品が互いに影響を与える場合}}{35}
{2.3.1}\SEVENjidori {乗法定理による計算}}{36}
{2.3.2}\SEVENjidori {隠れた条件と加法定理}}{38}
{\hbox to2zw{{\rm (}\hfill 1\hfill {\rm )}}}今まで考えてこなかった条件を式に加える}{38}
{\hbox to2zw{{\rm (}\hfill 2\hfill {\rm )}}}例}{40}
{2.4}\SEVENjidori {確率変数，確率質量関数と確率分布}}{42}
{2.4.1}\SEVENjidori {確率変数}}{42}
{2.4.2}\SEVENjidori {確率質量関数}}{43}
{2.4.3}\SEVENjidori {確率分布}}{43}
{2.4.4}\SEVENjidori {確率分布と事象の関係}}{45}
{2.4.5}\SEVENjidori {同時確率質量関数，同時確率分布}}{46}
{2.5}\SEVENjidori {まとめと議論}}{47}
{2.5.1}\SEVENjidori {なぜ自動車や飛行機が大丈夫なのかを不真面目に考える}}{47}
{2.5.2}\SEVENjidori {信頼性向上の方法に関する考察}}{49}
{2.5.3}\SEVENjidori {冗長化に関する考察}}{51}
