---
marp: true
---

<!-- footer: 確率ロボティクス第1回 -->

# 確率ロボティクス第1回: イントロダクション

千葉工業大学 上田 隆一

<br />

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 「確率ロボティクス」とは 

- 分からないことをロボットで扱うための分野
- なぜそんなことが必要か？
    - ロボットが[工場](https://youtu.be/-QquWBX0sa0?t=83)から生活環境へ
        - 生活環境は分からないことだらけ
    - 工場のロボットもやることが難しくなっている<br />（[例: 唐揚げロボット](https://www.youtube.com/watch?v=Sfq81rVNyGo)）


<span style="color:red">不確か</span>な状況で活動しなければならない

---

## 不確かな状況での活動

- 例
    - 受験でどこを受けるか（将来の不確かさ）
    - 枕元のメガネを探す/なくしたものを探す（場所の不確かさ）
    - 誰かが言っていることを信じる/信じない
- 適切に行動できていると誰も自信を持って言えない
    - 特に失敗に代償が伴う場合は<span style="color:red">自信満々はかえって危険</span>$\rightarrow$ロボットも同じ

---

## もう少しだけ「不確かさ」を考察

- 五感で直接得られない、直接の体験で得られない情報
    - 隣の部屋、下の部屋で何が起きているかは分からない
    - 変な噂が流れてきたけど自分で直接確認できない
- 未来・過去の情報
    - 過去の記録が残ってない。未来は本質的に分からない。
- 正確に計測できない
    - 駅まで何メートル？$\rightarrow$誰も正確に言えない
- 前提知識がないと分からない
    - 小学生にいきなり微積分を教えても分からない 

<div style="color:red;text-align:center;font-size:200%">分からないことだらけ</div>

---

## 「分からない」$\neq$「行動できない」

- 動物や人間はいい加減に生きている
    - 動物は言葉を知らないけど困ってもいない
    - 駅まで何メートルか分からなくても駅には行ける
    - 説明書読まないで何かを組み立て始めたけどなんとかなった<br />（ならないこともある）
    - ブログに見当違いなことを書いていても儲かった
    - 全財産を使って起業してみた
- 実世界は「動いたもの勝ち」が結構多い

<div style="text-align:center">「人間のように賢くいい加減」に動くロボットは実現できないか</div>

---

## 不確かさ、自信のなさ、いい加減な行動をロボットの中に表現

- 動機: 4〜6ページのような状況に対応できる知能をロボットに持たせたい
    - 自信満々はとにかく危なっかしい
    - 損得勘定
- 方法: 数学を使うとなると「確率・統計」が道具となる
<br />　
<div style="text-align:center">ということで確率ロボティクスという分野が存在</div>

---

## Probabilistic ROBOTICS（確率ロボティクス）

- セバスチャン・スランらの教科書
    - 1995年頃から10年間に確立したロボット用の推論アルゴリズム（+カルマンフィルタ）を掲載
    - カルマンフィルタ、パーティクルフィルタ、FastSLAM、GraphSLAM、POMDP手法など
    - 確率ロボティクス分野
        - この教科書の範囲や周辺のアルゴリズムを研究する分野

<img width="50%" src="./figs/probrobo_books.jpeg" />

---

## 他の分野との関連性

- 制御に対する確率ロボティクス
    - いわゆる現代制御理論を1段階抽象化したもの
- 機械学習の手法群から見た確率ロボティクス
    - 機械学習の一部
    - 機械学習のブームの前にあったブーム
<br />　
- 補足: 機械学習ってなに？
    - 大雑把に言うと<span style="color:red">データから何か原因を推論</span>する方法
    - 人工ニューラルネットワークも含まれる


---

## 1.3 詳解確率ロボティクス<br />について

およびこの講義資料（スライド）について

<img width="30%" src="./figs/lnpr.jpeg" />

---

## 1.3.1 意図と体裁

- 書いた意図
    - 実際に動作するコードを交えて<br />確率ロボティクスを説明したい
        - 説明に実感が持てるように
        - コードを書いて試せるように<br />　
- Jupyter Notebookで<br />コードを書く
    - さっと書ける
    - コードの動作を視覚的に確認可能

<img width="42%" src="./figs/code_animation.png" />

とにかくコードを書いていただきたい

---

## 1.3.2 書籍の構成

- 3部構成
    - 「準備」、「自己位置推定とSLAM」、「行動決定」
- 2〜12章と付録Aが手法やアルゴリズムを説明した章
    - 興味に応じて次の図の順番で読める

<img width="70%" src="./figs/book_structure.png" />

---

## 1.3.3 書籍で使用するツール

- Pythonとnumpyなどのモジュール
    - よくわからなければ[Anaconda](https://www.anaconda.com/)で一式インストール<br />　
- [Jupyter Notebook](https://jupyter.org/)
    - インストール方法がOSやOSのバージョンでばらばらなので、<br />各自ネットで調査お願いします<br />　
- [GitHub](https://github.com/)
    - 用途
        - コードが読む
        - サンプルコードやこのスライドのリポジトリをfork（次ページ）
        - 自分の練習コードを置く
    -  アカウントを作ったほうがよい


---

## リポジトリ・ウェブサイト

- サンプルコード
    - 書籍掲載のコード: [ryuichiueda/LNPR_BOOK_CODES](https://github.com/ryuichiueda/LNPR_BOOK_CODES)
    - 完成したコードだけ残したもの: [ryuichiueda/LNPR](https://github.com/ryuichiueda/LNPR)<br />　
- 講義用スライド
    - リポジトリ: [ryuichiueda/LNPR_SLIDES](https://github.com/ryuichiueda/LNPR_SLIDES)
    - [目次](https://b.ueda.tech/?page=lnpr#%E8%AC%9B%E7%BE%A9%E7%94%A8%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%89)<br />　
- 訂正等の情報
    - https://b.ueda.tech/?page=lnpr