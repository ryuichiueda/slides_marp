---
marp: true
---

<!-- footer: "Advanced Vision Session 8" -->

# Advanced Vision

## Session 8: The Integration of Image Processing and Language Processing

Ryuichi Ueda, Chiba Institute of Technology

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## Contents

- Supplement for this session
- Vision Transformer
- Image GPT
- Diffusion Transformer
- CLIP
- DALL·E
- GLIDE
- DALL·E 2 (unCLIP)
- Stable Diffusion

---

## FiLM (Feature-wise Linear Modulation) [[Perez 2017]](https://arxiv.org/abs/1709.07871)

(Additional information for this lesson)

- A mechanism for linearly transforming the output of a layer
    - A linear transformation of $\beta_i$ and $\gamma_i$ without normalization, similar to [Layer Normalization](./lesson7.html#3)
    - Learn $\beta_i$ and $\gamma_i$ from external sources (can also be done using internal information)
- Example structure: Figure 3 in the paper
    - Additional information
        - BN: Batch regularization layer. I didn't do this, though.
        - GRU: Gated Recurrent Unit (can be replaced by a Transformer)

---

- Role: Emphasizes specific elements in the output of each layer and each channel
    - Example: If "blue..." is entered, the output corresponding to blue is emphasized (Figure 4).
    - In practice, it often works to mask unnecessary information (Figure 5).

---

## Vision Transformer (ViT) [[Dosovitskiy 2020]](https://arxiv.org/abs/2010.11929)

- Repurposes the Transformer encoder for images
    - Divides the image into blocks and treats it like words (right image)
    - CLS: Class token (right image)
        - Same as sentence classification
        - Passes through a fully connected layer (MLP Head)
- Treating the image as blocks is the same as CNN, but CNNs are not good at seeing the relationships between distant blocks

[Image: CC-BY-4.0 by Daniel Voigt Godoy](https://commons.wikimedia.org/wiki/File:Vision_Transformer.png)<span style="font-size:60%">(The configuration diagram is also shown in Fig. 1 of [[Dosovitskiy 2020]](https://arxiv.org/abs/2010.11929))</span>

![bg right:25% 100%](https://upload.wikimedia.org/wikipedia/commons/9/93/Vision_Transformer.png)

---

### Size of ViT

- The original paper includes several models of different sizes.
    - ViT-Base: 12 layers, vector dimension: 768, parameters: 86 million
    - ViT-Large: 24 layers, vector dimension: 1024, parameters: 307 million
    - ViT-Huge: Number of layers: 32, Vector dimension: 1280, Number of parameters: 632 million

---

### How to create vectors corresponding to tokens

- Divide the image into blocks of $P \times P$ pixels
    - Example: $P=16$: The vector dimension is $16\times 16 \times 3 = 768$
        - 3 is the number of channels (RGB)
    - Position embedding is also performed
        - Parameters are not fixed values; they are the learning target
- Image understanding
    - Local understanding: into each vector
    - Global understanding: learning with self-attention

---

### Pre-training method

- Solve classification problems with supervised learning
    - Unlike language, unsupervised learning (like BERT) is not very effective
- Training data used in the original paper
    - JFT-300M
        - A dataset with 300 million images and 18,291 classes
    - ImageNet-21k
        - Dataset of 14 million images and 21,841 classes
- High performance with more training data (JFT-300M was better)

---

### How ViT works

- Regarding position embedding
    - Fig. 7 (left) in [[Dosovitskiy 2020]](https://arxiv.org/abs/2010.11929)
    - Similar to basis functions used in image processing
- What is the focus of the decision?
    - Fig. 6 and Fig. 7 (right) in [[Dosovitskiy 2020]](https://arxiv.org/abs/2010.11929)
    - In the head of a self-attention mechanism (or multi-head attention mechanism), variations such as global and local layers already appear in layers close to the input.
        - Global layers are similar to the convolutional layers closer to the input of a CNN.
    - The further away from the input, the more global the results.

---

## Image GPT [[Chen 2020]](https://proceedings.mlr.press/v119/chen20s.html) ([site](https://openai.com/ja-JP/index/image-gpt/)) ([video](https://www.youtube.com/watch?v=7rFLnQdl22c))

- Image version of GPT
    - Uses the GPT-2 structure
    - Number of parameters: $1.36 billion for a model called iGPT-L
- Inputs a partial image and predicts the next pixel
    - Same problem as [PixelCNN](https://ryuichiueda.github.io/slides_marp/advanced_vision/lesson5.html#6)
- Like GPT, adding a head and fine-tuning it can be used for other tasks

---

### Image GPT training

- Two training methods
    - Next pixel prediction (GPT-like)
    - Fill-in-the-blank problem (BERT-style)
- Vector to embedding: Image reduced in resolution and arranged in a single row
    - Site: $32^2$, $48^2$, or $64^2$ pixels
    - Paper: $32^2$, $48^2$, $96^2$, or $192^2$ pixels
        - For $32^2$ or $48^2$, convert the colors from RGB to a color palette (a method used in older computers)
        - For $96^2$ and $192^2$ pixels, compress using VQ-VAE (to $16^2$ and $34^2$ code sequences, respectively)

---
## Diffusion Transformer (DiT) [[Peebles 2022]](https://arxiv.org/abs/2212.09748)

- Diffusion model + Transformer
- Additionally, a latent diffusion model is used to compress information into the latent space
- Input labels to control output ([Classifier-less Guidance](lesson4-2.html#5))
- Structure
- Figure 3 in [[Peebles 2022]](https://arxiv.org/abs/2212.09748)
- Input: Image tokens plus one token consisting of a vector representing the label and a vector representing the time.
- The latter is applied to the image using a mechanism called adaLN-Zero.
- Similar to FiLM with one additional parameter added.
- Output: Mean and variance of noise per pixel.
- Uses VAE to reduce image size.

---
## CLIP (Contrastive Language-Image Pre-training) [[Radford 2021]](https://arxiv.org/abs/2103.00020)

- contrastive: Means "contrasting."
- Links text and images using contrastive learning (explained later).
- [Figure](https://en.wikipedia.org/wiki/Contrastive_Language-Image_Pre-training)
- What CLIP can do
- Recognize what appears in an image (in a sense, there is no limit to the number of labels)
- A component for generating images from text
- unCLIP (covered later)

---

## Background on CLIP

- Steps in a commonly used image recognition method
1. Collect photos
2. Label the objects in the photos
3. Training
- Problems with the above method
- Troublesome
- Only labeled objects can be recognized

<center>Is there any way to collect labeled images? </center>

---

### Collecting images with labels (not captions)

- Some images have captions (that's what the paper says, right?)
$\Longrightarrow$It's possible to collect a large number of images and captions from various sources.
- Original paper: <span style="color:red">Collecting a set of 400 million images and captions</span>
- Problem: Captions are sentences or phrases, not just words.
- It's not a simple label.

<center>Can we use Transformer to solve this problem? </center>

---

### CLIP Training Method

1. Prepare training data using the method on the previous page.
2. Encode images using ViT.
3. Encode sentences using Transformer.
4. Learn the correlation between the encoded data (embeddings).
$\Longrightarrow$ Creates an ANN capable of converting images to sentences, sentences to images, etc.
- Note: ViT and Transformer are not necessarily required (although using Transformer will improve performance).

---

### CLIP Structure

- [Overview](https://en.wikipedia.org/wiki/Contrastive_Language-Image_Pre-training)
- image
