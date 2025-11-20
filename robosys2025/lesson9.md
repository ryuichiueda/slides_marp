---
marp: true
---

<!-- footer: "ロボットシステム学第9回" -->

# ロボットシステム学

## 第9回: ROS 2の通信と型

千葉工業大学 上田 隆一


<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## 今日やること

1. launchファイル
2. 独自のメッセージ型の作成
3. サービスの実装
4. パラメータ、actionlib

- 注意
  - こまめにGitHubにpushしながら進めましょう

---

## 1. launchファイル

- launchファイル
  - 複数のノードを一度に立ち上げるもの
    - 他にもいろいろ可能だがとりあえず
  - 作っておくと、ノードごとに`ros2 run`しなくてよい
- 形式
    - `setup.py`みたいにPythonでプログラムするもの（今日はこっち）
    - `package.xml`みたいにXMLで記述するもの
    - 他にもあったような

---

###  launchファイルの作成（準備）

- パッケージのディレクトリに`launch`ディレクトリを作成
    ```
    $ cd ~/ros2_ws/src/mypkg/                                                       
    $ mkdir launch
    ```

- `setup.py`にローンチファイルの場所を記述
    ```
      2 import os                  #追加。OSの機能のパッケージ
      3 from glob import glob      #追加。グロブ（ワイルドカード）を扱う関数
    （中略）
     11     data_files=[
    （中略）
     15        (os.path.join('share', package_name), glob('launch/*.launch.py'))                          
     16     ],                       #↑追加
    ```
- `package.xml`に依存関係を記述
    ```
    12   <exec_depend>launch_ros</exec_depend>
    ```

---

###  launchファイルの作成（記述）

- さきほど作った`launch`ディレクトリに設置
- 名前は`talk_listen.launch.py`としましょう
  - `setup.py`に`.launch.py`で終わると書いたので、それは守る
    ```python
      1 import launch
      2 import launch.actions
      3 import launch.substitutions
      4 import launch_ros.actions
      5
      6
      7 def generate_launch_description():
      8
      9     talker = launch_ros.actions.Node(
     10         package='mypkg',      #パッケージの名前を指定
     11         executable='talker',  #実行するファイルの指定
     12         )
     13     listener = launch_ros.actions.Node(
     14         package='mypkg',
     15         executable='listener',
     16         output='screen'        #ログを端末に出すための設定                                   
     17         )
     18
     19     return launch.LaunchDescription([talker, listener])                      
    ```

---

### ローンチファイル（実行）

- `colcon build`して実行
```bash
$ ros2 launch mypkg talk_listen.launch.py
[INFO] [launch]: All log files can be found below /home/ubuntu/.ros/log/202...
[INFO] [launch]: Default logging verbosity is set to INFO
[INFO] [talker-1]: process started with pid [17158]
[INFO] [listener-2]: process started with pid [17159]
（かなり遅れてlistener.pyの出力がまとめて表示される場合あり）
（Ctrl+Cで終了）
```

---

## 2. 独自のメッセージ型の作成

- 前回の通信: ひとつ整数を送受信するだけ
- 意味のあるひとかたまりのデータをまとめて送るには？
  - 意味のあるひとかたまりのデータ: 構造体に相当するもの<br />　
- 方法
  - 既存の型を利用
    - `$ ros2 interface list`で一覧表示可能
  - 自分で型（と型のためのパッケージ）を作成
    - やってみましょう

---

### msgファイルの作成

- 型を定義するパッケージを作成
  ```bash
  $ cd ~/ros2_ws/src
  $ ros2 pkg create --build-type ament_cmake person_msgs
  $ cd person_msgs
  ### package.xmlを前回のように編集 ###
  $ mkdir msg
  $ cd msg
  ```
- `msg`下に、次のような`Person.msg`というファイルを設置
    ```
    string name
    uint8 age
    ```
   - このファイルから、各言語で使える構造体のようなものが生成される

---

### ビルドの準備

- パッケージのトップディレクトリにある`CMakeList.txt`を編集
  - `find_package(ament_cmake REQUIRED)`の下あたりに、次の4行を記述
    ```cmake
    find_package(rosidl_default_generators REQUIRED)
    rosidl_generate_interfaces(${PROJECT_NAME}
      "msg/Person.msg"
    )
    ```
