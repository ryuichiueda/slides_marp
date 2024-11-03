---
marp: true
---

<!-- footer: 千葉工業大学・松本工業高校連携授業 -->

# 移動ロボット入門

千葉工業大学 上田 隆一

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 自己紹介

- 上田隆一という名前です
- ロボットの研究者です
- 長くなるので[続きはウェブで](https://ja.wikipedia.org/wiki/上田隆一)

---

## 宣伝: 本買って

- 左から順に
    - Linuxの本
    - ロボットの本（今日話する内容）
    - ロボットで使う数学の本


<img width="20%" src="shellgei160.jpg" />  <img width="20%" src="lnpr.jpg" />  <img width="20%" src="robot_stats.png" />

---

## 今日のテーマ

- 知能ってなんだろ？

---

## ある問題

- 登場人物（人物じゃないけど）
    - うちの猫様
    - 美味しいおやつ
    - 通路・扉
        - 扉は猫には開けられません
- 猫様はおやつまでたどり着けるだろうか？

![bg right:44% 100%](problem.png)

---

## 答え: できない

- 扉の下に手を突っ込んでガリガリして諦める

<iframe width="560" height="315" src="https://www.youtube.com/embed/JmONWX1IWAk?si=kmL8VdtQict3X7Rn" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

## ここで質問

- 人間なら簡単なのに猫には難しいのはなんで？
- 逆に言うと、おやつのところまで行くには何が必要？
    - 人間は何をしている？
    - 脳にどんな機能が必要？

---

## 答えあわせ

- 俯瞰ができていない（疑惑）
    - 猫の頭の中に<span style="color:red">地図</span>はあるだろうか？
    - 自分の見ている風景が地図のどこに相当するか理解できてる？
- 計画ができていない（これは確実）
    - 頭の中でおやつの場所に行くまでの<span style="color:red">手順</span>が思い浮んでなさそう

![bg right:44% 100%](map.png)

---

## 問題を難しくすると<br />人間にも難しい

- 複雑な迷路だと人間にも大変
- 迷路でなく人生だと？
    - 俯瞰できないから遊んでしまう
    - 俯瞰している親や先生の言うことを素直に聞かない
- 注意
    - 息抜きは大事・聞きすぎも問題
    - 親も先生も完全には俯瞰できてない

![bg right:40% 90%](jinsei.png)

---

## 無駄話はこれまで

- 今の話をふまえると自分で考えるロボットをどう作ればよいでしょう？どうしたらロボットが自分で仕事ができるようになる？
    - 具体性もない（達成までの計画もない）のに「人を助けるロボットを作りたい」とか目を輝かせて夢みたいなことを無責任に言ってませんか？

<center style="font-size:200%">いっしょに考えていきましょう</center>

---

## ・・・といいつつ最後の無駄話

- 「地図」を頭に持っている動物がいる
    - 特定のところに行くと反応するようになる<span style="color:red">場所細胞</span>
       - 自分の見ているものや動きの感覚（主観）を「場所」という客観的なものに変換
- 他，移動や環境の形状に反応する脳細胞が存在



<p style="font-size:50%;padding:0px">出典: 場所細胞: Stuartlayton at English Wikipedia, CC BY-SA 3.0, via Wikimedia Commons, https://commons.wikimedia.org/wiki/File:Boundary_cell.png. 格子細胞: Khardcastle, CC BY-SA 4.0, via Wikimedia Commons, https://commons.wikimedia.org/wiki/File:Autocorrelation_image.jpg. ボーダー細胞: Tom Hartley, Colin Lever, Sarah Stewart, CC BY-SA, via Wikimedia Commons, https://commons.wikimedia.org/wiki/File:Boundary_cell.png</p>

![bg right:44% 100%](brain.png)

---

## 移動ロボットの話

- 本題です
- とりあえず次のような問題を考える
   - ロボットがどこかに置かれる
       - 右図のようなやつ
   - ゴールがどこかロボットに教えられる
   - ロボットが自分でゴールまで行く

![bg right:40% 100%](robot.png)

---

## 移動ロボットのハードウェア

![](robot_explain.png)

![bg right:34% 98%](rviz_lidar.png)

---

## 地図づくり

- ロボットを人間が操作してロボットのセンサでセンシング
- ずれないようにつなげていく
    （コンピュータに計算させて自動で）
        <iframe width="560" height="315" src="https://www.youtube.com/embed/b2kYQ11PUSI?si=3VsJxUuX92oP6DZT" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
- 右図: できた地図

![bg right:40% 98%](map1.png)

---

## 地図づくり（おまけ）

- 地図が歪んで作られて、修正される様子
    - [ずれている: 12:49ごろ](https://youtu.be/jS5_a9BW2zI?si=0JT8wF6IS8fOH1Yw&t=769)
    - [なおっている: 13:16ごろ](https://www.youtube.com/watch?v=jS5_a9BW2zI&t=796s)

<iframe width="560" height="315" src="https://www.youtube.com/embed/jS5_a9BW2zI?si=0JT8wF6IS8fOH1Yw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

## 大きな地図の例

- 千葉工大の学内の地図
    - 左: 2次元のLiDARで作成
    - 右: 3次元のLiDARで作成
        - いずれもロボットを手動で走らせて作成、200m×300m

<img width="50%" src="tsudanuma.png" /><img width="50%" src="3dmap.png" />

---

## 地図作成の方法

1. ロボットを円軌道で動かして、センサで見つけた星の位置を記録（左図）
（桃色の線分の先端）
    - <span style="color:red">実際にはロボットの起動は歪む</span>ので先端が揃わない
2. 星の位置が揃う軌道を推定$\rightarrow$改めて星の位置を記録（右図）
- 言葉で説明すると簡単だけど数学は難しい$\rightarrow$[大学の講義資料1](https://ryuichiueda.github.io/LNPR_SLIDES/chap9_1.html)、[大学の講義資料2](https://ryuichiueda.github.io/LNPR_SLIDES/chap9_2.html)
<center>　　　<img width="33%" src="draw_graphslam_log.png" /><img width="33%" src="graphslam.png" />
</center>


---

## 地図のなかでの位置計算

- よく使われる方法
    1. 地図のなかにロボットの分身をたくさんばらまく
    2. ロボットが動いたら分身も動かす
    3. センサのデータが入ったら、データと合わないところにいる分身を消す
        - 右図はLiDARではなくカメラで星を見たときの例
- 確率の計算となる（[講義資料](https://ryuichiueda.github.io/slides_marp/prob_robotics_2024/lesson7.html)）

![bg right:40% 98%](mcl_simple_resampling.gif)

