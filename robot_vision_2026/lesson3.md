---
marp: true
---

<!-- footer: "ロボットビジョン第3回" -->

# ロボットビジョン

## 第3回: 画像の識別とセグメンテーション

千葉工業大学 上田 隆一

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## 今日やること

- 識別の問題
- CNN
- U-Net


---

## 識別の問題

- データを数種類に分類する
    - 言葉の品詞
    - 感情（文章や表情から）
    - 動物
    - ...
- ANNでよく扱われてきた問題
    - かつては問題に応じて専用のANNを準備することが必須だった（今日はこの話）
- 問題: 識別のためのANNを数式で定義してみましょう
    - $\boldsymbol{x} = \boldsymbol{f}(\boldsymbol{x}|\boldsymbol{w})$
        - $\boldsymbol{x}$はデータだけど出力$\boldsymbol{y}$の形式は？

![bg right:30% 100%](./figs/cat_and_dog.svg)


---

### 出力の例（1/2）

たとえば、「犬、猫、それ以外」を識別したい場合

- その0
    - 犬を1、猫を2、それ以外を3
        - 難点: 数字の差が意味を持ってしまう
- その1: <span style="color:red">ワンホット（one-hot）ベクトル</span>（右図）
    - 犬を$(1,0,0)$、猫を$(0,1,0)$、その他を$(0,0,1)$
        - 難点: 犬か猫が分からないやつはその他？
        - 断定しないといけない場合はこれでいいが、曖昧さを許したい場合は使えない
    - ワンホットベクトル自体は随所で活用される

![bg right:30% 100%](./figs/one_hot.svg)

---

### 出力の例（2/2）

- $\boldsymbol{y} = (P_\text{猫}, P_\text{犬}, P_\text{それ以外})$
    - $P_\text{x}$は、対象が$\text{x}$である<span style="color:red">確率</span>
    - $\boldsymbol{y}$は確率分布とみなせる
- 識別用のANNの出力はこの形式が一般的
    - ひとつに決めたければ確率最大のものを選択
- 確率分布を出力する専用のレイヤー（次ページ）

![bg right:30% 100%](./figs/prob_output.svg)

---

### ソフトマックス層

- softmax（softな最大値）: 1つに決めないということ
- 入力$\boldsymbol{x} = (x_1, x_2, \dots, x_n)$に対し<span style="color:red">$y_i = \eta e^{x_i}$</span>を出力
    - $\eta$は正規化定数
        - $\sum_{i=1}^n y_i = 1$にするための定数（のようなもの）
- 損失関数: <span style="color:red">交差エントロピー</span>を使用
   - $\mathcal{L}(\boldsymbol{w}, \boldsymbol{x}|\boldsymbol{y}') = H(\boldsymbol{y}', \boldsymbol{y}) = -\sum_{i=1}^N y_i' \log y_i$
       - $\boldsymbol{y}$が出力、$\boldsymbol{y}'$が正解
       - <span style="font-size:70%">注意: $\boldsymbol{w}$はほかの層のパラメータ</span>
       - 数学好きな人への補足: カルバック・ライブラー情報量を最小化するのと等価
    - 正解がワンホットベクトルだと$\mathcal{L}(\boldsymbol{w}, \boldsymbol{x}| \boldsymbol{y}') = - \log y_i$
        - $i$が正解の元

![bg right:20% 95%](./figs/softmax_layer.png)


---

### クロスエントロピーを用いるときのパラメータ更新

- $\mathcal{L}(\boldsymbol{w}, \boldsymbol{x}|\boldsymbol{y}') = H(\boldsymbol{y}', \boldsymbol{f}(\boldsymbol{x}|\boldsymbol{w})) = -\sum_{i=1}^N y_i' \log f_i(\boldsymbol{x}|\boldsymbol{w})$
- $\dfrac{\partial}{\partial w}\mathcal{L}(\boldsymbol{w} , \boldsymbol{x} | \boldsymbol{y}') = \sum_{i=1}^k \dfrac{\partial f_i(\boldsymbol{x} | \boldsymbol{w})}{\partial w}\dfrac{y_i'}{f_i(\boldsymbol{x}|\boldsymbol{w})}=\dfrac{\partial \boldsymbol{f}(\boldsymbol{x}|\boldsymbol{w})}{\partial w}^\top  \boldsymbol{e}'$
    - $\boldsymbol{e}' = (
    y_1'/y_1 \  \ 
    y_2'/y_2 \  \ 
    \dots \ 
    y_k'/y_k
)^\top$
- 前回の2乗誤差のときと同じ式
    - $\boldsymbol{e}'$だけ形が違うが、各値が決まったベクトルなので問題ない
    - 同じ方法で誤差逆伝搬、パラメータ更新が可能

