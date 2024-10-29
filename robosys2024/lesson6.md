---
marp: true
---

<!-- footer: "ロボットシステム学第6回" -->

# ロボットシステム学

## 第6回: ソフトウェアのテスト

千葉工業大学 上田 隆一


<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## おさらいと今日やること

- おさらい: これまで説明してきたシェルの役割
    - ユーザーから文字を受け取ってコマンドを実行する
    - コマンドを見つける（`PATH`）
- 今日やること: シェルの<span style="color:red">プログラミング言語としての側面</span>を学習
    - コマンドを関数のように組み合わせて制御
    - ファイルにコマンドを動かす手順（<span style="color:red">シェルスクリプト</span>）を書く
    - シェルスクリプトを使ってplus_stdinが正しいかどうかをテスト

---

## 1. シェルの変数

---

### 基本事項

- シェルは，`変数名=文字列`で，文字を記憶
    ```bash
    ### 例 ###
    $ X=我々は宇宙人だ   # 変数のセット
    ```
- `${変数名}`で値に置換
    ```bash
    ### 例 ###
    $ echo ${X}ぜ！      # 変数を値に
    我々は宇宙人だぜ！
    $ echo $X            # {}は省略できる（こともある）
    我々は宇宙人だ
    $ echo '$X' # 値にしないときはシングルクォートで囲う（``と混同注意）
    $X
    ```
    ```bash
    ### {} が省略できない例 ###
    $ echo ${X}Z
    我々は宇宙人だZ
    $ echo $XZ
                            #変数「XZ」と解釈されるのでなにも出力されない
    ```

---

### コマンドの出力を変数に

- `変数名=$(コマンド)`
 - 通常は標準出力に出るコマンドの出力を文字列として変数に格納
 - 例: `ls`の出力を変数`A`に　　　　　　　　　　　　　　
    ```bash
    $ A=$(ls)
    $ echo $A
    README.md plus_stdin  # 注意: 出力は各自異なります．
    ```


---

## 2. コマンドの終了ステータス

---

### コマンドによる正常終了・異常終了の伝達

- コマンドは人に対してだけでなく，シェルにエラーの有無を伝達
- 方法 
    - <span style="color:red">終了ステータス</span>と呼ばれる整数値で伝達
        - シェルは<span style="color:red">`?`</span>というパラメータにコマンドの終了ステータスを記録
     - 例: `ls`の出力
        ```bash
        $ ls /etc/passwd   # 存在するファイルをls
        /etc/passwd
        $ echo $?          # ?に$をつけると値に置き換わる
        0                  # ?の値はゼロ
        $ ls aaaaaaaa      # 存在しないファイルをls
        ls: 'aaaaaaaa' にアクセスできません: そのようなファイルやディレクトリはありません
        $ echo $?
        2                  # ゼロでない値が入る．
        ```

---

### `plus_stdin`の終了ステータス

- これまで書いてきた`plus_stdin`も終了ステータスをシェルに伝達
    - Pythonが裏でやっているので，任せておいて問題ない
    ```bash
    $ seq 3 | ./plus_stdin    # 正常な入力
    6
    $ echo $?
    0
    $ echo あ | ./plus_stdin  # ひらがなを入力してエラーを起こさせる
    （エラーの表示．省略．）
    $ echo $?
    1
    ```

<center>なんのために終了ステータスがあるか？→あとで説明</center>

---

## 3. テストコマンド

- 以下のいずれかで，文字列を比較可能　　　　　
     - その1: `test 比較したい文字列 = 比較したい文字列`
     - その2: `[ 比較したい文字列 = 比較したい文字列 ]`
     - その3: `[[ 比較したい文字列 = 比較したい文字列 ]]`
     - 例（その1〜3の違いには細かい話はありますが，　　ここでは「その2」だけ）
        ```bash
        $ a=山田
        $ [ "$a" = 上田 ]       # [ はコマンドなので，引数はくっつけないようにしましょう．
        $ echo $?               #終了ステータスで確認
        1
        $ [ "$a" = 山田 ]
        $ echo $?
        0
        ```

