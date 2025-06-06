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