---

### ソフトマックス層の誤差逆伝搬（1/2）

- おさらい
    - 前の層に送る誤差: $J_{\boldsymbol{f}}(\boldsymbol{x})^\top\boldsymbol{e}'$
    - ソフトマックス層の$i$番目の出力の関数: $f_i(\boldsymbol{x}) = e^{x_i} (\sum_{j=1}^k e^{x_j}) ^{-1}$
- ヤコビ行列をつくるための偏微分（正規化定数の部分も偏微分しないといけないので大変です）
    - $\partial f_i(\boldsymbol{x}) / \partial x_i = e^{x_i} (\sum_{j=1}^k e^{x_j}) ^{-1} - e^{x_i} (\sum_{j=1}^k e^{x_j}) ^{-2}e^{x_i}= y_i - y_i^2$
    - $\partial f_i(\boldsymbol{x}) /\partial x_j = - e^{x_i} (\sum_{j=1}^k e^{x_j}) ^{-2}e^{x_j}= - y_i y_j$


---

### ソフトマックス層の誤差逆伝搬（2/2）

できたヤコビ行列を使って送る誤差を計算
- $J_{\boldsymbol{f}}(\boldsymbol{x})^\top \boldsymbol{e}' = \begin{pmatrix}
        y_1 - y_1^2 & -y_1y_2 & \dots & -y_1y_k \\
        -y_1y_2 & y_2 - y_2^2 & \dots & -y_2y_k  \\
        \vdots  & \vdots & \ddots & \vdots  \\
        -y_1y_k & -y_2y_k & \dots & y_k  - y_k^2 \end{pmatrix}
        \begin{pmatrix}
    y_1'/y_1 \\
    y_2'/y_2 \\ 
    \vdots \\ 
    y_k'/y_k
        \end{pmatrix}$
    $=\begin{pmatrix}
        y_1' - y_1(y_1' + y_2' + \cdots + y_k') \\
        y_2' - y_2(y_1' + y_2' + \cdots + y_k') \\
        \cdots \\
        y_k' - y_k(y_1' + y_2' + \cdots + y_k') 
    \end{pmatrix} =$<span style="color:red">$\begin{pmatrix}
        y_1' - y_1 \\
        y_2' - y_2 \\
        \cdots \\
        y_k' - y_k 
    \end{pmatrix}$</span>
    - とてもスッキリ


---

## 視覚・画像とANN（CNN）

- いままでの講義: 入力をベクトル$\boldsymbol{x}$として扱ってきた
    - つまり1列に数値をならべたもの
    $\Longrightarrow$画像だともったいなくない？
- 画像
    - 2次元（以上）のデータ
    - 近いところの画素は互いに関係が深く模様を形成（しているのに1列にバラすともったいない）

ということでCNNというものがある
（次ページ）

![bg right:40% 90%](./figs/cat_mono.png)

---

### CNN（convolutional neural network）

- テレビ局ではないです
- convolutional: 「畳み込みの」
-  画像の近いところの画素値を入力して
出力するニューロンを多用（右図）
    - 画像の近いところ: $n\times n$画素の正方形領域
    - 小領域の画素の特徴や変化を出力
    - さらに下の層でも畳み込みすることで全体の特徴を捕捉
- 「畳み込み層」と他の層の組み合わせで画像を処理

![bg right:30% 90%](./figs/convolution_neuron.png)

---

### CNNの部品1: 畳み込み層

- 画像の一部（n$\times$n画素の「窓」）領域に<span style="color:red">フィルタ</span>をかけて出力を合計し、バイアスを足して下流に送る（右上図）
    - あまり言及されないが、たいてい次は活性化関数の層
