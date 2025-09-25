---
marp: true
---

<!-- footer: "ロボットシステム学第4回" -->

# ロボットシステム学

## 第4回: GitとGitHub

千葉工業大学 上田 隆一



<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 今日やること

- GitとGitHubを使う
- Pythonの文法の勉強を少し　
- 目次
    1. 準備
    2. GitHubへのコードの保存
    3. ブランチ
    4. コンフリクトへの対処
    5. その他リポジトリの操作
    6. まとめ


---

## 1. 準備

---

## Git

- 版管理（バージョン管理）システム
    - ファイルの変更履歴を管理するためのシステム
    - コードや文章を書くときは必須と言っても過言ではない　
- Linus Torvalds氏（Linuxを作り出した人）が作成
    - Linuxの共同開発のため

---

## Gitのインストール

- やること
    1. （`git`と打って「ない」と言われたら）インストール
        - `sudo apt install git`
    2. ユーザの設定
        ```bash
        ####自身の名前とe-mail アドレスを記録しておく###
        $ git config --global user.name "Ryuichi Ueda"
        $ git config --global user.email "ueda@hogehoge.com"
        ####エディタも登録しておくとよい###
        $ git config --global core.editor vim
        ####確認###
        $ cat .gitconfig
        [user]
        name = Ryuichi Ueda
        email = ueda@hogehoge.com
        [core]
        editor = vim
        ```

---

## GitHub

- Gitを利用したサービス
    - 「リポジトリ」のホスティングと公開，コミュニケーション
        - <span style="color:red">リポジトリ</span>: あるソフトウェアに関するファイルの集まり
    - 公開しないリポジトリも作成可能　
