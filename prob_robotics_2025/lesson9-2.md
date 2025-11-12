---
marp: true
---

<!-- footer: 確率ロボティクス第9回 -->

# 確率ロボティクス第9回: 行動決定（その2）

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

- Q学習のおさらい
- ベルマン方程式

---

## Q学習のおさらい

- 「学習の原理」として紹介した式
- 最初に適当な$V$を設定
- $V^\Pi(\boldsymbol{x})$と$\big\langle \ell(\boldsymbol{x}, a, \boldsymbol{x}')  + V^\Pi(\boldsymbol{x}' )\big\rangle_{P(\boldsymbol{x}' | \boldsymbol{x}, a)}$を比較
- 後者のほうがよければ
    - $\Pi(\boldsymbol{x})$の行動を変える
    - $V^\Pi(\boldsymbol{x})\longleftarrow \big\langle \ell(\boldsymbol{x}, a, \boldsymbol{x}')  + V^\Pi(\boldsymbol{x}' )\big\rangle_{P(\boldsymbol{x}' | \boldsymbol{x}, a)}$
    - ※ただし、偶然良かっただけかもしれないので慎重に