- `package.xml`も編集
  - `buildtool_depend`の下あたりに、次の3行を追加
    ```xml
    <build_depend>rosidl_default_generators</build_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```

---

### ビルド

- ビルドして環境に反映
  ```bash
  $ cd ~/ros2_ws
  $ colcon build
  （略）
  ---
  Finished <<< mypkg [0.57s]
  Finished <<< person_msgs [2.32s]                     
  
  Summary: 2 packages finished [2.51s]
    1 package had stderr output: mypkg
  ```
- `source`して、型が利用できるようになっているか確認
  ```bash
  $ source ~/.bashrc
  $ ros2 interface show person_msgs/msg/Person
  string name
  uint8 age
  ```

---

### Person型の利用（publish）

- `talker.py`からPerson型のメッセージを送信
    ```python
     1 import rclpy
     2 from rclpy.node import Node
     3 from person_msgs.msg import Person #変更
     4 
     5 rclpy.init()
     6 node = Node("talker")
     7 pub = node.create_publisher(Person, "person", 10) #変更
     8 n = 0
     9 
    10 
    11 def cb():
    12     global n
    13     msg = Person()         #送信するデータの型を変更
    14     msg.name = "上田隆一"  #msgファイルに書いた「name」
    15     msg.age = n            #msgファイルに書いた「age」                             
    16     pub.publish(msg)
    17     n += 1
    18 
    19 （続きは次ページ）
    ```

---

```python
20 def main():
21     node.create_timer(0.5, cb)
22     rclpy.spin(node)
```
   - ビルドして実行し、`ros2 topic echo トピック名`で確認のこと

---

### Person型の利用（subscribe）

- `listener.py`でPerson型のメッセージを受信、表示
    ```python
     1 import rclpy
     2 from rclpy.node import Node
     3 from person_msgs.msg import Person
     4 
     5 
     6 rclpy.init()
     7 node = Node("listener")
     8 
     9 
    10 def cb(msg):
    11     global node
    12     node.get_logger().info("Listen: %s" % msg)
    13 
    14 
    15 def main():
    16     pub = node.create_subscription(Person, "person", cb, 10)                 
    17     rclpy.spin(node)
    ```
    - `ros2 launch`で動作確認を

---

## 3. サービスの実装

- 疑問: ノード同士が直接、仕事の依頼やデータをやりとりしたいときにトピックは使える？
    - 使えるけど仕事の終わりの確認がめんどくさい
- <span style="color:red">サービス</span>を使うほうがよい
    - サービス: あるノードが別のノードに仕事を依頼する仕組み　


<center>実装してみましょう</center>

---

### 実装するサービス

- 人の名前を送ったら、その人の年齢を返すサービス
  - `listener`が依頼する側
  - `talker`が依頼する側

---

### srvファイルの作成

- 準備: `person_msgs`に`srv`というディレクトリを作成
  - `msg`と同じところに
  - 中に、次のような`Query.srv`を置く
    ```
    string name
    ---
    uint8 age
    ```
    - `---`の上: サービスを呼び出すときに呼び出し側が渡すデータ
    - `---`の下: サービスの実行後に呼び出し側が受け取るデータ


---

### ビルド

- `CMakeList.txt`に`Query.srv`を追加
  ```cmake
   15 rosidl_generate_interfaces(${PROJECT_NAME}
   16   "msg/Person.msg"
   17   "srv/Query.srv"   # 追加
   18 )
   ```
- ビルド、`source`、確認
  ```bash
  $ cd ~/ros2_ws/
  $ colcon build
  （略）
  $ source ~/.bashrc 
  $ ros2 interface show person_msgs/srv/Query
  string name
  ---
  uint8 age
   ```

---

### サービスのためのコールバック関数の実装

- `talker`側に、サービスが呼び出されたときの処理を書く
  - `talker.py`
    ```python
    （略）
     3 from person_msgs.srv import Query #使う型を変更
     4 
     5 rclpy.init()
     6 node = Node("talker")
     7 
     8 
     9 def cb(request, response):
    10     if request.name == "上田隆一":
    11         response.age = 46
    12     else:
    13         response.age = 255
    14 
    15     return response
    16 
    17 
    18 def main():
    19     srv = node.create_service(Query, "query", cb) #サービスの作成                     
    20     rclpy.spin(node)
    ```

