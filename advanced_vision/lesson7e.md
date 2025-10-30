---
marp: true
---

<!-- footer: "Advanced Vision Lesson 7" -->

# Advanced Vision

## Lesson 7: Applications of Transformer

Ryuichi Ueda, Chiba Institute of Technology

<br />

<span style="font-size:70%">This work is licensed under a </span>[<span style="font-size:70%">Creative Commons Attribution-ShareAlike 4.0 International License</span>](https://creativecommons.org/licenses/by-sa/4.0/).
![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)

---

<!-- paginate: true -->

## Contents

- Supplementary notes from last session
- BERT
- GPT

---

## Layer Normalization

- Normalize the output of a layer
- Method: For each vector $\boldsymbol{x}=(x_1, x_2, \dots, x_d)$ passed,
    - Normalize the vector elements so that their mean is $0$ and variance is $1$.
    - Multiply the $i$th element by $\gamma_i$ and shift it by $\beta_i$.
        - $\gamma_i$ and $\beta_i$ are the parameters to be trained.
- Role
    - Prevent values from becoming extreme.
    - Emphasize or weaken certain elements of the vector (manipulate the degree of attention).
        - Later, we will introduce a mechanism to learn $\gamma_i$ and $\beta_i$ from other information.

![bg right:20% 100%](./figs/layer_normalization.png)

---

## [BERT](https://aclanthology.org/N19-1423/) (Bidirectional Encoder Representations from Transformers) [Devlin2019]

- Model using Transformer encoder
    - Application: Google Search
- BERT<span style="font-size:60%;vertical-align:-5pt">BASE</span> and BERT<span style="font-size:60%;vertical-align:-5pt">LARGE</span>
    - Number of encoders: 12 for the former, 24 for the latter
    - Number of parameters: 110M for the former, 340M for the latter
- Training method (ANN configuration: [Fig. 1 in the original paper](https://aclanthology.org/N19-1423.pdf))
    - Pre-training: Sentence fill-in (masked LM, MLM) and next-sentence prediction tasks simultaneously
        - Wikipedia + 7,000 books
    - Fine-tuning: Tasks tailored to each application

---

### Input format

- In addition to the standard positional embedding, each token is assigned a segment embedding which indicates the sentence position.
    - The latercommer [RoBERTa](https://arxiv.org/abs/1907.11692) does not use segment embeddings.
(It also does not predict the next sentence.)
- Special tokens
    - `[CLS]`: Class token (attached to the beginning)
    - `[SEP]`: Sentence separator
    - `[MASK]`: Mask used to hide tokens during training.

---

### Pre-training

- Masked LM (also known as bidirectional tasks): Use a Transformer encoder to solve a sentence fill-in-the-blank problem.
    - Example: `[CLS]` I went to Doutonbori `[MASK]` bus. `[SEP]`
    - The embeddings output by the encoder are followed by a fully connected layer that outputs the probability of each word. 
    - Occasionally, the system will ask the user to answer using the existing word without masking, or to swap tokens to answer the correct answer.
- Next-Sentence Prediction: Two sentences are connected with a `[sep]` and the user is asked to guess whether they are a continuation or not.
    - 50% of the training data is continuation sentences, and the other 50% is separate sentences.
    - A fully connected layer answers continuity/discontinuity.

---

### How to Use BERT

There are various ways to use BERT, and they are <span style="color:red">fine-tuned</span> to suit the purpose (see [Reference](https://wandb.ai/mukilan/BERT_Sentiment_Analysis/reports/An-Introduction-to-BERT-And-How-To-Use-It--VmlldzoyNTIyOTA1)).

- Classification, Sentiment Analysis
    - Class token output is passed to a classifier.
- Question Answering
    - First, the system reads a sentence containing the answer, then asks a one-word quiz to answer.
        - For questions that require predicting the next word in the quiz.
- Named entity recognition
    - Classifying unknown words into categories such as "person's name," "place name," "organization name," etc.
    - Converting sentences into labels (a rough explanation)

---

### How to use BERT (continued)

- Extractive summarization
    - Extracting important parts from a sentence and summarizing them
    - Example configuration [[Liu2019]](https://aclanthology.org/D19-1387.pdf): Add an encoder on top of BERT, and output a binary value indicating whether to output the sentence in the class token at the beginning of each sentence.
- Abstractive summarization
    - Properly rewriting and summarizing
    - It seems possible, but I'm still investigating.

---
## GPT (Generative Pre-trained Transformer)

- GPT-1
- GPT-2
- GPT-3
    - ChatGPT
- GPT-4

---

### [GPT-1 [Radford2018]](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf)

- Making the Transformer decoder work like BERT
    - (BERT is the encoder)
    - Decoder in this case: A Transformer decoder with masked self-attention, without cross-attention
        - Masked: In other words, pre-training with next-word prediction

[<span style="font-size:70%">Image: CC0 (public domain)</span>](https://commons.wikimedia.org/wiki/File:Full_GPT_architecture.svg)

![bg right:40% 100%](https://upload.wikimedia.org/wikipedia/commons/5/51/Full_GPT_architecture.svg)

---

### GPT-1 Training Method (Pre-training Part 1)

- Pre-training Data: 4.5GB of text from 7,000 unpublished books across various genres ([BookCorpus](https://github.com/soskek/bookcorpus))
- Predict the next word from the unmasked portion
    - As described on the previous page
    - Loss function: $\mathcal{L}(\boldsymbol{\Theta}) = -\sum_i \log P(w_i | w_{{i-k}:{i-1}}, \boldsymbol{\Theta})$
        - $w_i$: Token to predict
        - $w_{i-k:i-1}$: Token used for prediction
        - $k$: Range of past tokens to read (truncation threshold)

---

### GPT-1 Training Method (Pre-training Part 2)

- Adding special tokens: `<s>` at the beginning of a sentence and `<e>` at the end
- Connecting a fully connected layer to the output $\boldsymbol{h}_\text{<e>}$ corresponding to `<e>` to calculate the occurrence probability for all words
    - $P(w_i) =\text{softmax}(W\boldsymbol{h}_\text{<e>})$
    - The idea is that the meaning of the read sentence is summarized in the `<e>` part, like a class token

![bg right:20% 100%](./figs/gpt-1_pt.svg)

---

### GPT-1 Training Method (Fine Tuning)

- Adding a head to the part of the pre-trained decoder corresponding to `<e>` to specialize it for a specific task
    - Problems similar to those handled by BERT (although GPT-1 was developed earlier)
    - Demonstrates high performance (omitted)
        - High performance is important, but the results on the next page are even more significant

---

### Considering use with <span style="color:red">zero-shot</span>

- Use GPT without fine-tuning
- Method used in the GPT-1 paper (example of having the machine answer a multiple-choice quiz)
    - Ask a question and ensure the answer is the last token
    - Compare the probability of occurrence of the answer token and select the one with the highest probability as the answer
- If it outputs sentences instead of just a single token,  perhaps it will be an answer?
    - GPT is essentially a model that continuously produces words.
<span style="color:red">$\Longrightarrow$Continues with GPT-2</span>

---

### [GPT-2 [Radford2019]](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)

- Scaling up GPT-1
    - 10x the number of parameters and training data
    - Collected 45 million links from the internet and acquired 80GB of text
- The paper pursues zero-shot learning
    - Instead of changing the model depending on the task, the task is also input
        - $P($Answer$|$Task$,$Input$)$
        - Example: "Translate into Japanese: This is a pen.", "Summary: (long sentence)"
- Is it possible? $\rightarrow$ Try increasing the parameters and training volume (GPT-1's performance improved with training volume).

---

### GPT-2 Capabilities

- As mentioned before, it receives task instructions such as "◯◯:" as input and responds.
    - It achieves the versatility to complete tasks without fine-tuning.
    - However, fine-tuning may still be necessary for some tasks.
- Table 13 of [[Radford2019]](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) writing fictional articles
- <span style="color:red">The paper suggests there is still room for learning</span>

---

### [GPT-3 [Brown 2020]](https://arxiv.org/abs/2005.14165)

- Enlarge the model and further increase the amount of training
    - 175 billion parameters, use up to 2048 tokens for prediction, and use 300 billion tokens for training
- Addressing computational complexity
    - Sparse attention [[Child2019]](https://arxiv.org/abs/1904.10509)
        - Use alternately with a standard attention mechanism
        - Reduce computational complexity
             - Only tokens in specific positions are considered for calculation.
             - In other words, manual attention.
    - Structured for GPUs.

---

### Questioning Method

- In the paper, questions are input to GPT-3 in the following divided ways:
- Task Description: (e.g., "Translate English to French")
- Example: (e.g., "sea otter => loutre de mer")
- One Example: <span style="color:red">One-Shot</span>
- Several Examples: <span style="color:red">Few-Shot</span>
- Prompt: (e.g., "Answer =>") (In the paper, "cheese =>")
- <span style="color:red">In-Context Learning</span>
- Adjusting the output using examples like the ones above.
- Instead of fine-tuning.
- Weights are not updated (forgotten after solving the problem).

---

### GPT-3 Results

- Able to perform arithmetic operations with a small number of shots
- The output fictitious articles are indistinguishable from those written by humans
- ChatGPT
- A service that uses GPT to answer prompts (human text input)
- "Prompt": A collective term for task descriptions, examples, and prompts
- Fine-tuning is no longer necessary, enabling services to answer a variety of questions
- Performance is expected to improve even with further training

---

### [GPT-4 [OpenAI]](https://arxiv.org/abs/2303.08774)

- The structure has been kept secret due to social impact
- Parameters: Several to several dozen times faster than GPT-3? (Possibilities measured in trillions)
- <span style="color:red">Images can also be input</span>
- Images + text will be discussed next time.

---

### Reinforcement Learning from Human Feedback (RLHF) [[Christiano 2017]](https://proceedings.neurips.cc/paper_files/paper/2017/file/d5e2c0adad503c91f91df240d0cd4e49-Paper.pdf)

- Mechanism introduced in GPT-4 [([Ouyang 2022]?)](https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf)
- Reinforcement learning with human feedback
- RLHF: Since the reward function for generating complex robot movements (cooking, cleaning) is unknown, we designed the reward by having humans compare various movements and score state transitions.
- It seems that people are more likely to score when it's a comparison rather than an absolute evaluation.
- Application to LLM
- Objective: Prevent false, biased, or harmful sentences from being output through human feedback.
- The method is explained on the next page.

---

### Applying RLHF to GPT

The experiments described in the paper were conducted with GPT-3.

- 3 Steps
- Step 1: Select a prompt, have a human (elite team) create responses to create example inputs and outputs, and fine-tune the pre-trained model to reproduce the inputs and outputs.
- Step 2: Humans score several sentences output by the model from Step 1 in response to one prompt. We then changed the head of the model from Step 1 to output reward values, creating a model that outputs the desirability of each sentence as a reward. Learning using human scores as training data
- Step 3: Using the reward model (which functions as a reward function) created in Step 2, reinforcement learning is performed on the model to achieve high-reward outputs.

---

### "Hallucination"

- Suddenly starting to say strange things
- Since words are output one by one,
the conversation may go off track depending on the order of the previous words.
- Have you ever gotten nervous and blurted out something strange during an interview?
- This is a simple anthropomorphization of a probabilistic model, which can lead to misunderstandings, and the paper warns against this.

---

## Summary

- We've looked at applications of the Transformer.
- It's having a major impact (or confusion?) on society.
- The more data and parameters there are, the smarter it becomes.
- If you read all the text ever written on Earth, would it end in a single paragraph? ?
- There are many more applications beyond language.

---

- ​​References
- Yamada et al.: Introduction to Large-Scale Language Models, Gijutsu Hyoronsha, 2023.
- Yohei Kikuta: Unraveling Generative AI from Original Papers, Gijutsu Hyoronsha, 2025.
