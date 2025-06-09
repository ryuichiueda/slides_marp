---
marp: true
---

<!-- footer: 確率ロボティクス第1回 -->

# 確率ロボティクス第1回（その1）: <br />イントロダクション

千葉工業大学 上田 隆一

<br />

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

- 今回の内容
    - イントロダクション
    - 講義の進め方

---

## イントロダクション

---

### この講義

- 「確率ロボティクス」
    - 確率・統計をロボットに導入して賢くしようという分野
    - ロボットが工場から人間の生活空間に入る上で必要となった
- なんで確率・統計なのか？
    - 運動の面からの理由: 生活空間の複雑さに従来の制御が対応できない
    - 知能の面からの理由: 生活空間の複雑さをある意味<span style="color:red">「いい加減」</span>に扱うために必要となる

---

### 運動の面からの理由: 制御と確率

- いわゆる現代制御
    - 状態方程式、観測方程式に基づいて機械やプラントの状態推定や制御
        - 状態方程式: $\boldsymbol{x}_t = \boldsymbol{f}(\boldsymbol{x}_{t-1}, \boldsymbol{u}_t) + \boldsymbol{\varepsilon}$
            - 制御対象に$\boldsymbol{u}_t$という制御指令を出すと状態$\boldsymbol{x}_{t-1}$が状態$\boldsymbol{x}_t$に変化
            - ただし<span style="color:red">雑音</span>で、$\boldsymbol{\varepsilon}$だけ$\boldsymbol{x}_t$がずれる
        - 観測（出力）方程式: $\boldsymbol{z}_t = \boldsymbol{h}_t (\boldsymbol{x}) + \boldsymbol{\varepsilon}'$
            - 時刻$t$の状態が$\boldsymbol{x}$だと、$\boldsymbol{z}_t$が観測される
            - ただし<span style="color:red">雑音</span>で、$\boldsymbol{\varepsilon}'$だけ$\boldsymbol{z}_t$がずれる
    - 雑音は確率でモデル化されるので<span style="color:red">実は確率を扱っている</span>


---

### 状態方程式・観測方程式で扱われる確率

- 雑音のばらつきの想定は、大抵の場合<span style="color:red">正規分布（ガウス分布）</span>
    - ある大きさのばらつきを想定した上で安定で効率の良い制御方法を考える
- このアイデアの限界
    - 雑音がもっと一般化すると、状態/観測方程式で扱いにくい
        - 「ロボットが段差に引っかかって90度向きがずれた（状態がワープ）」
        - 「人がセンサを遮った（ばらつきと呼ぶには大きすぎる誤差）」

<center style="color:red">⇒⇒⇒新しい道具（数式）が必要</center>


---

### 知能の面からの理由: 人間並の認識・判断能力をロボットに持たせたい

- 突然ですが質問: なぜ事故が起きるかもしれない乗り物に乗るのか？
    - 飛行機、自動車、ジェットコースター
    - ロボットも人間並になると考えないといけない問題
* 真面目な答え
    - 生活のため（じゃあジェットコースターは？）
    - ◯◯だから安全
    - ◯◯だから私は乗らない
* 不真面目な答え
    * <span style="color:red">みんな乗ってるから</span>
    * しらねー（はやくこのくだらない講義から開放してほしい）
    * うるせー（この講義終わったらどこに行こう？）

---

### もう1つ質問

- 猫ってなんで猫ってみんな呼んでるの？そもそも猫ってなに？
    - 今のコンピュータやロボットは画像から猫を見つけられる
- 真面目な答え
    - 猫という言葉は眠った子という言葉が・・・
    - 猫はネコ科の動物で・・・
* 不真面目な答え
    * みんな猫って呼んでるから
    * 犬でもたぬきでも牛でも馬でもないから
* <span style="color:red">$\Rightarrow$実は最近のコンピュータ/ロボットは不真面目な方の方式</span>


---

### 従来、多くの研究者が考えていたこと

- 「正しい情報をたくさん与えると賢いコンピュータが作れて、それをロボットに搭載すれば正しく動くはず」
    - 正しい情報から理屈をこね回して正解の認識や動作ができるはず
        - キーワード: エキスパートシステム、述語論理、第五世代コンピュータ
- いかにも頭よさそうだけどほんまか？
    - 「哺乳類で脚が4本で・・・」という理屈だけで猫が認識できる？

![bg right:26% 100%](./figs/cat.png)

---

### 不真面目な答えこそ知能の鍵

