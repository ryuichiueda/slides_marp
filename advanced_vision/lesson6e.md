---
marp: true
---

<!-- footer: "Advanced Vision Lesson 6" -->

# Advanced Vision

## Lesson 6: The Structure of the Transformer

Ryuichi Ueda, Chiba Institute of Technology

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## Contents

- The Structure of Transformer
- A Simple Application of Transformer

(More complex applications will be discussed next lesson.)

---

## Structure of Transformer (for translation)

- Consists of an encoder and a decoder
    - Left: Encoder
        - Input: Sentence before translation (e.g., "This is a pen.")
    - Right: Decoder
        - Input: Token indicating "start of translation" or partially translated sentence (e.g., "This is")
        - Output: Next word (e.g., "a")

<center style="padding-top:0.5em">Let's take a look at it step by step</center>

![bg right:38% 100%](https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png)

[<span style="font-size:70%">Image: CC-BY-4.0 by dvgodoy</span>](https://commons.wikimedia.org/wiki/File:Transformer,_full_architecture.png)

---

### Encoder

- Main part: in the dark yellow frame
    - "Nx layers": Concatenating multiple layers.
    - See the next page for details.
- Input (bottom of the figure): $H_\text{enc} = \sqrt{D}E + P$
    - $E=[\boldsymbol{e}_{w_1}\ \boldsymbol{e}_{w_2}\ \dots\ \boldsymbol{e}_{w_N}]^\top$
        - Sentence (a sequence of tokens represented as a $D$-dimensional vector)
- Output: $H_\text{enc}'$ with weights changed according to the decoder's work.
    - Context is reflected.

![bg right:28% 95%](./figs/transformer_encoder.png)

---

### Layer normalization

- The three "Norm"s in the figure
- Normalize the elements of each vector $\boldsymbol{h}=(h_1 \ h_2 \ \cdots \ h_D)^\top$ to equalize the influence of each vector.
    - How to normalize?
        - 1: The mean of $h_{1:D}$ is $0$ and the standard deviation is $1$.
        - 2: For each $h_i$, parameters $\gamma_i, \beta_i$ (training target) are prepared and transformed into $\gamma_ih_i + \beta_i$.
            - Because the importance of each element varies depending on its position.

![bg right:28% 95%](./figs/transformer_encoder.png)

---

### <span style="color:red">Self-Attention Mechanism</span>

- Changes token vectors based on the system's own information.
    - Reflects context (see next page for details).
- Mechanism: Q, K, and V are all generated from the input to the system.
    - Query: $Q= W_\text{Q}H$<span style="color:red">$_\text{enc}$</span> (previously it was $H_\text{dec}$).
    - Key: $K= W_\text{K}H$<span style="color:red">$_\text{enc}$</span> (same as above)
    - Value: $V= W_\text{V}H_\text{enc}$
    - Output: $H'=$Softmax$\Big(\dfrac{QK^\top}{\sqrt{D}}\Big)V$
- The previous attention mechanism was <span style="color:red">Cross Attention Mechanism</span>

![bg right:20% 100%](./figs/transformer_kvq.png)

---

### Supplementary information on self-attention mechanisms [[Google2017]](https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/)

- If we simply associate pronouns with nouns, we cannot tell whether the next "it" is "dog" or "street."
    - 1: The animal didn't cross the street because it was too tired.
        - it: dog
    - 2: The animal didn't cross the street because it was too wide.
        - it: street
- KVQ: By applying not only nouns but also all tokens to a matrix $K$, we can calculate the proximity of the query (it) to the other.
    - "You shall know a word by the company it keeps!" [[Firth1957]](https://cs.brown.edu/courses/csci2952d/readings/lecture1-firth.pdf) (Reprinted)

---

### Multi-head Attention

- Split the attention mechanism into multiple parts.
    - $W_\text{K}, W_\text{V}, W_\text{Q}$ ($D \times D$ matrix) is divided.
        - $Q^{(m)}= W_\text{Q}^{(m)}H$
        - $K^{(m)}= W_\text{K}^{(m)}H$
        - $V^{(m)}= W_\text{V}^{(m)}H\quad$ ($m=1, 2, \dots, M$)
            - $W_X^{(m)}$: $(D/M) \times D$ matrix obtained by cutting $W_X$ horizontally.
    - In terms of ANNs, connections are broken every $m$ and become independent.
        - Each one changes how it interprets the sentence. (It is trained to do so.)
- The $m$ outputs are combined$\rightarrow$ return to $D \times D$ matrix.

![bg right:20% 100%](./figs/transformer_kvq.png)

---

### Feedforward layer (fully connected layer)

- Text passed through the self-attention mechanism is passed through.
    - The upper of the two dotted boxes in the right figure.
    - Features are further emphasized through a nonlinear activation function (ReLU in the original Transformers).

![bg right:28% 95%](./figs/transformer_encoder.png)

---

### Additional Notes 1

- Both the attention mechanism and the feedforward layer use skip connections.
    - Each layer learns and outputs differentials.
    - To provide easy-to-understand input to each layer at the beginning of learning.
        - Necessary because the layers are deep.
- Although not shown in the figure, dropout layers are used in several places.
    - Dropout: a process that disables a certain percentage of neurons per learning unit (batch).
        - Prevents overfitting by not assigning specific roles to specific neurons.

![bg right:20% 95%](./figs/transformer_encoder_body.png)

---

### Additional Notes 2

- GELUs (Gaussian Error Linear Units) are sometimes used instead of ReLUs as the activation function.
    - $h(x) = x\cdot \frac{1}{2}\big\{ 1 + \text{erf}(x/\sqrt{2})\big\}$
        - $\text{erf}(a) = \frac{2}{\sqrt{\pi}}\int_0^a e^{-t^2}\text{d}t$
    - Differentiable

![bg right:30% 100%](https://upload.wikimedia.org/wikipedia/commons/4/42/ReLU_and_GELU.svg)<span style="font-size:50%">([Image by Ringdongdang CC BY-SA 4.0](https://commons.wikimedia.org/wiki/File:ReLU_and_GELU.svg))

---
### Encoder Summary

- Trained to achieve the following behavior:
    - Receives a sentence as a matrix $H_\text{enc}$, which is a list of token vectors and adds positional information.
    - Operates each vector in $H$ according to the context using a self-attention mechanism and a fully connected layer.
        - Repeats the above steps.
    - Outputs $H'_\text{enc}$, which reflects the context.
- The backpropagation error received depends on the decoder.

![bg right:28% 95%](./figs/transformer_encoder.png)

---

### Decoder (and Head)

- The main body is in the green box.
    - Receives a matrix $H_\text{dec}$ corresponding to the sentence up to that point.
- An ANN is connected after the decoder to perform the specific task.
    - In the case of translation, a fully connected layer is used to predict the next word.
    - The decoder changes $H_\text{dec}$ to $H'_\text{dec}$ to make this task easier.

![bg right:45% 100%](./figs/transformer_decoder.png)

---

### Structure of Decoder

- (Self-Attention + Cross-Attention + Feedforward Layer) $\times N$
- Self-Attention
    - Manipulates $H_\text{dec}$ by considering the context of the sentence during translation
    - "Masked" in the diagram means: A mechanism for masking the latter half of a sentence
        - During training, completed translation examples are input, so this is necessary
        - Example: When training to think what comes next after "This is," the input is "This is a pen.", so the element corresponding to "a pen" in $W_X$ is masked.
- Cross-Attention: Reflects the decoder output $H'_\text{enc}$

![bg right:15% 100%](./figs/transformer_decoder2.png)

---

### Beyond the Decoder

- Predicts the next word after the decoder input with a fully connected layer
- Can be trained like a skip-gram
- Output is the probability that each token will appear next
- There are as many dimensions as there are token types.
- Learning progresses by backpropagating the error in this area.
- Loss function: Cross entropy
- $-\sum_{i=1}^{N_\text{token}} P(\boldsymbol{e}_i)\log Q(\boldsymbol{e}_i)$
$= - \log Q(\boldsymbol{e}^*)$
- $P$ is the correct answer, and $Q$ is the output.
- $\boldsymbol{e}^*$: The correct token.

![bg right:40% 125%](./figs/transformer_prediction.png)

---

### Summary of the Transformer (for translation) architecture

- What kind of problem was it solving? $\rightarrow$Probability problems like this
- $\Pr\{$next word$|$original sentence$,\quad\!\!\!\!$original sentence$\}$
- Transformer innovations
- Adding location information to the original and original sentences
- Considering context
- Using a self-attention mechanism to identify notable points from the original sentence and incorporate them into the embedding (encoder)
- Using a self-attention mechanism to consider context in the original sentence, and then incorporating the context from the encoder using a cross-attention mechanism

---
## Applications of Transformer

- Sentiment analysis
- Sentence generation

(More advanced topics will be covered next time.)

---

### Sentiment analysis using a Transformer encoder

- Considering applying Transformer to classification tasks
- Input: Sentence (e.g., "I found a 100 yen coin today.")
- Output: Emotion (happy, happy, sad, etc.)
- Can be configured with an encoder [[Nakai 2025]](https://gihyo.jp/book/2025/978-4-297-14972-7)
- Add a token (class token) called `[CLS]` to the beginning of a sentence for training.
- After training, the output class token gathers information for analysis.
- This basic structure can be used as is for object recognition using the Vision Transformer (next time).

![bg right:30% 100%](./figs/sentiment_analysis.png)

---

### Sentence generation using a Transformer encoder

Also from [[Nakai 2025]](https://gihyo.jp/book/2025/978-4-297-14972-7) (Section 4.3.2)

- Training with the configuration shown on the right allows for random sentence generation.
- Because context is taken into account, the output is fairly natural (though there is no guarantee that the content is correct).
- GPT uses a decoder (we will do this in the next post or later).

![bg right:20% 90%](./figs/transformer_encoder_generator.png)

---

## Summary

- Transformer Encoder
- Reflecting context in embedding
- Adding location information ($\rightarrow$) and self-attention
- Transformer Decoder
- Encoder functionality plus cross-attention allows for other languages ​​to be reflected in the context.
- Masking during training
- Other References: [[Kikuta 2025]](https://gihyo.jp/book/2025/978-4-297-15078-5)
