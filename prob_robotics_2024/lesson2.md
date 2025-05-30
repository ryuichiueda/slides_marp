---
marp: true
---

<!-- footer: 確率ロボティクス第2回 -->

# 確率ロボティクス第2回: 確率・統計の基礎I

千葉工業大学 上田 隆一



<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->


## あるデータ（詳解2.1節）

センサの計測値を記録してみた

- 方法
    - ロボットを決めた距離だけ壁から離して設置
    - 2日間、3秒ごとにセンサの値を記録
        - 光センサ
        - レーザスキャナ（LiDAR）の正面の1本のレーザー

![bg right:40%](./figs/sensor_experiment.jpg)

---

## [200mm壁からロボットを離して得たデータ](https://github.com/ryuichiueda/LNPR/blob/master/data/sensor_data_200.txt)


![bg right:30%](./figs/data200.png)

- 列
    - 1: 日付
    - 2: 時分秒
    - 3: 光センサの値（壁から反射した光の強さ）
    - 4: LiDARの1本のレーザから得られた壁の距離[mm]

　
<center>値が揺らいでいる</center>

---

### 値のゆらぎ・ばらつき

- LiDARからの値（最初に得られた10個）
    - 214, 211, 199, 208, 212, 212, 215, 218, 208, 217, ... 　
- ロボットでこの値を使うときに気になること
    - 例えば壁の前200[mm]に正確に止まる、などの用途で
        - 毎回値が違うのにどれを信じればよい？
        - 200[mm]ということなのに210[mm]前後の値が多い
        - 1[mm]の違いもなくぴったり止まりたいが可能？

 
<center>なんらかの工夫や計算が必要そう</center>

---

## 値のばらつきの観察

LiDARからの値（以後センサ値と呼ぶ）の<br />ばらつきを視認してみましょう

- ヒストグラムの作成
    - 度数分布をグラフ化
        - 度数分布: データの値の範囲を区切り、各区間の値の個数<span style="color:red">頻度</span>を集計したもの
    - 図: 区間の幅1で描いたヒストグラム
        - （整数のデータで幅1なので例としてはあまりよくない）

![bg right:40%](./figs/sensor_200_histgram.png)

---

## ヒストグラムの形の解析<br />（詳解2.2.2項）

- このヒストグラムや元のデータから何を調べられるでしょうか
    - 用語を確認しながら考えてみましょう

![bg right:40%](./figs/sensor_200_histgram.png)

---

### 頻度・事象

- <span style="color:red">頻度</span>: ある現象（確率・統計の用語では<span style="color:red">事象</span>）が起きた回数
    - 頻度という言葉の使用例:
        - 210[mm]あたりの値が得られた頻度が高い
        - 値が194[mm]や226[mm]に近づくほど頻度が低くなる
    - 事象の例:
        - センサ値が210[mm]だった
        - センサ値が210[mm]以上だった、等


![bg right:35%](./figs/sensor_200_histgram_35pct.png)

---

### ヒストグラムの広がり

- 疑問: センサ値が毎回違ってヒストグラムが広がりをもつのはなぜ？
* 理由: なんらかの<span style="color:red">雑音</span>が存在するから
    - <span style="color:red">雑音（ノイズ）</span>: 値がゆらぐ（乱す）原因
        - 例: センサ内の電気的なゆらぎ、<br />外光、湿度、<span style="color:red">正体不明</span>・・・
        - ロボットの場合、センサを不適切な環境で使うので混沌を極める

![bg right:35%](./figs/sensor_200_histgram_35pct.png)

---

### ヒストグラムの偏り

- 疑問: 壁の距離が200[mm]と説明されたのに<br />頻度の高い値が210[mm]付近になるのはなぜ？
* なんらかの<span style="color:red">バイアス</span>が存在するから
    - <span style="color:red">バイアス（偏り）</span>: 値がずれる原因
        - 例: 筆者の勘違い、センサの取り付けた向きのずれ、正体不明・・・
        - 事前にキャリブレーションできるがゼロにはできず、ロボットの場合は動かしているうちに再発ということも
        - 雑音と違いデータから量を推測不可能
    - 非常に厄介