- 理詰めで考えすぎると・・・
    - エネルギーや時間がかかる（無限にかかるかも）
    - 人とコミュニケーションが成立しなくなる
    - 「分からないけどとりあえず動いてみよう」ができない
- 「みんな乗ってるから」
    - これができるから飛行機のことを仕組みから勉強しなくてもよい
    - <span style="font-size:50%">憲法が保証しているから勉強しなくても生きていける</span>
- 「猫は猫」
    - みんな犬と区別つけてるし、猫と呼ぶから猫
       - 他の国では別の呼び方だし、下手すると区別してないかも

---

### 不真面目さを扱う良い道具: 確率・統計

- 確率・統計: 原因は一旦横に置いて、出てきたデータの法則性を扱う数学
    - 飛行機の事故「率」: 仕組みが分からなくても統計はとれる
        - 新たに情報を得て、統計からの予測を修正するとき$\rightarrow$確率を使用
        - 結果から原因を考えることができる
    - 「みんなそれを猫と言っている」も統計
        - <span style="color:red">人工ニューラルネットワークが学習してきたのはコレ</span>

統計さえとれればロボットが物理学者である必要はないかもしれないし、現に物理学者でない我々は日常生活ができているし、仕事をしている

---

### 最近の人工ニューラルネットワークの話題

- Transformerによる翻訳やGPT（Generative Pre-trained Transformer）
    - 冒頭/文の途中で、次に出力するのがふさわしい単語を選んで出力
        - 「ふさわしい単語」: 人からの質問、翻訳前の文、自身の出力したこれまでの文を考慮して、各単語が次にくる<span style="color:red">確率が最も高い単語</span>
- 拡散モデル（Stable Diffusionなど）
    - <span style="color:red">ある確率分布にしたがう雑音</span>がのった画像から雑音除去する方法を学習
    $\rightarrow$ノイズだけの画像を勝手に解釈して画像を生成

<center>単に統計的な法則を学習するだけでなく、確率的な構造・問題設定により進化</center>

---

### つまり

- 運動・知能双方で確率・統計の考え方が大変重要

---

## 講義で使う教科書

- 上田: 「ロボットの確率・統計」, コロナ社, 2024. 
    - 2024年度以前の「詳解確率ロボティクス」から変更
- 理由
    - ~~本を買ってほしい~~
    - 20年を経てロボティクスがより発展している
        - 機械学習や人工ニューラルネットワーク、認知科学との関係性をおさえておく必要がある
    - 確率・統計を基礎から講義したい
        - 一般的な確率・統計の講義と要点が異なる
        - 「詳解確率ロボティクスが難しい」との声
            - 基礎をつければ独学できるように書いてある

![bg right:20% 80%](./figs/books.png)


--- 

### Probabilistic ROBOTICS（確率ロボティクス）

- セバスチャン・スランらの教科書
    - 1995年頃から10年間に確立したロボット用の推論アルゴリズムを掲載
    - カルマンフィルタ、パーティクルフィルタ、FastSLAM、GraphSLAM、POMDP手法など
    - 確率ロボティクス分野
        - この教科書の範囲や周辺のアルゴリズムを研究する分野

<img width="40%" src="./figs/probrobo_books.jpeg" />


---

### 各回の内容（その1/2）

- 第1回（今回）: イントロダクション/代表値
- 第2回: 確率と信頼性工学
- 第3回: 期待値とギャンブル
- 第4回: 連続値と多変量
- 第5回: ベイズの定理と実験
- 第6回: 動く確率分布とロボット
- 第7回: センシングとベイズ推定


---

### 各回の内容（その2/2）


---

### 点数について

- テスト: 60点
- 課題: 40点
    - 締め切りは年末あたりにしていますが、応相談

---

### リポジトリ・ウェブサイト

- 講義用スライド
    - リポジトリ: [ryuichiueda/slides_marp](https://github.com/ryuichiueda/slides_marp/tree/master/prob_robotics_2025)
        - [目次](https://github.com/ryuichiueda/slides_marp/tree/master/prob_robotics_2025/README.md)
- 詳解確率ロボティクス
    - 詳解確率ロボティクス掲載のコード: [ryuichiueda/LNPR_BOOK_CODES](https://github.com/ryuichiueda/LNPR_BOOK_CODES)
    - 完成したコードだけ残したもの: [ryuichiueda/LNPR](https://github.com/ryuichiueda/LNPR)<br />　
    - 書籍解説スライド: [ryuichiueda/LNPR_SLIDES](https://github.com/ryuichiueda/LNPR_SLIDES)<br />　
    - 訂正等の情報
        - https://ueda.tech/?page=lnpr

