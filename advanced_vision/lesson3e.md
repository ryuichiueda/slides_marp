---
marp: true
---

<!-- footer: "Advanced Vision Session 3" -->

# Advice on Vision

## Lesson 3: Fundamentals of Image Classification and Generation I

Ryuichi Ueda, Chiba Institute of Technology

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## Contents

- CNN
- U-Net
- Autoencoder

---

## Before we get to that, a follow-up question:

- Problem: How can we mathematically describe an artificial neural network that can distinguish between dogs and cats (and other things) in digital images?
    - Considering an artificial neural network as a function
    - How do we express the inputs, outputs, and parameters?

![bg right:30% 100%](./figs/cat_and_dog.svg)

---

### Example Answer 1

- $y = f(\boldsymbol{x} | \boldsymbol{w})$
    - $\boldsymbol{x}$: A vector of pixel values (highly multidimensional)
        - Dimensions: Number of vertical pixels $\times$ Number of horizontal pixels $\times$ Color channels (RGB: 3, RGBD: 4)
    - $y = 0$: Dog, $y=1$: Cat, $y=2$: Other
        - $\boldsymbol{w}$: A vector of parameters (also multidimensional)
        - Sometimes written as $y = f_\boldsymbol{w}(\boldsymbol{x})$ (in ANN circles)
       - It can also be written as $y = f(\boldsymbol{x} ; \boldsymbol{w})$ (traditional).

Problem: Integer values like $0, 1, 2$ can't be output from the end of a neural network.

---

### Example Answer 2

- $\boldsymbol{y} = \boldsymbol{f}(\boldsymbol{x} | \boldsymbol{w})$
    - $\boldsymbol{x}$ and $\boldsymbol{w}$: Same
    - $\boldsymbol{y} = (1$ if cat,1 if dog, 1 otherwise$)$
        - Since only one element is 1, it's called a "<span style="color:red">one-hot vector</span>."

![bg right:30% 100%](./figs/one_hot.svg)

Question: Is it okay to be definitive when it's subtle?

---

### Example Answer 3

- $\boldsymbol{y} = \boldsymbol{f}(\boldsymbol{x} | \boldsymbol{w})$
    - $\boldsymbol{x}$ and $\boldsymbol{w}$ are the same
    - $\boldsymbol{y} = (P_\text{cat}, P_\text{dog}, P_\text{other})$
        - $\boldsymbol{y}$ is a probability distribution
- This format is commonly used for the output of ANNs for classification
    - To settle on one, select the one with the highest probability

![bg right:30% 100%](./figs/prob_output.svg)

---

## Another Question

- What should the loss function be during training?
    - Consider Example 3 on the previous page.
    - Output: $\boldsymbol{y} = (\hat{P}_1, \hat{P}_2, \dots, \hat{P}_N)$
    - Correct answer: $\boldsymbol{y}^* = (P_1, P_2, \dots, P_N)$
        - The correct answer is often a one-hot vector with the correct element $=1$.

![bg right:30% 100%](./figs/prob_output.svg)

---

### Common answer

- Use <span style="color:red">cross entropy</span>
    - $\mathcal{L}(\boldsymbol{w}) = H(\boldsymbol{y}^*, \boldsymbol{y}) = -\sum_{i=1}^N P_i \log \hat{P}_i$
        - $\log$ is the natural logarithm (base $e$)
    - A side note for math buffs: This is equivalent to minimizing the Kullback-Leibler divergence.
- Let's calculate the probability of the correct answer when it's high (e.g., $0.9$) and low (e.g., $0.1$).
    - Answer omitted.
- The essence of ANN learning is adjusting $\boldsymbol{w}$ so that the value of $\mathcal{L}$ (loss) approaches $0$.

![bg right:30% 100%](./figs/prob_output.svg)

---

### A topic we've touched on before.

- How do animals convert their vision into information needed for action and decision-making?
- Can this be replicated on a computer?

