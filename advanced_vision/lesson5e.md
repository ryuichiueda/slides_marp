---
marp: true
---

<!-- footer: "Advanced Vision Lecture 5" -->

# Advanced Vision

## Lecture 5: Embeddings and Adding Context

Ryuichi Ueda, Chiba Institute of Technology

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## Contents

- Why should we handle language models in vision lectures?
- Word2vec
- Transformer
- Applications of the Transformer

---

## Why do we learn natural language in vision courses?

- Existence of image $\leftrightarrow$ language applications
    - Image generation and object recognition in response to prompts
        - Stable diffusion
        - Segment Anything Model
↑ All of these use the Transformer discussed here.
- Applying language processing techniques to image processing
    - Transformer$\rightarrow$Vision Transformer
    - The only difference is the type of data, with few essential differences (?)
- The popularity of the Transformer: Used in a variety of places, as mentioned above

<center>We have no choice</center>

---

## Word2vec[[Mikolov2013]](https://arxiv.org/abs/1301.3781)

- Models and frameworks for representing words as vectors
- The vector representations created by Word2vec are used as input for the Transformer

---

### Word Embedding, Distributed Representation

- Similar words are represented by similar vectors.
    - Example (more dimensions are needed)
        - Uncle$= (0.9, 0.32, 0.07)$, Aunt$= (0.7, 0.55, 0.08)$, Estate$= (0.1, 0.05, 0.88)$
    - Similarity can be calculated using the dot product.
        - Uncle$\cdot$Aunt$= 0.77$
        - Uncle$\cdot$Estate$= 0.07$
    - Increasing the dimension allows for calculation of similarity from various perspectives.
- <span style="color:red">Distributed Representation (Embedding)</span>: A vector representation of words like the one above.
- <span style="color:red">Embedding</span>: Creating a distributed representation.

![bg right:15% 100%](./figs/embedding.png)

---

### Relationship between embeddings and what we've discussed so far

- Space of distributed representations = latent space
    - The input is mapped to a different space using an encoder
    - (Probability is not considered in the case of Word2vec)
- Question
    - How do we create similarity between words in the latent space?
        - What is the encoder's structure?
        - What is the decoder's structure?
        - What should we train?

![bg right:30% 100%](./figs/word_latent.png)

---

### Distributional Hypothesis

- "You shall know a word by the company it keeps!" [[Firth1957]](https://cs.brown.edu/courses/csci2952d/readings/lecture1-firth.pdf)
    - ![](./figs/ass.png)
        - The author seems to like "ass."
    - The meaning of a word is carried by the surrounding words.
- In other words, the vector value of a word can be determined from the words before and after it in a sentence. (If the hypothesis is correct.)
    - [Mikolov2013] presents two methods for creating distributed representations that utilizes this property.

<center>Let's go through them one by one</center>

---

### Embedding Method 1: Skip-gram

- Prepare an ANN shown on the right.
    - Two affine layers and a softmax layer
- Accepted input: $\boldsymbol{v} = (0\ 0\ \cdots\ 1\ 0\ \cdots\ 0)$
    - For a given word, a one-hot vector with the corresponding element set to $1$
    - Dimensions equal to the number of words
- Vector $\boldsymbol{x}$ between affine layers: Hundreds to Thousands of dimensions
    - <span style="color:red">This becomes the distributed representation</span>
- Output: Vector of the same dimensions as the input
    - Probability corresponding to each word

![bg right:30% 100%](./figs/skip_gram.png)

---

### Skip-gram training

- Given a one-hot vector $\boldsymbol{v}_{w}$ for a given word $w$, learn the probability that another word $\boldsymbol{w}'$ exists within a certain range
- Create training data from a large amount of literature.
- Embedding that reflects the relationships between words is possible.
- <span style="color:red">Each row of $X$ is a distributed representation.</span>
- $X = [\boldsymbol{x}_{w_1}\ \boldsymbol{x}_{w_2}\ \dots\ \boldsymbol{x}_{w_N}]^\top$
- $\boldsymbol{x}_{w_i} = \boldsymbol{v}_{w_i}X$
- Input the one-hot vector $\boldsymbol{v}_{w_i}$ for a given word $w_i$, and you get $\boldsymbol{x}_{w_i}$.

![bg right:35% 100%](./figs/skip_gram.png)

---
### Embedding Method 2: Continuous Bag-of-Words (CBoW)

- Train the ANN shown below as follows:
- Hide a word in a sentence and guess the hidden word from $C$ surrounding words.
- Example: "Tokyo Skytree is the __ tower in Japan." ($C=2$)
$\rightarrow$ Infer "tallest" from "is," "the," "tower," and "in."
- ANN Input/Output
- Input: Average of the one-hot vectors of words within $C$ surrounding words.
- Output: Record the probability that each word is the hidden character.
- Like skip-gram, the dimension is the number of different words.
- Like skip-gram, <span style="color:red">Each row of $X$ corresponds to a vector of latent representations</span>

$\qquad\qquad\qquad\qquad$![w:600](./figs/cbow.png)

---

## Transformer

---

### Can embeddings help computers recognize sentences?

...can't

- Predicting the most likely words using skip-grams and arranging them can create sentences that look like they belong, but they'll probably end up being nonsensical.
- Something like a [Markov chain generator](https://lorem.sabigara.com/?source=ginga-tetsudo&format=plain&sentence_count=5)
- Simple embeddings have limitations
- No complete information about word order
- No context-dependent information
- No distinction between homonyms using a single vector $\rightarrow$
- Example: chinchilla (both rodents and cats)

<center>What should we do? </center>

![bg right:20% 100%](./figs/Chinchilla.jpg)

<span style="font-size:70%">
<a href="https://commons.wikimedia.org/wiki/Chinchilla_lanigera#/media/File:Chinchilla_lanigera_(Wroclaw_zoo)-2.JPG">Top photo by Guérin Nicolas (CC BY-SA 3.0)</a>
<a href="https://commons.wikimedia.org/wiki/File:Chinchilla_cat_(3228221937).jpg">Bottom photo by Allen Watkin (CC BY-SA 2.0)</a>

---

### What should I do?

- Adding word order and context information to the embedding is recommended.
- Adding location information to the latent representation vector.
- Further, <span Considers context using an attention mechanism.
- Transformer, developed in [[Vaswani2017]](https://arxiv.org/abs/1706.03762)
- These mechanisms surpass existing ANNs.
- I will explain the Transformer in detail, starting with an overview and input.

---

### Transformer

- Developed by Google for translation.
- [Let's try it](https://translate.google.co.jp/?hl=ja&sl=en&tl=ja&op=translate)
- What it is: An ANN with the structure shown on the right.
- Consists of an encoder (left) and a decoder (right).
- It has also been applied to images.
- Vision Transformer (ViT)
- Most other new language-related concepts are applications of this.

![bg right:45% 100%](https://upload.wikimedia.org/wikipedia/commons/3/34/Transformer%2C_full_architecture.png)

[<span style="font-size:70%">Image: CC-BY-4.0 by dvgodoy</span>](https://commons.wikimedia.org/wiki/File:Transformer,_full_a
