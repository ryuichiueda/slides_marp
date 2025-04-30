---
marp: true
---

<!-- footer: "機械学習（と統計）第11回" -->

# 機械学習

## 第11回: 人工ニューラルネットワークの基礎

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 人工ニューラルネットワークってなに？

---

## 人工ニューラルネットワークってなに？

- まずは問題
    - なんで犬とか猫とか我々は認識できるのか?
        - 脳がやっているということは知っている
        - 脳に神経があることも知っている
    - <span style="color:red">脳や神経は具体的にどういう構造なのか?</span>


![w:400](./figs/Retina-diagram.svg.png)<span style="font-size:40%">（https://commons.wikimedia.org/wiki/File:Retina-diagram.svg, by S. R. Y. Cajal and Chrkl, CC-BY-SA 3.0）</span>

![bg right:30% 100%](./figs/cat_and_dog.png)


---

### 神経細胞

- 信号を伝える細胞
- 信号を伝える仕組み
   1. 樹状突起に化学物質をある量受けると電圧が発生
   （<span style="color:red">発火</span>）
       - 視細胞のように他の刺激で発火するものも
   2. 電圧が軸索を伝って、その先のシナプスから化学物質を放出
   3. 他の細胞が発火

![bg right:50% 100%](./figs/neuron.png)


<center style="font-size:50%">（図: public domain）</center>

---

### （人工でない）ニューラルネットワーク

- 脳: 神経細胞が集まって回路を形成
    - <span style="color:red">計算をしている</span>（後述）
    - ニューラルネットワークというのはこれのこと
- 脊髄: 神経が背骨を伝わり体の隅々へ
    - もともと脳ではなくこちらが本体
    - 反射などの計算はここで
- 末端: 回路の先端が筋肉につながっていてスイッチに


<center style="font-size:50%">（右図：CC BY-NC-SA 4.0, 脳科学辞典から）</center>

![bg right:30% 100%](./figs/皮質局所神経回路_図1.png)
![bg right:40% 100%](./figs/皮質局所神経回路_図2.png)


