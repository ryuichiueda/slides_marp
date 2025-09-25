---
marp: true
---

<!-- footer: "ロボットシステム学第3回" -->

# ロボットシステム学

## 第3回: Linux環境でのPythonプログラミングII

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

- 前半: Python入門
    - Pythonで引数を操作
    - if文
- 後半: 標準入出力の操作と理解

---

## 前半: <span style="text-transform:none">Python</span>入門

---

## <span style="text-transform:none">Python</span>での引数の処理

- 要点
    - システムのことを扱う<span style="color:red">sysモジュール</span>を読み込む
        - 他によく使うモジュールとしては<span style="color:red">math</span>など
    - 引数はリストになっている
- 例（`args`）
    ```python
    #!/usr/bin/python3
    import sys             #sysモジュールを読み込み
    
    print(sys.argv)        #sysの「下の」argvに引数が入るのでprintしてみる
    ```
- 実行（「`args`」という名前でコードを保存して実行）
    ```bash
    $ ./args 引数1 引数2 引数3
    ['./args', '引数1', '引数2', '引数3']    #端末に打った通りにリストに入る
    ```

---

## 引数を使ったコマンドの作成1

- 引数の数を足し合わせる`plus`というコマンドを作ってみましょう
    - とりあえず2つの引数を足す計算のコードを作る
    - 例（`plus_a`）
        ```python
        #!/usr/bin/python3
        import sys
        
        print( float(sys.argv[1]) + float(sys.argv[2]) )
        ```
        - <span style="color:red">`float`</span>: 文字列を浮動小数点数に変換 
    - 実行
        ```bash
        $ ./plus_a 1 2
        3.0
        ```

---

## 引数を使ったコマンドの作成2

- 今度は引数をすべて足すコマンドを作成
    - 例（`plus_b`）
        ```python
        #!/usr/bin/python3
        import sys
        
        x = 0.0                    #xを定義して初期化
        for n in sys.argv[1:]:     #スライスを使う
            x += float(n)          #+=で足し込む
        
        print(x)
        ```
        - 一気にコードを書かず、引数がちゃんと読み取れているか`print`で確認しながら書くこと
    - 実行
        ```bash
        $ ./plus_b 1 2 3 4 5 6 7 8 9 10
        55.0
        ```

---

## 引数を使ったコマンドの作成3

- Pythonの「リスト内包表記」を利用
    - 発展的な内容なのでPython初心者の人はやらないでよいです
    - 例（`plus_c`）
        ```python
        #!/usr/bin/python3
        import sys
        
        nums = [ float(e) for e in sys.argv[1:] ]   #引数を浮動小数点数に変換してリスト作成
        print(sum(nums))                            #リストの和を返すsum関数を利用
        ```
        - 実行例は省略

---

## if文を使う

- 次のように書く
    ```python
    if 条件1:   #条件1が成り立つと、下の処理が実行される。elif以下の処理はスキップ。
        処理    #処理はインデントのレベルをひとつ上げて記述
        ・・・
    elif 条件2: #条件1に合わない場合は条件2が調べられる。
        処理    #（elifのブロックは省略や複数の記述が可能）
        ・・・
    else:       #ifやelifの条件に合わない場合に下の処理が実行される。
        処理
        ・・・
    ```
- 補足
    - `elif`: else ifの略
    - 動かないときはインデントを確認しましょう
        - `IndentationError`というエラーが出る（ちゃんとログは読みましょう）

---

## 練習: if文を使い、次のコードを記述しましょう。
- コード（3種類書く）
    1. 引数の数について負の数をカウントしてprint
    1. 引数の数について負、非負の数をカウントしてprint
    1. 引数の数について負、ゼロ、正の数をカウントしてprint
- 条件の書き方は、この例題についてはC言語と同じ。
    - 数`x`に対して、`x < 0.0`、`x == 0.0`、`x > 0.0`、`x >= 0.0`などと記述

---

## 練習の解答

- 3番目のものだけ記述
    ```python
     1 #!/usr/bin/python3
     2 import sys
     3 
     4 minus, zero, plus = 0, 0, 0 #こんなふうにまとめることが可能
     5
     6 for n in sys.argv[1:]:
     7     x = float(n)
     8     if x < 0.0:　
     9         minus += 1 　　　
    10     elif x > 0.0:          　
    11         plus += 1
    12     else:
    13         zero += 1
    14   　
    15 print("負:", minus)
    16 print("０:", zero)
    17 print("正:", plus)
    ```

---

## 後半: 標準入出力

---

## コマンドの出力のファイルへの保存

- 端末への出力は<span style="color:red">「 > ファイル」</span>でファイルに保存可能
    ```python
    $ ./plus_c 1 2 3 4 5 6 7 8 9 10 > ans    #ansというファイルに出力を保存
    $ cat ans                                #ansの中身の確認
    55.0
    ```
    - （出力の）<span style="color:red">リダイレクト</span>と呼ばれる機能<br />　