- フィルタを1つずつずらして適用（右下図）$\rightarrow$下流も画像に
    - 下流の画素数を変えたくない場合$\rightarrow$縁をパディング
    - 2つ以上ずらすこともあり（ずらす量: ストライドという）
- 畳み込みの演算（下図）
    - $\odot$: アダマール積（要素ごとに掛け算）$\rightarrow$全要素を足す

![bg right:20% 90%](./figs/cnn_conv.png)

$\qquad\qquad$![w:660](./figs/cnn_calc.png)

--- 

### フィルタの意味

- フィルタ: 従来の画像処理に使われてきたものと同じ
- 局所的な特徴（エッジなど）を検出
- 畳み込み層の学習=フィルタの学習
![w:700](./figs/cnn_filter.png)


--- 

### 畳み込み層の誤差逆伝播

- $\odot$の両側の各行列の要素を1列に並べてベクトルに
- フィルタをベクトル$\boldsymbol{w} = (w_1\ \ w_2 \ \dots\ w_n)^\top$に
- $\boldsymbol{w}$に対応する入力を$\boldsymbol{x} = (x_1 \ \ x_2 \ \dots \ x_n)^\top$に
- 出力の1画素$y$の誤差$e_y$に対する誤差逆伝播
- $y = f(\boldsymbol{x}| \boldsymbol{w}) = w_1x_1 + w_2x_2 + \cdots w_nx_n + b$
- $J_{f}(\boldsymbol{x}) = (w_1 \ \  w_2 \ \cdots \  w_n)^\top$
- この画素に関して送る量: $(e_{x_1} \ \ e_{x_2} \ \dots \ e_{x_n})^\top = (w_1 \ \  w_2 \ \cdots \  w_n)^\top e_y$
- ある入力画素1画素の誤差逆伝播の量: 
- 出力全画素分について$we_y$を足せばよい

![bg right:30% 96%](./figs/cnn_conv_bp.svg)


--- 

### 畳み込み層のパラメータ更新

- 出力の1画素$y$の誤差$e_y$に対する更新
- $\partial y/\partial w_i = x_i$、$\partial y/\partial b = 1$なので
    - $w_i \verb|-=| \alpha x_ie_y$
    - $b \verb|-=| \alpha e_y$
- 全出力に関して、上の2式の更新を行えばよい

---

### CNNの部品2: プーリング層（サブサンプリング層） 

- 画素数を減らして特徴を強調する層
- よく使われるもの
    - 最大値を残すmaxプーリング
    - 平均値を計算して送る平均値プーリング
- 学習はしない
- 後段（ものを分類するネットワークなど）が学習しやすく
- 誤差逆伝播
   - maxプーリング: 最大値として選択した画素だけに、来た画素をそのまま伝播
   - 平均値プーリング: 平均値を計算した画素すべてに、来た誤差を均等に割って伝播

![bg right:23% 90%](./figs/cnn_pooling.png)


---

### チャンネル

