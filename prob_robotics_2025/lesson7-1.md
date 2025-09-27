---
marp: true
---

<!-- footer: 確率ロボティクス第6回 -->

# 確率ロボティクス第7回: センシングと推定（その1）

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

- 情報のフィルタとしてのベイズの定理
- ベイズの定理を使ったセンサデータの処理

---

### 情報のフィルタとしてのベイズの定理

- 次のようなヒントから，どこのことを言っているのか考えてみましょう
	* (a) 日本では寒い場所です。
	* (b) 本州ではありません。
	* (c) 時計台があります。

---

### 質問

- 答えはいいとして、どう考えていきましたか？
    - 消去法？
    - 講師の意図は考えましたか？
    - 脳みそのどこを使いましたか？
- ロボットに実装するには？
    - たぶん今だとGPTだと思いますが、
    GPTも間接的に使っているある方法で

---

### 「消去法」について考える

- 実はベイズの定理で（アナログに）扱える
	- $p(\boldsymbol{x} | Z) = \eta L(\boldsymbol{x}| Z)p(\boldsymbol{x})$
	    - $\boldsymbol{x}$: 推定対象
	    - $Z$: ヒント
	    - $L$: <span style="color:red">尤度関数</span>
            - $L(\boldsymbol{x}|Z) = \Pr\{Z | \boldsymbol{x}\}$
