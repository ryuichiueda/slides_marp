---
marp: true
---

<!-- footer: "Advanced Vision Lesson 8" -->

# Advanced Vision

## Lesson 8: The Integration of Image Processing and Language Processing

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
    - Input labels to control output ([Classifier-free Guidance](lesson4-2.html#5))
- Structure: Figure 3 in [[Peebles 2022]](https://arxiv.org/abs/2212.09748)
    - Input: Image tokens plus one token consisting of a vector representing the label and a vector representing the time.
        - The latter is applied to the image using a mechanism called adaLN-Zero.
            - Similar to FiLM with one additional parameter added.
        - Output: Mean and variance of noise per pixel.
    - Uses VAE to reduce image size.

---
## CLIP (Contrastive Language-Image Pre-training) [[Radford 2021]](https://arxiv.org/abs/2103.00020)

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
    - Bothersome
    - Only labeled objects can be recognized

<center>Is there any way to collect labeled images? </center>

---

### Collecting images with labels (not captions)

- Some images have captions (e.g. academic papers)
$\Longrightarrow$It's possible to collect a large number of images and captions from various sources.
    - Original paper: <span style="color:red">Collecting a set of 400 million images and captions</span>
- Problem: Captions are sentences or phrases, not just words.
    - It's not a simple label.

<center>Can we use Transformer to solve this problem? </center>

---

### Training Method of CLIP 

1. Prepare training data using the method on the previous page.
2. Encode images using ViT.
3. Encode sentences using Transformer.
4. Learn the correlation between the encoded data (embeddings).
$\Longrightarrow$ Creates an ANN capable of converting images to sentences, sentences to images, etc.
- Note: ViT and Transformer are not necessarily required (although using Transformer will improve performance).

---
### CLIP Structure

- [Overview](https://en.wikipedia.org/wiki/Contrastive_Language-Image_Pre-training)
- Image Encoder: ViT
    - Input: Image
    - Class tokens are used as output (vectors with $n \times 100$ dimensions)
- Text Encoder: Transformer decoder minus cross-attention
    - Input: Image captions
    - <span style="color:red">Align output with image encoder</span>
- Mathematically important point: <span style="color:red">Multimodal</span>
    - Outputs of the text encoder and image encoder are plotted in the same latent space
        - Captions (sentences, phrases) and images are placed in the same space, with similar ones being placed close together

---

### Evaluation Method (Contrastive Learning)

- $N$ pairs (batches) of images and captions are input to the encoder
    - Output of the image encoder: Vector $\boldsymbol{i}_1, \boldsymbol{i}_2, \dots, \boldsymbol{i}_N$
    - Text encoder output: Vector $\boldsymbol{t}_1, \boldsymbol{t}_2, \dots, \boldsymbol{t}_N$
- I want the vectors of paired images and captions to be the same.
- I want to increase the cosine similarity between $\boldsymbol{i}_j$ and $\boldsymbol{t}_j$.
- Cosine similarity: $\boldsymbol{i}_j\cdot \boldsymbol{t}_j/(|\boldsymbol{i}_j| |\boldsymbol{t}_j|)$
- I want the vectors of unpaired images and captions to be different.
- I want to decrease the cosine similarity between $\boldsymbol{i}_j$ and $\boldsymbol{t}_k (i\neq k)$.
- $\Rightarrow$ loss function: $\mathcal{L} = -\dfrac{1}{N} \sum_{j=1}^N \ln\mu_{j,k}
e^{\boldsymbol{i}_j\cdot\boldsymbol{t}_j /T}
-\dfrac{1}{N} \sum_{k=1}^N \ln\mu_{j,k}
e^{\boldsymbol{i}_k\cdot\boldsymbol{t}_k /T}$
- $\mu(j,k) = (\sum_{k=1}^N e^{\boldsymbol{i}_j\cdot\boldsymbol{t}_k /T})^{-1}$
- $T$ is the "temperature" and is decreased as training progresses.

---

### How to use the trained model

- Example: Image classification
- Prepare $N$ labels for the objects you want to classify.
- "a photo of Generate $N$ phrases, each with the same label, and run them through a text encoder to obtain a feature vector $T_{1:N}$.
- Run the image through an image encoder to obtain a feature vector $I$.
- Compare $I$ with $T_i (i=1,2,\dots,N)$ and select $T_i$ with the highest cosine similarity.

---

## DALL·E (Dali) [[Ramesh 2021]](https://arxiv.org/abs/2102.12092)

- Generate images from phrases or sentences.
- Figures 2 and 8 in [[Ramesh 2021]](https://arxiv.org/abs/2102.12092)
- https://openai.com/ja-JP/index/dall-e/
- Have the Transformer consider images as a continuation of a sentence.
- What you'll need
- Transformer (decoder)
- A modified version of GPT-3
- Images can also be input as embedding vectors
- [VQ-VAE](https://ryuichiueda.github.io/slides_marp/advanced_vision/lesson5.html#8) (The paper calls it [discrete VAE (dVAE)](https://ryuichiueda.github.io/slides_marp/advanced_vision/lesson5.html#3))
- Encodes $256 × 256$ images into $32 × 32$ images (or rather, code sequences)

---
### Training DALL·E

- Caption-image pairs are used as training data
- Same as CLIP
- Stage 1: Train dVAE using collected images
- Inputting a [code string](https://ryuichiueda.github.io/slides_marp/advanced_vision/lesson5.html#6) to a trained decoder generates an image.
- Stage 2: Train a transformer to generate a code string after the input sentence.

![bg right:45% 100%](./figs/dall-e.svg)

---

### Image Generation with DALL·E

- Stage 2 configuration on the previous page
- Website: https://openai.com/ja-JP/index/dall-e/
- Generate 512 images, rank them using CLIP, and output the top 32.
- Let's play around.

---
## GLIDE[[Nichol 2021]](https://arxiv.org/abs/2112.10741)

- Acronym for Guided Language to Image Diffusion for generation and editing.
- Poor generation
- "A Diffusion Model for Language-Guided Image Generation and Editing"
- Using natural language and [classifier-less guidance] (lesson4-2.html#5) to generate images using a diffusion model
- (Other methods, such as CLIP guidance, were also tried, but the classifier-less approach produced better results.)
- Encoding natural language is used as labels for classifier-less guidance
- U-Net structure
- Generated image: Figure 1 in the paper
- Fine-tuning allows for partial image modification with text (image inpainting): Figures 2, 3, and 4 in the paper

---
## DALL·E 2 ([Official Video](https://www.youtube.com/watch?v=qTgPSKKjfVg))

- Successor to DALL·E
- Basic idea
- Uses CLIP
- Since text and images are in the same latent space,
text can also be converted to images using the latent space vector $\rightarrow$image
- However, various efforts were made to output a well-defined image.

---

### Structure

- Above the dotted line: CLIP (used for training)
- Below the dotted line: Generation
- Consists of a prior model (prior) and a decoder (almost entirely GLIDE)

<span style="font-size:70%">[Image: CC-BY-4.0 by Ramesh et al.](https://www.researchgate.net/figure/A-high-level-overview-of-unCLIP-Above-the-dotted-line-we-depict-the-CLIP-training_fig2_359936873)</span>
![](./figs/unclip.png)

---

### Prior model + decoder (unCLIP[[Ramesh 2022]](https://arxiv.org/abs/2204.06125))

- Redundant problem of estimating (generating) image $\boldsymbol{x}$ from text $\boldsymbol{y}$ 
- $p(\boldsymbol{x}|\boldsymbol{y}) = p(\boldsymbol{x}, \boldsymbol{z}_x | \boldsymbol{y}) = p(\boldsymbol{x} | \boldsymbol{z}_x, \boldsymbol{y})p(\boldsymbol{z}_x | \boldsymbol{y}) = p(\boldsymbol{x} | \boldsymbol{z}_x, \boldsymbol{y})p(\boldsymbol{z}_x | \boldsymbol{y}, \boldsymbol{z}_y)$ 
- $\boldsymbol{z}_x, \boldsymbol{z}_y$: Feature vectors for image and text in CLIP, respectively.
- Mathematically redundant, but with additional hints during training, quality improves.
- Last term: $p(\boldsymbol{x} | \boldsymbol{z}_x, \boldsymbol{y})p(\boldsymbol{z}_x | \boldsymbol{y}, \boldsymbol{z}_y)$
- Backward probability distribution: Prior model
- Outputs high-quality image feature vectors.
- Rather than simply outputting text feature vectors, this is enhanced by inputting text as well.
- Forward probability distribution: Decoder
- This also inputs text again.

---

### Stable Diffusion

- Service website: https://stablediffusionweb.com/ja
- Rival of the DALL·E series
- Easy to use and rapidly gaining popularity
- 5 billion images used for training

---

### Stable Diffusion (v1) structure (Latent Diffusion) Models, LDM) [[Rombach 2021]](https://arxiv.org/abs/2112.10752)

- Figure 3 in [[Rombach 2021]](https://arxiv.org/abs/2112.10752) (Figure from Wikipedia)
- The upper $x\rightarrow\varepsilon\rightarrow z\rightarrow$Diffusion Process$\rightarrow z_T$ section is for training.
- The training images are converted into vectors in the latent space and then diffused using DDPM.
- Latent space: From the VQGAN proposed in [[Esser 2020]](https://arxiv.org/abs/2012.09841)
- In essence, it's the GAN version of VQ-VAE.
-
