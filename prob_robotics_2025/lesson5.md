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

## 質問: この実験について議論してみましょう

- C君がロボットをある地点からある地点まで自動で走らせるソフトウェアを改良して、評価するために実験
- 実験内容: 改良前後のソフトウェアで5回ずつロボットを走行させる
- 実験結果: 
    - 改良前: 完走$\rightarrow$失敗$\rightarrow$失敗$\rightarrow$完走$\rightarrow$完走
    - 改良後: すべて完走

<center style="padding-top:2em">改良前後どっちが優れている？その前に実験は妥当？</center>