![bg right:35%](./figs/sensor_200_histgram_35pct.png)

---

### 誤差

- <span style="color:red">誤差</span>: 何か測りたいものの「真の」値とセンサの値の差
- 誤差の種類
    - 偶然誤差: 主に雑音による
    - 系統誤差: 主にバイアスによる
    - 過失誤差: 実験データの記録間違いなど

ロボットを動かす = これら誤差との戦い

---

## 雑音の数値化（詳解2.2.3項）

いまの話を数字を使って議論しましょう

---

### 平均値

- <span style="color:red">平均値</span>: 全センサ値を足してセンサ値の個数で割ったもの
- 次の式で表される
    - $\mu = \frac{1}{N}\sum_{i=0}^{N-1} z_i$
        - $z_0, z_1, \dots, z_{N-1}$: センサ値
        - $N$: センサ値の個数　
- 今扱っているセンサ値の平均値: 209.7[mm]
    - 分かること: 200[mm]だと言っていたが1[cm]くらい違う
    （平均値がないとこういう議論は不可能）
- [演習問題](https://b.ueda.tech/?page=robot_and_stats_questions#大量データの平均値)

---

### 分散、標準偏差

- 平均値はわかったけど、各センサ値はそこからどれだけ離れているのか
    $\rightarrow$<span style="color:red">分散、標準偏差</span>で数値化　
- 分散: 各センサ値と平均値の差の2乗の平均値
    - 通常は2乗和を$N-1$で割ったもの（<span style="color:red">不偏分散</span>）を使用
        - $\sigma^2 = \frac{1}{N-1}\sum_{i=0}^{N-1} (z_i - \mu)^2 \quad (N>1)$
        - 理由はロボットの確率・統計に
- 標準偏差: 分散の正の平方根（上の式の$\sigma$）
    - センサ値と単位が揃うので分散よりイメージがつきやすく便利
        - 「誤差はどれだけ？」と聞かれて答える値
    - 今扱っているセンサ値の標準偏差: 4.8[mm]<span style="font-size:70%">（つまり5[mm]ぐらいの誤差）</span>
- [演習問題](https://b.ueda.tech/?page=robot_and_stats_questions#大量データのばらつき)

---

## （素朴な）確率分布（詳解2.2.4項）

- ここでやりたいこと: 度数分布から、未来にどんなセンサ値が得られそうかを予想　
- なぜやるか
    - ロボットが実際に得られたセンサ値と予想を比較
        - 自己位置推定で出てくる演算
    - センサのシミュレーション

---

### 予想のアイデア

- 未来のセンサ値を集めたら今までと同じ度数分布が得られるのではないか？
- 度数分布を頻度でなく割合の分布に
    - $P_{\textbf{z}}(z) = N_z / N$
        - $N_z$: センサの値が$z$だったという事象の頻度
    - 理由: 集める個数で頻度は変わるので
- 全センサ値の種類に関して$P_{\textbf{z}}(z)$を足し合わせると1に
    - <span style="color:red">$P_{\textbf{z}}(z)$を確率と呼びましょう</span>

![bg right:35%](./figs/sensor_200_histgram_35pct.png)

---

### 確率分布

- ヒストグラムを確率のグラフに描き直してみる
    - 上: ヒストグラム
    - 下: 確率$P_{\textbf{z}}$のグラフ
        - 縦軸の値が変わっただけ
- 用語
    - 関数$P_{\textbf{z}}$: 確率質量関数と呼ぶ
    - $P_{\textbf{z}}$の形状や$P_{\textbf{z}}$そのものを<span style="color:red">確率分布</span>と呼ぶ


![bg right:35%](./figs/hist_and_prob.png)

---

## 確率分布を用いたシミュレーション<span style="font-size:70%"><br />（詳解2.2.5項）</span>

- $P_{\textbf{z}}$にしたがってセンサ値をひとつずつ生成
    - 「ドロー」と表現
    - 数式での表現: <span style="color:red">$z \sim P_{\textbf{z}}$</span>
    - 「したがって」とは
        - 例えば$P(200\text{})/P(150\text{}) = 2$なら$z=200$を$z=150$より2倍出現しやすく　
- 右のヒストグラム: シミュレーションで得たもの
    - センサの特性を再現

![bg right:30%](./figs/lidar_simulation.png)

---

## 確率モデル（詳解2.3節）


- 度数分布から確率分布を作ることへの疑問
   - 度数分布のデコボコは重要なのか？
       - データの回数が少ないともっとデコボコ
   - 実際に得られた値より小さな/大きな値になる確率はゼロ？
   - なにか法則性（つまり数式）を当てはめられないだろうか？

![bg right:30%](./figs/sensor_200_histgram_35pct.png)

「確率分布のモデル」を当てはめようという発想

---

## ガウス分布の当てはめ（詳解2.3.1項）

- たぶん、確率・統計を勉強した人は「<span style="color:red">ガウス分布</span>」を当てはめようとする
    - 根拠はない（本当は違うけど是とする）　
- ガウス分布の形状
    - $p(z | \mu, \sigma^2 ) = \frac{1}{\sqrt{2\pi}\sigma} e^{ - \frac{(z - \mu)^2}{2\sigma^2}}$
         - $\mu$: 平均値、$\sigma$: 標準偏差
         - 図: センサ値の$\mu$と$\sigma$から描いたガウス分布
             - ヒストグラムとよく似ている
         - 値が確率でないことに注意（次ページ）
             - [練習問題](https://b.ueda.tech/?page=robot_and_stats_questions#連続値と確率)

![bg right:30%](./figs/gauss_200.png)

---

## 確率密度関数（詳解2.3.2項）

- ガウス分布からの確率の求め方: $p(z | \mu, \sigma^2 )$を積分
    - $p$の値を<span style="color:red">密度</span>と言う
    - 密度を積分すると確率に（体積と同じ）
    - 例
        - センサの値が$210$より小さい確率: <span style="font-size:90%">$P(z < 210) = \int_{-\infty}^{210} p(z | \mu, \sigma^2 ) dz$</span>
        - センサの値が$210$: <span style="font-size:90%">$P(z = 210) = \int_{-209.5}^{210.5} p(z | \mu, \sigma^2 ) dz$</span>
            - センサの値が離散値なのに連続関数を当てはめているのでこうなる
    - 右図: この計算で作った確率分布

![bg right:30%](./figs/int_gauss.png)

---

### 用語の補足

- 密度を返す関数$p$: <span style="color:red">確率密度関数</span>
- $p$の形状や$p$そのものも確率分布と呼ぶことがある
- ガウス分布は特に$\mathcal{N}$と表記される
   - $\mathcal{N}(z | \mu, \sigma^2 ), \mathcal{N}(\mu, \sigma^2)$などと表記　
- $P(z < a) = \int_{-\infty}^a p(z) dz$を累積分布関数と呼ぶ
    - 右図
    - $P(a \le z < b) = P(z < b) - P(z < a)$


![bg right:30%](./figs/cdf.png)

---

### ここまでのまとめ

- やったこと: LiDARからのデータの解析
    - ヒストグラムで表現
    - 平均値等、データのゆらぎ（ばらつき）の度合いを数値化
    - ガウス分布とみなしてモデル化
        - 確率分布を$\mu$と$\sigma^2$だけで表現　
- 何ができるようになったか
    - センサの値がばらつく原因が不明でも雑音を分析
    - ロボットが壁に対してどれくらいの正確さで距離をとれるか見積もり
    - 平均値からバイアスによる系統誤差を計算$\rightarrow$キャリブレーション
    - ・・・