---

### `ros2 service`で動作確認

- `talker`を立ち上げてからサービスの存在を確認し、呼び出してみる
  ```bash
  ### 確認 ###
  $ ros2 service list
  /query                  <- 表示されるか確認
  （以下略）
  ### 実行 ###
  $ ros2 service call /query person_msgs/srv/Query "name: 上田隆一"
  requester: making request: person_msgs.srv.Query_Request(name='上田隆一')
  
  response:
  person_msgs.srv.Query_Response(age=44)
  
  $ ros2 service call /query person_msgs/srv/Query "name: しらない 人"
  （略）
  response:
  person_msgs.srv.Query_Response(age=255)
  ```

---

### ノードからのサービス呼び出し

- `listener.py`を次のように書き換え
  - 前半
    ```python
    （ヘッダ部分はtalker.pyと同じ）
     4
     5 rclpy.init()
     6 node = Node("listener")
     7 
     8 
     9 def main():
    10     client = node.create_client(Query, 'query') #サービスのクライアントの作成
    11     while not client.wait_for_service(timeout_sec=1.0): #サービスの待ち待ち
    12         node.get_logger().info('待機中')
    13
    14     req = Query.Request()
    15     req.name = "上田隆一"
    16     future = client.call_async(req) #非同期でサービスを呼び出し
    ```
    - 後半（下）に続く

---

- 後半
    ```python
    18     while rclpy.ok():
    19         rclpy.spin_once(node) #一回だけサービスを呼び出したら終わり
    20         if future.done():     #終わっていたら
    21             try:
    22                 response = future.result() #結果を受取り
    23             except:
    24                 node.get_logger().info('呼び出し失敗')
    25             else: #このelseは「exceptじゃなかったら」という意味のelse
    26                 node.get_logger().info("age: {}".format(response.age))
    27 
    28             break #whileを出る
    29 
    30     node.destroy_node() #ノードの後始末   （後始末は無限ループでないので書きました。
    31     rclpy.shutdown()    #通信の後始       ただ、本来は無限ループでも書いたほうがよいです。）
    ```

---

### 動作確認

- 順番を変えて立ち上げてみましょう
  - `talker`を先、`listener`を後: 年齢が受け取れる
    ```bash
    $ ros2 run mypkg listener
    [INFO] [1664865500.552181002] [listener]: 待機中
    [INFO] [1664865501.554913737] [listener]: 待機中
    [INFO] [1664865501.806117977] [listener]: age: 46
    ```
  - `listener`を先、`talker`を後: 「待機中」が出たあと年齢が受け取れる
    ```bash
    $ ros2 run mypkg listener
    [INFO] [1664865501.806117977] [listener]: age: 46
    ```

---

## 4.1. パラメータ

- システムやノードのパラメータを管理する仕組み
    - 各ノードがアクセスして値を使用
    - 用途
        - センサの周波数などの設定（や変更）
        - プログラムの初期設定値の記録やノードへの伝達
    - 今の状態で確認できるパラメータ
      ```bash
      $ ros2 param list
      /talker:
        use_sim_time
      $ ros2 param get /talker use_sim_time 
      Boolean value is: False
      ```

---

## 4.2 アクション

ここでは、とりあえず「アクションというものがある」というだけお伝え

- アクション
  - サービスの長時間版
    - 呼び出し側が、途中の経過の観察やキャンセルできる
  - 使用例
    - ナビゲーション（目的地を指定して終わるまで待つ）
    - マニピュレータの姿勢変更（最終的な姿勢を指定して終わるまで待つ）
  - トピックやサービスを組み合わせて実装される

---

## まとめ

- やったこと
  - ローンチファイルを作成
  - 独自のメッセージの型、サービスを実装
  - パラメータ、アクションの把握（紹介のみ）
- 確認
  - 本日扱ったふたつのパッケージがGitHubにpushされていること
    - コミットの履歴も残っていること