- 利用方法
    - ウェブサイト([https://github.co.jp/ ](https://github.co.jp/))
    - コマンドライン
        - `git`コマンド
        - `gh`コマンド（本講義では扱わず）　
- 注意: 他にも同様のサービスは存在
    - GitLab, Bitbucketなど

---

## GitHubでのアカウント作成

注意: 文言等はよく変更されるので，基本的にサイトの英語を読んで手続きを

1. トップページで"Sign up"か"GitHubに登録する"を押す
2. ユーザ名，email アドレス，パスワードを決めて"Create account"を押す
    - ユーザ名は恥ずかしくないものを！
3. 画面指示に従って手続き
    - プランを選ぶときに"Free"が選択されているのを確認$\rightarrow$"Finish sign up"
4. 登録したメールアドレスに確認メールが届く$\rightarrow$指示にしたがう
5. 鍵の登録（次ページ）
6. （必要ならば）ファイアウォール対策

---

## 鍵の設定（鍵の作成）

- 手元のPCとGitHubとの通信を暗号化するために，<span style="color:red">公開鍵</span>をGitHubに登録
    - 手元のPCには<span style="color:red">秘密鍵</span>を持っておく
        - 秘密鍵は文字通り秘密にして他人に見せたり触れたりさせない　
- 鍵の作り方
    ```bash
    $ ssh-keygen
    （いろいろ聞かれるけどすべてEnterで大丈夫）
    $ ls ~/.ssh/                   #確認
    id_rsa      id_rsa.pub         #この2つのファイルがあれば大丈夫
    ```
    - `id_rsa.pub`の方が公開鍵
- 参考: 暗号については過去の資料にちょっと書いてある
    - https://lab.ueda.tech/?page=robosys_2016_12

---

## 鍵の設定（GitHubでの作業）

- 右上のユーザのアイコンを押す$\rightarrow$Settings$\rightarrow$SSH and GPG keys$\rightarrow$New SSH key
    - titleはなんでもいいので鍵の名前を入れる
        - 例: 「WSL」とか「Ubuntu Note」とか
    - Keyに`id_rsa.pub`の中身を貼り付け
        - エディタや端末で開いてマウス等でコピーして貼り付け
<img width="70%" src="./figs/ssh_keys.png" />

---

## ファイアウォール回避の設定

今年からやらなくてよくなりました！！

- ホーム下の`.ssh/config`というファイルに次のように記述
    ```bash
    $ cat ~/.ssh/config
    ・・・
    
    Host github.com
          Hostname ssh.github.com
          User git
          Port 443
          IdentityFile ~/.ssh/id_rsa
    
    ・・・
    ```
    - SSHでデフォルトの22番ポートではなくHTTPSの443番ポートを使う設定
        - 参考: https://docs.github.com/ja/authentication/troubleshooting-ssh/using-ssh-over-the-https-port


---

## 2. GitHubへのコードの保存

- やること
    - これまで講義で作ってきたコードをGitHubにアップロード
    - コードを消しちゃった人は前回の`plus_stdin`を作りましょう
        - `plus_stdin`
            ```python
            #!/usr/bin/python3
            import sys
               
            ans = 0.0
            for line in sys.stdin:
                ans += float(line)
                 
            print(ans)
            ```

---

## リポジトリの作成

- GitHubのサイトでの操作
  - 右上のアカウントのアイコンを押して"Your repositories"を押す
  - 右にある"New"を押す
  - 必要事項を記入
    - 名前: robosys202x（そのままrobosys202xと入れないように！）
    - Description: 説明を適当に
    - Publicのままに
    - "Add a README file"にチェック
    - ライセンス: None（別の回で追加します）
  - "Create repository"ボタンを押す

$\Longrightarrow$`README.md`がひとつ存在したリポジトリができる

---

## リポジトリを手元にコピー

- リポジトリの画面の"Code"をクリック
- "SSH"を選択してURLをコピー
  - クリップボードのアイコンをクリックするとコピーできる
- リポジトリをコピーしたいディレクトリで次の操作
    - この操作を<span style="color:red">クローン</span>と言う
        ```bash
        $ git clone <さっきクリップボードにコピーした文字列をペースト>
        Cloning into 'robosys202x'...
        （略）
        Receiving objects: 100% (3/3), done.
        $ cd robosys202x/
        $ ls -a
        .  ..  .git  README.md
        ```
    - <span style="color:red">注意: </span>鍵の設定が失敗しているとエラー

---

## リポジトリにコードを追加1: git add

- プログラム`plus_stdin`を一つ置く
    ```bash
    $ ls
    README.md  plus_stdin
    ```
- <span style="color:red">`git add`</span>で記録の対象として選択
    - <span style="color:red">ステージングエリア</span>というところに記録される
        ```bash
        $ git add plus_stdin
        $ git status             #ステージングエリアの確認
        ブランチ main
        Your branch is up to date with 'origin/main'.
        
        コミット予定の変更点:
          (use "git restore --staged <file>..." to unstage)
        	new file:   plus_stdin
        ```

---

## リポジトリにコードを追加2: git commit

- <span style="color:red">`git commit`</span>でステージングエリアの情報をリポジトリに反映
    - この時点で，手元のリポジトリに`plus_stdin`の記録が残る
    - `git commit`で作った1つの記録を<span style="color:red">コミット</span>と呼ぶ
        ```bash
        $ git commit -m "Add a command" #git commit -m "何をしたか短く"
        [main fa8aab8] Add a command
         1 file changed, 8 insertions(+)
         create mode 100755 plus_stdin
        $ git log -n 1                 #最新のコミット1件を表示
        commit fa8aab8a2ade8cd33823f488fbb1bbec6d981260 (HEAD -> main)
        Author: Ryuichi Ueda <ryuichiueda@gmail.com>
        Date:   Tue Dec 7 16:58:54 2021 +0900

            Add a command
        ```

---

## GitHubへの反映

- 手元のリポジトリをGitHubのリポジトリへ転送
    - <span style="color:red">プッシュ</span>と呼ぶ
        - 手元（<span style="color:red">ローカルリポジトリ</span>からGitHub（<span style="color:red">リモートリポジトリ</span>）へ
    - コマンドは<span style="color:red">`git push`</span> 
        ```bash
        $ git push   #git push origin mainと打たないといけない場合もある
        Enumerating objects: 4, done.
        Counting objects: 100% (4/4), done.
        Delta compression using up to 16 threads
        Compressing objects: 100% (3/3), done.
        Writing objects: 100% (3/3), 373 bytes | 373.00 KiB/s, done.
        Total 3 (delta 0), reused 0 (delta 0)
        To github.com:ryuichiueda/robosys202x.git
           68d342f..fa8aab8  main -> main
        ```
    - プッシュしたらGitHub側で反映されたことを確認のこと

---

## 3. ブランチ

---

## GitHubを利用した開発

- GitHubにコードをアップした時点で様々な利点
    - 自分のコードを紛失する可能性が極めて低く
    - 混乱せずに様々な環境で開発可能に
    - 自分の力を見せることが可能に
        - たとえ学科内だと平凡でも，世の中的にはコードが書けるだけで少数派　
- 面倒なこと: 少々責任が伴う
    - ライセンス等の整備（また別の回で）
    - <span style="color:red">使えないものを使えると言って置かない</span>
        - 他の人が使うかもしれない

---

## 動くものを残しながらの開発

- よくあるケース
    - 改良しようと結構手を加えたらコードが動かなくなった　
- どうする？
    - そのままGitHubにpushすると他の人がコードを使えなくなる
    - GitHubにpushしないで放置すると作業の記録が残せない

<span style="color:red">$\Rightarrow$ブランチを分ける</span>

---

## ブランチ

- リポジトリの内容を枝分かれして開発を進める
  - ブランチ = 枝
- 今のところブランチは「main」だけ
  ```bash
  $ git branch
  - main          #ブランチはmainだけ．「-」は選択状態を表現
  ```
  - GitHubはmainブランチを優先して表示するので，ここでの雑な開発は避けたい
- 開発用ブランチを作りましょう
  ```bash
  $ git switch -c dev     #git checkout -b devでも可
  Switched to a new branch 'dev'
  $ git branch
  - dev               #devブランチができて，devが選択状態に
    main
  ```

---

## devブランチでの開発（その1）

ついでにPythonの文法の勉強もします

- `plus_stdin`について，整数の文字列は整数に変換するよう改良
    - <span style="color:red">例外処理</span>をしてみましょう
        - 失敗しそうな処理を<span style="color:red">`try`</span>で囲む
        - 下に<span style="color:red">`except`</span>のブロックを作って例外処理
            ```python
            #!/usr/bin/python3
            import sys
                       　　 
            ans = 0　 #もともと0.0だったのを0に変更
            for line in sys.stdin:
                try: 
                    ans += int(line)   #intは文字列を整数に（失敗すると例外発生）
                except:　
                    ans += float(line)
                       　 
            print(ans)
            ```

---

## devブランチでの開発（その2）

- 検証とコミット（とプッシュ）　　　　　　　　　　　　　
    ```bash
    ###動作確認###
    $ seq 5 | ./plus_stdin 
    15                        #整数として処理されていることを確認
    $ seq 5 | sed 's/$/.1/' | ./plus_stdin 
    15.5                      #小数も計算できることを確認
    ###バグがないことを確認したらコミット###
    $ git add -A              #-Aで変更を全部ステージングできる
    $ git status              #ブランチと変更されたファイルを確認
    ブランチ dev
    コミット予定の変更点:
      (use "git restore --staged <file>..." to unstage)
    	modified:   plus_stdin
    $ git commit -m "Support integer calculation"
    [dev f02a202] Support integer calculation
     1 file changed, 5 insertions(+), 2 deletions(-)
    ###不要だけどGitHubにもプッシュしてみましょう###
    $ git push --set-upstream origin dev   #origin: GitHubにあるリポジトリのこと
	（略）
     - [new branch]      dev -> dev
    Branch 'dev' set up to track remote branch 'dev' from 'origin'.
    ```

---

## （寄り道）ブランチの観察

- `git log --graph`で表示してみましょう
    ```
    $ git log --graph  #下の出力は一部省略
    - commit f02a20237590c9e4650f100928c6c2f969c111c3 (HEAD -> dev, origin/dev)
    |     Support integer calculation
    |
    - commit fa8aab8a2ade8cd33823f488fbb1bbec6d981260 (origin/main, origin/HEAD, main)
    |     Add a command
    |
    - commit 68d342fbb7a9b65e402d0b6f5a7763e56f248937
          Initial commit
    ```
    - ポイント
        - 各コミットには`f02a2023...`のような識別記号$\rightarrow$<span style="color:red">コミットハッシュ値</span>
        - ()の中に情報
            - `HEAD`: いまのディレクトリの内容
            - `origin/<ブランチ名>`: GitHubのリポジトリのブランチ
        - 右端の線：コミット同士の関係を表現

---

## devブランチでの開発（その3）

- mainへの<span style="color:red">マージ</span>とGitHubへのプッシュ
    - まずmainブランチに戻って変更内容の確認
        ```bash
        $ git switch main        # git checkout mainでも可
        Switched to branch 'main'
        Your branch is up to date with 'origin/main'.
        $ git diff main dev
        （略．mainとdevのコードの違いが表示される）
        ```
    - mainにdevの中身をマージ（併合）してGitHubに反映
        ```bash
        $ git merge dev #下の出力には省略あり
         1 file changed, 5 insertions(+), 2 deletions(-)
        $ cat plus_stdin 
        （略．try...exceptの入ったコードが表示される）
        $ git push
        To github.com:ryuichiueda/robosys202x.git
           fa8aab8..f02a202  main -> main
        ```
<center>安全にmainブランチを更新できた</center>

---

## 4. コンフリクト

- Gitを使っていると，コミット同士が矛盾することがある
    - マージできない　

そういう状況を作ってみましょう．

---

## コンフリクトを起こす（準備）

- ローカルリポジトリを別に作成
    ```bash
    $ mkdir ~/tmp/
    $ cd ~/tmp/
    $ git clone git@（略） #略の部分は自分で考えましょう
    ```
    - ローカルリポジトリが2個に　　　　　　　　　　　　　　　　　　
        - 片方をA，もう片方をBと呼びましょう
            - どっちがどっちでもよい


---

## コンフリクトを起こす（その1）

- リポジトリAで変更してpush
    - 数字の処理部分を関数に（ついでなのでPythonの関数も勉強します）
        ```python
        #!/usr/bin/python3
        import sys
        　   #スライドの関係で1行だけど、本来、関数の前後は2行空白をあける
        def tonum(s):   #def 関数の名前(引数)で関数を定義
            try:
                return int(s)
            except:
                return float(s)
        　 
        ans = 0
        for line in sys.stdin:
                ans += tonum(line)
        　 
        print(ans)
        ```
        - <span style="color:red">忘れずpushを</span>


---

## コンフリクトを起こす（その2）

- リポジトリBで別の変更
    - リポジトリAの存在を忘れて作業したという想定
        ```python
       （略）
        for line in sys.stdin:
            line = line.rstrip() #for文の下にこの行を挿入
       （以下略）
        ```
    - コミットしてpushするとエラー
        ```bash
        $ git push 
        To github.com:ryuichiueda/robosys202x
         ! [rejected]        main -> main (non-fast-forward)
        error: failed to push some refs to 'git@github.com:ryuichiueda/robosys202x'
        hint: Updates were rejected because the tip of your current branch is behind
        hint: its remote counterpart. Integrate the remote changes (e.g.
        hint: 'git pull ...') before pushing again.
        hint: See the 'Note about fast-forwards' in 'git push --help' for details.
        ```

<center>異なる内容はpushして混ぜることができない</center>

---

## コンフリクトの解消（その1）

- リポジトリBで`git pull`
    ```bash
    $ git pull #出力には省略あり
    CONFLICT (content): Merge conflict in plus_stdin
    Automatic merge failed; fix conflicts and then commit the result.
    ```
    - 「`CONFLICT`」と出るが`pull`は完了　　　　　　　　　　　
        - `plus_stdin`の内容（A, B両方の更新が反映されるが矛盾も生じる）
            ```python
            （略）
            <<<<<<< HEAD                #Bの内容
            ans = 0
            for line in sys.stdin:
                line = line.rstrip()
            =======                     #Aの内容
            
            def tonum(s):
            >>>>>>> a4936f439aed64b3234d533c6e7a3abc7b5d744d
            （以下略）
            ```


---

## コンフリクトの解消（その2）

- コードを手で修正してコミット，push
    ```python
    #!/usr/bin/python3
    import sys 
    　                   #2行あけましょう
    def tonum(s):
        try:
            return int(s)
        except:
            return float(s)
    　                   #2行あけましょう
    ans = 0 
    for line in sys.stdin:
        line = line.rstrip()
        ans += tonum(line)
    　
    print(ans)
    ```

---

## 5. その他リポジトリの操作

---

## 過去のコードの取り出し（動機）

- 昔のコードを一部復活させたいときにやりたくなる
    - 例: 次の履歴から「Add a command」時のコードを取り出したい
        ```bash
        $ git log 
        commit f02a20237590c9e4650f100928c6c2f969c111c3 (HEAD -> main, origin/main, origin/HEAD)
        （略）
            Support integer calculation
        　
        commit fa8aab8a2ade8cd33823f488fbb1bbec6d981260   #これの`plus_stdin`を取り出したい
        （略）
            Add a command
        　
        commit 68d342fbb7a9b65e402d0b6f5a7763e56f248937
        （略）
            Initial commit
        ```

---

## 過去のコードの取り出し（方法）

- 取り出すだけなら次の方法で可能　　　　　　　　　
    ```bash
    $ git switch -d fa8aab8         #コミットハッシュ値の先頭何桁を指定
    HEAD is now at fa8aab8 Add a command
    $ git branch
    - (HEAD detached at fa8aab8)            #使い捨てのブランチができる
      dev
      main
    $ cat plus_stdin 
    （略．try，exceptを加える前のコード）
    $ cp plus_stdin /tmp/                 #必要ならコードのコピーをとる
    $ git switch -                                            #元に戻る
    Previous HEAD position was fa8aab8 Add a command
    Switched to branch 'main'
    Your branch is up to date with 'origin/main'.
    ```

---

## ローカルリポジトリだけ作ったものをGitHubにアップ

- 手順
    1. GitHubに同名のリポジトリを作成
    2. `git remote add origin <リポジトリ>`で結びつけ
- 注意: メインのブランチをローカルとリモートで合わせること
    - 手元が`master`なのに，リモートが`main`のときは手元を`main`にするとよい　

---

## リポジトリの名前を変えたい

- リモート: GitHubのリポジトリのSettingsで変更
- ローカル: リポジトリの`.git/config`を編集
    - 実は変えなくてもリモートにpush可能　

---

## 6. まとめ

- Git/GitHub 
    - バージョン管理システム/サービス
        - 今日から必須の道具
            - レポート等も管理することを強く推奨
    - 他にも様々な操作が必要に
        - 困ったら仕組みから理解してみましょう　
- Pythonの文法
    - 今回出てきたもの
        - 例外処理
        - 関数
    - 分からなくなったら戻ってくること