![w:400](./figs/Retina-diagram.svg.png)<span style="font-size:40%">(https://commons.wikimedia.org/wiki/File:Retina-diagram.svg, by S. R. Y. Cajal and Chrkl, CC-BY-SA 3.0)</span>

Can this be done with artificial neural networks (ANNs)? $\rightarrow$ Yes.

---

### Another topic: Someone has appeared that can automatically draw pictures.

- Examples are everywhere, so please do your own research.
- How do they work?

---

## Vision, Images, and ANNs (CNNs)

- ANNs specialize in images and video.
    - Image Characteristics
        - 2-D (3-D with depth, and 3-D with video if a time axis is added).
        - Similar pixels are present around a certain pixel.
- Recap: Digital Images
    - A plane is divided into a grid, and the color intensity is represented by the number. (e.g. right figure)
    - In the case of color images, the data is a grid of numerical data for R, G, and B.

![bg right:25% 90%](./figs/cat_mono.png)

---

### The Difficulty of Image Recognition

- The same object may appear enlarged, small, or rotated.
- It may be deformed, abstracted, or distorted.

![](./figs/dots_varisous.png)

![bg right:30% 90%](./figs/cat_back.png)

---

### CNN (Convolutional Neural Network)

- This is not a TV station.
- It uses many neurons that input and output pixel values ​​from nearby areas of the image (right image).
    - Nearby areas of the image: a square region of $n\times n$ pixels.
    - It outputs pixel characteristics and changes in the small region.
    - Further convolutions are used in lower layers to capture overall features.
- It recognizes images using a combination of "convolutional layers" and other layers.

![bg right:30% 90%](./figs/convolution_neuron.png)

---
### CNN component 1: Convolutional layer

- Apply a <span style="color:red">filter</span> to a portion of the image (a "window" of n$\times$n pixels), add the output, replace it with a single value, and send it downstream (upper right).
- Apply the filter by shifting it one pixel at a time (lower right). $\rightarrow$ Downstream also applies to the image.
    - To maintain the number of downstream pixels $\rightarrow$ pad the edges
    - Shifting by more than two pixels is also possible (the amount of shift is called the stride).

![bg right:20% 90%](./figs/cnn_conv.png)

---

- Convolution operation (lower).
    - $\odot$: Hadamard product (element-wise multiplication).

$\qquad\qquad$![w:660](./figs/cnn_calc.png)

---

### Meaning of Filter

- Filter: Same as those used in traditional image processing
    - Detect local features (edges, etc.)
    - Convolutional layer training = Filter training
![w:700](./figs/cnn_filter.png)

---

### Filter calculation formula

- $y = \sum_{i=1}^n\sum_{j=1}^n w_{(i,j)}x_{(i,j)} + b$
    - $(i,j)$: Pixel position in the filter coordinate system
    - $x_{(i,j)}$: Pixel value
    - $w_{(i,j)}$: Weight (<span style="color:red">Learning target</span>)
    - $b$: Bias (<span style="color:red">Learning target</span>)
        - Previously, it was $-b$, but it's the same thing.
- It's the same as before, just in 2D.
    - However, it's not "fully connected."
    - An affine layer (plus activation function layer) is sometimes called a "fully connected layer."

---

### CNN Component 2: Pooling Layer (Subsampling Layer)

- A layer that reduces the number of pixels within a window, retaining only the most distinctive pixels.
- "Max pooling," which retains the maximum value, is mainly used.
- No learning is performed.
- The reduced number of pixels makes it easier for the subsequent stage (the object classification network) to learn.
- It becomes slightly more tolerant to misalignment of the objects in the image.
- CNNs do not fully address the "difficulties" mentioned at the beginning, so images of various sizes, positions, and orientations are used for training.

![bg right:23% 90%](./figs/cnn_pooling.png)

---

### CNN Component 3: Softmax Layer
(Note: This layer is also used in applications other than CNNs.)

- Softmax (soft maximum): Not settling on a single answer
- Example: Identifying objects in an image
- Outputting a probability without a definitive answer (e.g., 90% dog, 9% cat, 1% other)
- Because the real world is full of ambiguous situations, it is more convenient to output an ambiguous answer without a single answer.
- Mathematical formula
- For input $\boldsymbol{x} = (x_1, x_2, \dots, x_n)$, output <span style="color:red">$y_i = \eta e^{x_i}$</span>
- $\eta$ is a normalization constant

![bg right:20% 95%](./figs/softmax_layer.png)

---

### Channels

- When working with color (RGB) images