- 1層に複数の画像がある場合、多チャンネルに
- カラー（RGB）画像を扱う場合: 3チャンネル
- 1つの画像に$n$個のフィルタ$\rightarrow n$個のチャンネルに
- 下図[LeNet[LeCun1989]](https://direct.mit.edu/neco/article-abstract/1/4/541/5515/Backpropagation-Applied-to-Handwritten-Zip-Code)の構造<span style="font-size:70%">（画像: Zhang et al. [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)）</span>
- 画像から手書きの数字を識別するCNN（1ch $\rightarrow$ 6ch $\rightarrow$ 16ch）
- チャンネル数だけの種類の特徴を捉えることが可能
     ![w:800](https://upload.wikimedia.org/wikipedia/commons/3/35/LeNet-5_architecture.svg)


---

### チャンネルとフィルタ（イレギュラーな構成でない場合）

- 畳み込み層: $c$チャンネルの入力に対し、$c \times n \times n$の3次元形状のフィルタを適用
- $n\times n$:画素のフィルタを$c$個用意してそれぞれのチャンネルに適用
- 各チャンネルの出力を足し込んで1チャンネルに
    ![w:500](./figs/cnn_conv_multi_ch.svg)
- プーリング層: チャンネル数は不変


---

### 代表的なCNN（1/2）

- LeNet[[LeCun1989]](https://direct.mit.edu/neco/article-abstract/1/4/541/5515/Backpropagation-Applied-to-Handwritten-Zip-Code): 手書き文字を識別
- 畳み込み・プーリング$\rightarrow$全結合層
    - シグモイド関数を活性化関数に使用
- AlexNet[[Krizhevsky2012]](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf): 畳み込みを5層に深く
（当時としては深い）
- 右図: LeNet（左）とAlexNet（右）の比較
- LeRUを活性化関数に使用
- 1000種類の識別
- [AlexNetの論文](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf)
    - 学習した中間層や認識結果が見られる

![bg right:33% 90%](https://upload.wikimedia.org/wikipedia/commons/a/ad/AlexNet_block_diagram.svg)

<a style="font-size:70%" href="https://commons.wikimedia.org/wiki/File:AlexNet_block_diagram.svg">右図: Zhang et al., CC BY-SA 4.0</a>

---

### 代表的なCNN（2/2）: ResNet[[He+ 2016]](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf)

- 性能と層の多さが当時圧倒的
- 右図のようにとても多層（152層）
    - <span style="font-size:70%">（画像: Zhang et al. [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)）</span>
- 次の技術で多層化が実現（次ページ、次々ページ）
    - 図に多数の「迂回」: <span style="color:red">スキップ（残差）接続</span>
    - 学習データのミニバッチごとに正則化（batch normalization）
        - バッチ: ある数の教示データ
        - 少量のバッチごとにパラメータ変更を行う「ミニバッチ」という手法がある
        - 畳み込み層のあと、活性化関数の前に層として挿入

![bg right:15% 100%](https://upload.wikimedia.org/wikipedia/commons/6/6f/Resnet-18_architecture.svg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original)

---

### スキップ（残差）接続

- あるレイヤーの出力を次の層だけでなく、
別の層にも入力する接続方法
    - 入力に挟まれた層は入出力の差分を
    学習することに
- スキップ接続の有無: 初期の学習の容易さに影響
    - スキップ接続なし: 最初は$\boldsymbol{y}$がランダム
    - スキップ接続あり: （途中の層の出力が最初ゼロだと）最初は$\boldsymbol{y}=\boldsymbol{x}$に

![bg right:30% 90%](../advanced_vision/figs/skip.png)



---

### バッチ正則化層[[Ioffe+ 2015]](https://proceedings.mlr.press/v37/ioffe15.pdf)

- ある入力のセット$B = \{\boldsymbol{x}^{(j)} = (x_1^{(j)}, x_2^{(j)}, \dots, x_n^{(j)} ) | j = 1,2, \dots, m\}$
に対し、次の値を計算
    - 平均値$\mu_1, \mu_2, \dots, \mu_n$（ベクトルの各元に対して計算）
    - 分散$\sigma^2_1, \sigma^2_2, \dots, \sigma^2_n$（同上）
- ある元の入力を次のように正規化
    - $\hat{x_i}^{(j)} = (x_i^{(j)} - \mu_i)/\sqrt{\sigma^2_i + \varepsilon}$
        - $\varepsilon$: ゼロ割り防止の微少量
- パラメータ（学習対象）$\gamma_i$、$\beta_i$で、その元に強弱、シフトを付加
    - $y_i^{(j)} = \gamma_i \hat{x_i}^{(j)} + \beta_i$
    - 注意: 畳み込み層のうしろに置く時は$\gamma$、$\beta$はチャネルごとに1個ずつ

---

### CNNのまとめ

- 畳み込み層で模様の特徴を抽出、プーリング層で縮約
- 画像から物体を識別
- LeNetは1989年、AlexNetは2012年、ResNetは2015年
- ResNetがANNを深くするきっかけに
- CNNにはさらなる用途が（次ページから）


---

## セグメンテーション技術

- 画像の画素ごとに識別
- 代表的な手法: U-Net
    - 例: [[三上他 2022]](https://www.jstage.jst.go.jp/article/jrsj/40/2/40_40_143/_article/-char/ja)（右図）
        - 葉、茎、背景を識別
    - 構造
        - CNNの後ろに逆向きのCNNをつけたもの
        - 「転置畳み込み（後から説明）」という操作で画像を大きくしていく（構造は次ページ）


![bg right:25% 90%](https://github.com/ryuichiueda/jrsj_color_figs/blob/main/vol_40_no_2/fig_11.png?raw=true)

---

### U-Netの構造

- 左半分: CNN（物体の識別のような処理）
- 右半分: 逆向きのCNN（識別結果からの画像の構築）
- スキップ接続を使用
    - 途中で次元が落ちているので単なる差分学習以上の意味

<img width="700" src="https://upload.wikimedia.org/wikipedia/commons/2/2b/Example_architecture_of_U-Net_for_producing_k_256-by-256_image_masks_for_a_256-by-256_RGB_image.png" />
<a style="font-size:70%" href="https://commons.wikimedia.org/wiki/File:Example_architecture_of_U-Net_for_producing_k_256-by-256_image_masks_for_a_256-by-256_RGB_image.png">画像: Mehrdad Yazdani, CC BY-SA 4.0</a>

---

### 転置畳み込み

- 画像の解像度を上げる操作
    - 画像をパディングして大きくし、フィルタを適用$\rightarrow$画像が大きく
    - この操作とスキップ接続で得た元の画像の情報からセグメンテーション
- 誤差逆伝播、パラメータ更新: 通常の畳み込みと同じ

![bg right:25% 95%](./figs/trans_conv.png)

---

## オートエンコーダと潜在空間

---

### オートエンコーダ

- 入力と出力を一致させるように学習されたANN [[Hinton 2006]](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.cs.toronto.edu/~hinton/absps/science.pdf)
    - 損失関数: 入出力の平均二乗誤差（MSE, mean square error）
        - 学習のためのラベル付けは不要（教師無し）
    - 構成はCNNでも全結合でもよいが、U-Net状に中間の次元を小さく
        - 入力側: どんどん情報を落としていく
        - 出力側: どんどん情報を増やしていく
    - 疑問: 何の意味があるの？
![w:900](./figs/autoenc.png)

---

### 入力側（<span style="color:red">エンコーダ</span>）のやっていること

- 入力されたデータの分類
    - （学習がうまくいった場合は）似たような画像から似たような出力が得られる
    - うしろに全結合層（とソフトマックス層）をくっつけて追加で学習させると分類器に
- 右図の例: 出力を2次元まで縮小した場合の
出力の分布の例
（注意: 実用的なものはもっと高次元）
    - 分布している空間を<span style="color:red">潜在空間</span>と言う

![bg right:35% 95%](./figs/encoder.png)


---

### 出力側（<span style="color:red">デコーダ</span>）のやっていること

- 潜在空間のベクトルからデータを復元
    - 例: 「犬」のベクトルが来たら犬の写真や絵を描画
    - 復元方法（絵の描き方）を学習
        - 転置畳み込みのフィルタなどのパラメータに
    - 復元しやすいようにエンコーダ側が学習される
        - 潜在空間でのベクトルの分布が決まる

![w:800](./figs/decoder.png)


---

### オートエンコーダの利用

- エンコーダとデコーダを分離して利用
- エンコーダ
    - 先に前結合層などを取り付けて分類器に
    - 先に別のデコーダを取り付けると別のものが<span style="color:red">生成</span>される
- デコーダ
    - 学習に用いたもの以外のエンコーダを取り付けると変換器に
        - 例「犬」と入力$\rightarrow$犬の絵を<span style="color:red">生成</span>

<center>ちまたで<span style="color:red">生成AI</span>と言われるものの原型</center>

![bg right:30% 95%](./figs/autoenc2.png)

---

## まとめ

- CNNからオートエンコーダまで学習
    - 画像の識別から生成までの流れを見てきた
        - CNNによる物体の識別: エンコーダ+識別器
        - U-Netによるセグメンテーション: オートエンコーダに似た構造
    - 次回以降にいくつかの応用
        - 台形の図がよく出てくる

![bg right:30% 95%](./figs/autoenc2.png)