---

## 4. 簡単なシェルスクリプトの記述

- コマンドの起動手順をファイルに書いてみましょう
    - 我々がこれから書くのはBashのスクリプト
     （Bashはシェルなので，シェルスクリプトの一種）　
    - ここからはおそらく一気に覚えられないので見様見真似で書いて実行
    - 読めるようにはなってください

---

### シェルスクリプトを作ってみる


- テストコマンドの例をファイルに保存して実行してみましょう
 - 「`yamada.bash`」というファイルに，次のように記述
    ```bash
    #!/bin/bash
    　 
    a=山田
    [ "$a" = 上田 ]       
    echo $?               
    [ "$a" = 山田 ]
    echo $?
    ```
 - `chmod`してPythonのスクリプトと同様に実行
    ```bash
    $ chmod +x yamada.bash
    $ ./yamada.bash
    1
    0
    ```

---

## 5. シェルの関数

- 基本的な関数の書き方: 名前のうしろに`()`をつけて，`{}`の中に処理を記述
- 第`n`引数を`${n}`で受け取り
    - 例: `ng`という関数を作り、呼び出してみる（ファイル名は`test.bash`）
    ```bash
    #!/bin/bash
    　
    ng () {
            echo ${1}行目が違うよ  #$1はngの1番目の引数
    }
    　
    ng 123
    ```
    - 実行
    ```bash
    $ chmod +x ./test.bash
    $ ./ng.bash
    123行目が違うよ
    ```

--- 

### コマンドと関数の連携

- `[`が失敗したら`ng`を呼び出す
    - 例（ファイル名: `test.bash`）
    ```bash
    #!/bin/bash
    　
    ng () {
            echo ${1}行目が違うよ
            res=1                   #追加
    }
    　
    res=0
    a=山田
    [ "$a" = 上田 ] || ng "$LINENO"  # LINENOは，この行の行番号の入る変数
    [ "$a" = 山田 ] || ng "$LINENO"  # ngに第一引数として$LINENOを付与
    　
    exit $res     # このシェルスクリプトの終了ステータスを返して終了
    ```
    - `||`（OR記号）: 左側のコマンドが異常終了したら右側を実行

---

### 実行結果

```bash
$ ./test.bash
10行目が違うよ
$ echo $?
1
```

---

## 6. 初歩的なテスト

やっと本題

---

### ここで言うテストとは

- プログラムが意図通りに動作するかを<span style="color:red">別のプログラム（テストコード）を書いて</span>テストすること
- 次のようなテストコードを書いて実行
    1. テスト対象のコードに引数や標準入力からデータを入力
    2. 出力を記録
    3. 期待した出力と一致するか比較　

<center>面倒だと思いますか❓</center>

---

### テストがないと辛い

- 例: 「プログラムに機能をどんどん追加していったら，最初に書いた部分がうまく動かなくなった！」
    - <span style="color:red">→こまめにテストを実行すれば防止可能</span>
        - <span style="color:red">転ばぬ先の杖</span>

### リグレッションテスト
- 上記のようなテストを特に<span style="color:red">「リグレッションテスト（退行テスト）」</span>と言う．これからそれをやる．　

---

### こういう開発スタイルに早く移行しましょう

1. こまめにテスト
2. テストに通ったらGitにコミット
3. テストに失敗して，原因不明なら前回のコミットに退却
 - `git restore`
4. さらに細かくテスト

予告: 最初の課題ではこのような経緯の分かるリポジトリを各自提出してもらいます！（あとから慌てても無理．コピー不可能）

---

### コマンドに対するリグレッションテストの記述

- 準備
    1. `plus_stdin`を`plus`に改名しておく$\rightarrow$<span style="color:red">コミットを</span>
        - 注意: テストと無関係です．
    1. さきほどの`test.bash`をリポジトリ直下（`plus`と同じところ）に置いてコミットしてGitHubにpush
