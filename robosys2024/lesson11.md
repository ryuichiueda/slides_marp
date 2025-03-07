---
marp: true
---

<!-- footer: "ロボットシステム学第11回" -->

# ロボットシステム学

## 第11回: Pythonのクラスとオブジェクト

千葉工業大学 上田 隆一


<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 今日やること

- 作ってきたROS 2のパッケージのコードをクラスで整理
  1. オブジェクトとクラスの説明
  1. 実践
  1. まとめ

---

## 1. オブジェクトとクラス

---

### Pythonのオブジェクト

- ドットをつけると持っている変数や関数が使える
  - 例: 
    - `msg.data = n`
    - `pub.publish(msg)`
  - 注意: オブジェクトの持っている変数や関数（メソッド）は、まとめて「属性」（attribute）と呼ばれる　
- ひとつのオブジェクトで関連する属性をまとめて管理可能
  - ROS 2のノードと同様、機能をうまく切り分けていくと分かりやすいソフトウェアに

---

### 2. オブジェクトの作り方

- クラスを使ってオブジェクトを作る
  - 例: `node = Node("talker")`
    - 「`Node`」という<span style="color:red">クラス</span>にオブジェクトの定義が書いてあって、それにしたがって`node`オブジェクトができる
    - C言語の「`struct 構造体の名前 変数の名前;`」に相当
    - カッコの中の文字列`"talker"`は、オブジェクトの初期化のときに渡す引数　
  - 遺言
    - うまくクラスを使えるようになるには豊富な経験が必要
    - 人のコードを使うときに、どういう属性のまとめ方をしているか観察を

---

## 3. クラスの作成

- `talker.py`をクラスを使った記述に変更してみましょう

---

### クラスの作成と初期化（その1）

- やること（その1）
  - 1. `Talker`というクラスを作成
  - 2. `Talker`にパブリッシャーと変数を属性として実装

```python
  1 import rclpy
  2 from rclpy.node import Node
  3 from std_msgs.msg import Int16
  4
  5 ### ヘッダの下にTalkerというクラスを作成 ###
  6 class Talker(Node):     #Nodeというクラスの機能を受け継いだクラスになる
  7     def __init__(self):            #オブジェクトができたときに呼ばれる
  8         super().__init__("takler") #Nodeのオブジェクトとしての初期化
  9         self.pub = self.create_publisher(Int16, "countup", 10)
 10         self.create_timer(0.5, self.cb)
 11         self.n = 0
            # ↑ selfはオブジェクト自身のこと
            # ↑ オブジェクトにひとつパブリッシャと変数をもたせる。
（次ページに続く）
```

---

### クラスの作成と初期化（その2）

- やること（その2）
  - 3. コールバック関数もTalkerのメソッドに
  - 4. mainでTalkerのオブジェクトを作成
- 書き換えたら動作確認（テスト）を

```python
 14     def cb(self):         #コールバックのメソッド
 15         msg = Int16()
 16         msg.data = self.n #属性には必ずselfをつける
 17         self.pub.publish(msg)
 18         self.n += 1
 19
 20
 21 def main():
 22     rclpy.init()
 23     node = Talker() #Talkerのオブジェクトを作成
 24     rclpy.spin(node)  #↑あとは__init__が呼ばれてすべてが動き出す
```

---

## 課題

- `listener.py`もクラスを使って書いてみましょう

---

## 3. まとめ

- Pythonのクラスを作成
  - クラスの中にパブリッシャの機能を整理して実装
- 今後は「構造」に注目してプログラミングを！
