---
marp: true
---

<!-- footer: "Advanced Vision Session 10" -->

# Advanced Vision

## Lesson 10: Integration of Images, Language, and Robot Control II

Ryuichi Ueda, Chiba Institute of Technology

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## What to do today

- Before we get to the main topic
    - Flow matching
    - LoRA (low-rank adaptation)
- VLA (vision-language-action model), robot platform model
    - [Prof. Kawarazuka's slides](https://speakerdeck.com/haraduka/miru2025-tiyutoriarujiang-yan-robotutoji-pan-moderunozui-qian-xian) are also useful references.

---

## Flow matching (FM) [[Lipman 2022]](https://arxiv.org/abs/2210.02747)

- Achieving distribution transformation using a different approach than the diffusion model
- Diffusion model (see below, recap)
    - Transforming the real distribution (actually the training data) to a Gaussian distribution and then back again
        - The transformation involves adding noise.
- FL: <span style="color:red">Can't we just transform the data without adding noise? </span>

![w:900](./figs/ddpm.svg)

---

### Problems with the idea on the previous page

- Unable to generate noise images at any time
    - Right figure (recap)
    - Impediments to learning at each time
- FM solved this problem

![bg right:32% 100%](./figs/ddpm_training_data.png)

---

### Idea of FM 

- Mutual conversion between a Gaussian distribution $p_0$ and a meaningful distribution $p_1$, such as the distribution of an image
    - Consider <span style="color:red">the vector field</span> $\boldsymbol{u}_t$ ($0\le t \le 1$)
        - Assume a velocity field that drives the distribution at each time
    - The ANN learns a function $\boldsymbol{v}_t(\boldsymbol{w})$ that reproduces this vector field.
- The difference (squared error) between $\boldsymbol{v}_t(\boldsymbol{w})$ and $\boldsymbol{u}_t$ is used as the loss function.

---

- The problem is to have the ANN solve the optimal transportation problem.
    - Optimal transportation problem: The problem of transforming the distribution in the easiest way.
$\qquad\qquad$![w:600](./figs/flow_matching_problem.svg)

---

### Problem Decomposition: Conditional Flow Matching

- Like the diffusion model, intermediate images (or data) of $t$ are required.
    - Considering the entire distribution is difficult.
- Decomposing $p_t$ into conditional probabilities.
    - $p_t(\boldsymbol{x}) = \int_{X_1} p_t(\boldsymbol{x} | \boldsymbol{x}_1)q(\boldsymbol{x}_1) \text{d}\boldsymbol{x}_1$
        - $q$: Distribution of the training data
            - Subscript of $\boldsymbol{x}_1$: Time, not the data number
            - <span style="color:red">The overall loss function can be minimized even by minimizing the loss function for each training data point</span>

![bg right:27% 95%](./figs/flow_matching_method.svg)

---

- Vector field $\boldsymbol{u}_t$ can also be calculated (weighted average)
- $\boldsymbol{u}_t(\boldsymbol{x}) = \int_{X_1} \boldsymbol{u}_t(\boldsymbol{x}|\boldsymbol{x}_1) \dfrac{p_t(\boldsymbol{x} | \boldsymbol{x}_1)q(\boldsymbol{x}_1)}{p_t(\boldsymbol{x})} \text{d}\boldsymbol{x}_1$

![bg right:27% 95%](./figs/flow_matching_method.svg)

---

### Flow Design

- For each conditional probability, the intermediate path (distribution) must be formulated.

![bg right:27% 95%](./figs/conditional_flow.svg)

---

- For now, we will select the Gaussian distribution.
    - $p_t(\boldsymbol{x}|\boldsymbol{x}_1) = \mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}_t(\boldsymbol{x}_1), \sigma_t(\boldsymbol{x}_1)^2I)$
        - Boundary Conditions
            - $\boldsymbol{\mu}_0(\boldsymbol{x}_1) = \boldsymbol{0}, \sigma_0(\boldsymbol{x}_1) = 1$
            - $\boldsymbol{\mu}_1(\boldsymbol{x}_1) = \boldsymbol{x}_1, \sigma_1(\boldsymbol{x}_1) = \sigma_\text{min}$
    - The flow is: $\boldsymbol{\psi}_t(\boldsymbol{x}) = \sigma_t(\boldsymbol{x}_1)\boldsymbol{x} + \boldsymbol{\mu}_t(\boldsymbol{x}_1)$
        - At $t=0$, $\boldsymbol{x}$ at various points moves toward $\boldsymbol{x}_1$ (right).
        - The shapes of $\sigma_t(\boldsymbol{x}_1)$ and $\boldsymbol{\mu}_t(\boldsymbol{x}_1)$ have not yet been determined.
            - Note: Both are functions of time, not $\boldsymbol{x}_1$.