- 次のように`test.bash`を変更（次ページ）

---

```bash
 1 #!/bin/bash
 2
 3 ng () {
 4         echo ${1}行目が違うよ
 5         res=1
 6 }　
 7
 8 res=0    
 9　
10 out=$(seq 5 | ./plus)
11 [ "${out}" = 15 ] || ng "$LINENO"
12 　   　
13 exit $res 
```


- 動作確認
    ```bash
    ### 実行権限をお忘れなく ###
    $ ./test.bash 
    $ echo $?
    0
    ```

---

 - 15を14に変えて`echo $?`で`1`と出ることも確認$\rightarrow$<span style="color:red">コミットを</span>
 - なんで判定に終了ステータスを使うのかは次回判明

---

### さらなる改良


- 改良点
 - 人間にも成否が分かるように/テスト項目を追加可能に
- さきほど習得した関数を利用
 - 前回学んだ著作権やライセンスの設定も
    ```bash
    #!/bin/bash
    # SPDX-FileCopyrightText: 2022 Ryuichi Ueda
    # SPDX-License-Identifier: BSD-3-Clause
    　
    ng () {
            echo NG at Line $1
            res=1
    }
    　
    res=0
    　
    ### I/O TEST ###
    out=$(seq 5 | ./plus)
    [ "${out}" = 14 ] || ng ${LINENO}
    　
    [ "$res" = 0 ] && echo OK        # &&（AND記号）は左側が成功すると右側を実行
    exit $res
    ```

---

### 動作確認

- 失敗した行と終了ステータスを確認
    ```bash
    ./test.bash
    NG at Line 12
    $ echo $?
    1
    ```
 - 動作確認したらテストコマンドで比較する数を`15`に戻して動作確認
 - `OK`と出るか．終了ステータスは`0`か．
 - <span style="color:red">commit & push</span>

---

### シェルスクリプトの挙動の確認

- `-x`や`-v`でシェルスクリプトの動作を観察可能　　　
    ```bash
    #!/bin/bash -xv        <- シバンの後ろに-xvと書いて-xと-vをセット
    （以下略）
    ```
 - 動作確認
        ```bash
        $ ./test.bash 
        （略）
        res=0
        + res=0
       　 
        ### I/O TEST ###
        out=$(seq 5 | ./plus)
        ++ seq 5
        ++ ./plus
        + out=15
        [ "${out}" = 15 ] || ng ${LINENO}
        + '[' 15 = 15 ']'
       　 
        [ "$res" = 0 ] && echo OK
        + '[' 0 = 0 ']'
        + echo OK
        OK
        exit $res
        + exit 0
        ```


---

### テスト項目の追加

- 不正な入力に対する挙動もテストするとよい 　　　　　
 - 入力が正しいような出力をしていないか
 - 特定の終了ステータスを返しているかどうか
        ```bash
        #!/bin/bash -xv
        （略）
        ### I/O ###
        out=$(seq 5 | ./plus)
        [ "${out}" = 15 ] || ng ${LINENO}
          　 
        ### STRANGE INPUT ###
        out=$(echo あ | ./plus)
        [ "$?" = 1 ]      || ng ${LINENO}
        [ "${out}" = "" ] || ng ${LINENO}
          　 
        out=$(echo | ./plus) #空文字
        [ "$?" = 1 ]      || ng ${LINENO}
        [ "${out}" = "" ] || ng ${LINENO}
          　 
	[ "$res" = 0 ] && echo OK
        exit $res
        ```
 - 注意: 終了ステータスはコマンドを実行したらすぐ確認（変わってしまうので．）

---

## まとめ・後始末

- まとめ
 - シェルスクリプトを記述
 - 終了ステータス，変数，テストコマンド，関数
 - リグレッションテストの記述
 - プログラムと一緒に少しずつ書いていく
 - ROSのように標準入出力を使わないものについては第11回で　
- 後始末
 - `yamada.bash`は削除してpush