- リダイレクト
    - シェルが機能を提供
    - コマンド（プログラム）は、とりあえず端末に字を出すようにしておけば、処理結果の保存先を気にしなくてよい
        - コマンドにおける端末に字を出す出口: <span style="color:red">標準出力</span>と呼ばれる
        - プログラムを書くときは、特に理由がなければ標準出力に結果を出す

---

## ファイルからの入力

- ファイルの中身は<span style="color:red">「 &lt; ファイル」</span>でコマンドに渡せる
    - 入力のリダイレクト
- Pythonでの受け取り方
    - <span style="color:red">`sys.stdin`</span>とfor文で<span style="color:red">標準入力</span>から行毎に受け取る（`read_stdin`）
    ```python
    1 #!/usr/bin/python3
    2    　
    3 import sys
    4 　
    5 for line in sys.stdin:　
    6     word = line.strip() #最後に改行文字が入っているのでstripメソッドで除去
    7     print(word + " を標準入力から読んだよ")
    ```

---

### 前ページのコードの実行結果

```bash
$ seq 5 > nums    #seq: 1から指定された数字まで出力
$ cat nums         #リダイレクトをつかってnumsというファイルを作成
1
2
	・・・
5
$ ./read_stdin < nums
1 を標準入力から読んだよ
2 を標準入力から読んだよ
3 を標準入力から読んだよ
4 を標準入力から読んだよ
5 を標準入力から読んだよ
```

---

## 標準入力からの数字の足し算

- コードの例（`plus_stdin`）
    ```python
    #!/usr/bin/python3
    import sys  
    
    ans = 0.0
    for line in sys.stdin:　
        ans += float(line)
    
    print(ans)
    ```
    - できる人はリスト内包表記を使ってみましょう
- 実行
    ```bash
    $ ./plus_stdin < nums
    55.0
    ```

---

## 標準入力（パイプ）からの数字の足し算

- 需要: `nums`の中を見てから`plus_stdin`を使いたい
    - 何かデータを処理する前にデータを`cat`する人は多い
        - 例
            ```bash
            $ cat nums
            1
            2
            ・・・
            $ cat nums    #上矢印ボタンを押すと、直前に打った文字列cat numsを呼び出せる
            $ cat nums | ./plus_stdin # numsに続けて | ./plus_stdinと入力
            25.0
            $ seq 10 | ./plus_stdin  #numsを作らなくても結局これでよい
            25.0
            ```
            - <span style="color:red">`|`</span>: <span style="color:red">パイプ</span>
                - 左のコマンドの標準出力と、右のコマンドの標準入力を接続

---

## パイプによるコマンドの連携

- 例: 横に並んだ数字を足す
    - 縦並びに変換してから`plus_stdin`に入力
        ```bash
        $ echo 1 2 3 4 5 > yoko_nums
        $ cat yoko_nums | tr ' ' '\n'  #trで空白を改行に
        1
        2
        3
        4
        5
        $ cat yoko_nums | tr ' ' '\n' | ./plus_stdin
        15.0
        ```
        - <span style="color:red">`tr`</span>: 文字の置換コマンド<br />　
- 特別な理由がない限りデータは標準入力から受付
    - 引数や特定のファイルからだと、このような連携ができない

---

## プログラマーにとってのパイプの利点

- コードがシンプルに
    - `plus_stdin`は横並びの数字や文字の混入に対応しなくてよい
        - 様々な入力に柔軟に対応<span style="color:red">しない</span>
    - 各コマンドのコードがシンプルに
    - 既存のコマンドで可能なことはプログラムしなくてよい<br />　
- <span style="color:red">実はROSも似たような考え方で作られている</span>
    - 入出力を厳格に
    - プログラムごとに機能を分ける
    - 既存のプログラムを再利用しやすく

---

## 標準エラー出力

- コマンドにはパイプやリダイレクトで渡したくない出力も存在
    - エラーの際のメッセージなど
    - ファイルにリダイレクトされるとエラーが読めない<br />　
- ちゃんとしたコマンドはエラーを<span style="color:red">標準エラー出力</span>に出す
    - 例: `plus_stdin`に文字を入力してみる
        ```bash
        $ echo あ | ./plus_stdin > ans
        Traceback (most recent call last):                   #エラーはansに入らず画面に出てくる
          File "./plus_stdin", line 6, in <module>
            ans += float(line)
        ValueError: could not convert string to float: 'あ\n' #余談: エラーはちゃんと読みましょう
        ```
        - 標準出力とは別の出口からエラーが出ていることが分かる
        - ファイルにリダイレクトする場合は「<span style="color:red">`2>`</span>」で


---

## まとめ

- 学んだこと
    - 引数と標準入力に関してPythonでプログラミング
        - 他の言語でも、ほぼ同じ
    - for文やリスト内包表記でリストを操作
    - if文の書き方
    - 標準入出力でコマンドを連携（ROSに通ずる考え方）<br />　
- 重要語句
    - モジュール、sysモジュール、float関数、リスト内包表記、if文、リダイレクト、標準出力、標準入力、`sys.stdin`、パイプ、標準エラー出力
- コマンドや記号
    - `>`、`<`、`2>`、`seq`、`|`、`tr`