![bg right:27% 95%](./figs/conditional_flow.svg)

---

### Design using optimal transportation

- We want to transfer distribution using the most straightforward flow, as shown in this diagram. $\Longrightarrow$ The optimal transportation problem, 
![w:400](./figs/conditional_flow.svg)
- Conditional optimal transportation path
    - Flow: $\boldsymbol{\psi}_t(\boldsymbol{x}) = \{1 - ( 1 - \sigma_\min)t\}\boldsymbol{x} + t \boldsymbol{x}_1$
        - $\boldsymbol{\mu}_t(\boldsymbol{x}_1)=t \boldsymbol{x}_1, \sigma_t(\boldsymbol{x}_1)=1 - (1- \sigma_\text{min})t$
- Vector field at this time
    - $\boldsymbol{u}_t(\boldsymbol{x}|\boldsymbol{x}_1) = \dfrac{\sigma_t'(\boldsymbol{x}_1)}{\sigma_t(\boldsymbol{x}_1)}\{ \boldsymbol{x} - \boldsymbol{\mu}_t(\boldsymbol{x}_1) \} + \boldsymbol{\mu}_t'(\boldsymbol{x}_1) = \dfrac{\boldsymbol{x}_1 - (1-\sigma_\min)\boldsymbol{x}}{1-(1-\sigma_\min)t}$
- loss function
    - $\mathcal{L}_\text{CFM}(\boldsymbol{w}) = \big\langle \{ \boldsymbol{v}_t(\boldsymbol{\psi}_t(\boldsymbol{x}_0)) - [ \boldsymbol{x}_1 - (1 - \sigma_\min)\boldsymbol{x}_0 ] \}^2 \big\rangle_{t \sim \mathcal{U},q(\boldsymbol{x}_1), p(\boldsymbol{x}_0 )}$

---

### What FM can do

- Figures 1, 6, and 11 in [[Lipman 2022]](https://arxiv.org/abs/2210.02747)
    - Figure 4 is also interesting, even though it is used to explain the algorithm.
- Stable Diffusion 3
- Robot Control (We will cover this later in this article)
- Supplementary Information
    - We have only discussed the case of optimal transportation, but there is room for other design possibilities.

---

## Low-Rank Adaptation (LoRA) [[Hu2021]](https://arxiv.org/abs/2106.09685)

- Highly efficient fine-tuning method
- Idea (commonly called an <span style="color:red">adapter</span>)
    - Fixing pre-trained matrix parameters
    - Preparing a fine-tuning model next to it and calculating only the parameter differences
        - Fewer parameters than the model below
            - The computational complexity of backpropagation is reduced.
        - See the next page for how to reduce it.

![bg right:32% 100%](./figs/LoRA.svg)

---

### Parameter Reduction Method

- For the pre-trained $\alpha \times \beta$ matrix $W$,
prepare the following matrix:
    - Matrix $A$ ($d\times \beta$)
    - Matrix $B$ ($\alpha \times d$)
- Fine-tuned matrix: $W' = W + BA$
    - Number of parameters in $W$: $\alpha \beta$
    - Number of parameters in $BA$: $(\alpha + \beta)d$
         - Reduce the number of parameters with a small $d$

![bg right:40% 100%](./figs/lora_matrixes.svg)

---

- The input dimensionality is reduced in $A$ and restored in $B$
    - Similar to dimensionality reduction using latent space

![bg right:40% 100%](./figs/lora_matrixes.svg)

---

### Robotics Transformer 2 (RT-2) [[Brohan2023]](https://arxiv.org/abs/2307.15818) ([Site](https://robotics-transformer2.github.io/))

- Abstract of this paper: "We refer to such a category of models as vision-language-action models (VLA) and ...," which is where the term VLA appears.
- Structure (there are two types)
    - PaLI with various additions (RT-2-PaLI-X)
    - PaLM-E-based (RT-2-PaLM-E)
        - From here on, I will assume the use of PaLM-E.
        - A model that turns anything into a token and then speaks tokens.

<center style="padding-top:2em">If that's the case, what's the difference between PaLM-E and RT-2? </center>

---

### Differences from PaLM-E (Why it's called VLA)

- It also learns robot behavior
(not at the language level, but at the <span style="color:red">numerical level</span>)
    - Numerical level: things like joint rotation angles and movement amounts
        - Example: The training data pair in Figure 1 of the paper (the bottom one)
            - Q: What should the robot do to `<task>`?
            - A: Displacement: $(0.1, -0.2, 0)$, Rotation: $(10^\degree, 25^\degree, -7^\degree)$
- Unlike PaLM-E, it can directly output robot behavior.
    - Considering the control layer, it's reasonable to consider it a successor to RT-1.

---

### OpenVLA[[Kim2024]](https://arxiv.org/abs/2406.09246)

- As the name suggests, this VLA is open.
- Requirements for making it open.
    - Since users' robots vary, it is useful to facilitate fine-tuning.
$\Longrightarrow$<span style="color:red">LoRA is now available.</span>
        - (Note: A VLA trained on training data from a variety of robots can absorb minor differences between robots to some extent, even without fine-tuning.)

---

### Structure (Figure 2 in [[Paper]](https://arxiv.org/abs/2406.09246))

- Image processing: Tokens are generated independently from two models, SigLIP and DINOv2.
    - SigLIP[[Zhai2023]](https://arxiv.org/abs/2303.15343): A zero-shot image classification model.
        - Instead of classifying objects from a large number of objects using softmax, it outputs a probability of matching between the image and a short sentence.
        - Tokens represent what is in the image.
    - DINOv2[[Oquab2023]](https://arxiv.org/abs/2304.07193): Image foundation model
        - Extract image features and convert them into tokens

---

- LLM part: Llama (Large Language Model Meta AI)
    - Output tokens to be input into the Action De-tokenizer below
- Action generation: "Action De-tokenizer" (The implementation is unclear. Should we read the code?)

---

### Training data and training method

- Pre-training training data: Open X-Embodiment dataset
    - Trajectories of 70 robots, 2 million robots
- Fine tuning
    - Training data is provided by the user
    - As mentioned above, LoRA can be used

---

### $\pi_0$[[Black 2024]](https://arxiv.org/html/2410.24164v1) ([site](https://www.physicalintelligence.company/blog/pi0))

- VLA model developed by Physical Intelligence
- Simultaneous training of data from a wide variety of robots, including single-arm, dual-arm, and mobile manipulators
    - Original dataset of 68 tasks and the Open X-Embodiment dataset
        - Each dataset contains data from 7 and 22 robots
        - Over 10,000 hours of training
- Achieves a 50Hz control cycle using the action chunking architecture used in ACT
    - However, it uses conditional flow matching (CFM) instead of CVAE
- Usage examples: See the above site for various examples
    - Achieves complex and detailed movements, such as removing laundry from the washing machine and folding it

---

### Structure (Figure 3 on [this page](https://arxiv.org/html/2410.24164v3))

- PaliGemma
    - Open, lightweight Google VLM (3 billion parameters)
    - Input: Image and task instructions
    - Output: Token
- Action expert
    - Outputs robot action sequences (300 million parameters)
    - Input: Tokens from PaliGemma and robot state
    - Output: Action sequences
        - <span style="color:red">Flow Matching</span>

---

### How to use Flow Matching

- Training by incorporating observational data into the vector field variables created by the neural network
    - Loss function: $\mathcal{L}_\text{CFM}(\boldsymbol{w}) = \big\langle \{ \boldsymbol{v}_{\boldsymbol{w}}(A_t^\tau,\boldsymbol{o}_t) - \boldsymbol{u}(A_t^\tau | A_t) \}^2 \big\rangle_{q(A_t^\tau | A_t), p(A_t | \boldsymbol{o}_t ), \tau \sim \text{Beta}}$
        - $\tau$ is the FM time ($0 \le \tau \le 1$)
            - $t$ is the actual time (the robot's movement step)
            - We want to emphasize the loss function when $\tau$ is small
                 $\rightarrow$ We evaluate using a weighted average biased by the beta distribution
        - $A_t$ (the movement sequence at time $t$) is the training data
             - It is paired with observations or instructions $\boldsymbol{o}_t$
        - $q(A_t^\tau | A_t ) = \mathcal{N}[\tau A_t, (1-\tau)I]$ (optimal transportation path)

---

- During use (inference)
    - When noise is introduced into $A_t^0$, $A_t^1$ is generated, guided by $\boldsymbol{v}_\boldsymbol{w}$ conditioned on $\boldsymbol{o}_t$.

---

## Summary

- The VLA has been developed.
- Over the past few years, robots have become capable of understanding human instructions.
- They can even perform highly detailed tasks.
- Tasks that are currently out of reach will eventually be possible.
- Future
- Take another look at your research topic.
- Consider what you want to solve with robots, and whether they are unsolved.
