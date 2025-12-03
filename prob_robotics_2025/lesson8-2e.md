---
marp: true
---

<!-- footer: Probabilistic Robotics Lesson 8 -->

# Probabilistic Robotics Lesson 8: Machine Learning (Part 2)

Ryuichi Ueda, Chiba Institute of Technology

<br />

<p style="font-size:50%">
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
</p>

---

<!-- paginate: true -->

## Contents

- Clustering
- EM Method
- Variational Inference

---

## The Importance of Clustering

- Review of the advanced vision
   - What do You see in the image on the right?
   - Why does it look like a cat?
- Probably grouping dots into one circle and two triangles (clustering).
   - [Research Example](https://www.riken.jp/medialibrary/riken/pr/press/2001/20010727_1/20010727_1.pdf)

![bg right:40% 60%](./figs/dots.png)

---

### What can we recognize by summarizing?

- For example, if you want to know what is in front of you, what needs to be done?
   - Photoreceptor cell response$\longrightarrow$Object to recognize (e.g., cat)
   - Numerous stimuli$\longrightarrow$The single word "cat"
   - <span style="color:red">The brain needs to "reduce"</span>
       - <span style="color:red">Reduce = Summarize to a representative value (feature)</span>

![bg right:30% 78%](./figs/leaf_stem.png)

---

- Left image: Image of actual crops in a field, with stems and leaves classified.
    - For robotics
    - The various colors have been reduced to three.
    - Humans can (with time) produce classification results like the one on the right.

![bg right:30% 78%](./figs/leaf_stem.png)

---

### Classical Clustering Methods

- Used in the field of robotics for 30 years.
    - k-means algorithm
    - EM algorithm
- Problem to solve
    - Determine which points belong to the same group when points are scattered.

![bg right:30% 78%](./figs/clustering_problem.png)

---

## k-means algorithm

- Divide the data into appropriate clusters and converge by repeating the following steps.
    - Find the center of each cluster (denoted by the $\times$ symbol in the figure).
    - Re-cluster each data set based on the nearest cluster center.

![](./figs/k-means.png)

---

## Clustering numbers using k-means

- Divide the following nine numbers into three clusters:
    - (8, 1, 3), (5, 5, 2), (6, 11, 7)
        - The brackets indicate the initial classifications, which were randomly chosen.
    - The answer is on the next page.
- Note
    - If the mean values are the same, select the cluster randomly.
    - If there are two or more close mean values for a given data set (if they are the same distance), change the original class.

---

### Answer

- Initial values: (8, 1, 3), (5, 5, 2), (6, 11, 7) $\rightarrow$ Cluster means: 4, 4, 8
- Rearrangement: (1, 5, 2), (3, 5), (8, 6, 11, 7) $\rightarrow$ Cluster means: 2.666..., 4, 8
- Rearrangement: (1, 2, 3), (5, 5), (8, 6, 11, 7) $\rightarrow$ Cluster means: 2, 5, 8
- Rearrangement: (1, 2, 3), (5, 5, 6), (8, 7, 11) $\rightarrow$ Cluster means: 2, 5.333..., 8.666...
- Rearrangement: (1, 2, 3), (5, 5, 6, 7), (8, 11) $\rightarrow$ Cluster means: 2, 5.75, 9.5
- Rearrangement: (1, 2, 3), (5, 5, 6, 7), (8, 11) (No change. End)

---

### Problems of the k-means algorithm

- Is it okay to determine the number of clusters from the beginning?
    - This is particularly problematic when programming sensors or robots.
        - For example, we want to know how many people are in an image. It's rare to know from the beginning that there are three people.
- What if the clusters are distorted?
    - In this case, you can either transform the data to eliminate the distorted data or use another method (such as a support vector machine).
- A more fundamental problem: You're not considering why the data is generated (i.e., ad hoc).

---

### EM Method (Maximum Likelihood Method)

- EM: Expectation Maximization
(We'll explain what this means later.)
<br />
- Consider a model (mathematical formula) of a certain probability distribution and find the parameters that best explain the data.
    - Why did the data shown on the right come about?
$\rightarrow$ Imagine that there are several sources of data,
and that data is generated around them.

![bg right:28% 95%](./figs/clustering_reason.png)

---

### "There are several sources of data,<br />and that data is generated around them."

The basic model in this case: <span style="color:red">Gaussian Mixture Distribution</span>

- Addition of multiple Gaussian distributions
and normalization (integration to 1)
    - $p(\boldsymbol{x} | \boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}) = \pi_1 \mathcal{N}(\boldsymbol{\mu}_1, \Sigma_1)$
$\qquad+ \pi_2 \mathcal{N}(\boldsymbol{\mu}_2, \Sigma_2) + \dots + \pi_n \mathcal{N}(\boldsymbol{\mu}_n, \Sigma_n)$
    - $\pi_1 + \pi_2 + \dots + \pi_n = 1$
(Note: This is the <span style="color:red">mixture ratio</span>, not pi.)
- This can be illustrated as shown on the right.
(The fit is a bit poor.)

![bg right:30% 100%](./figs/gauss_mix.png)

---

### "Most Likely Distribution" for Data

- The distribution that maximizes the following likelihood is considered "most likely."
    - $p(\boldsymbol{x}_{1:N} | \boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}) = \prod_{j=1}^N p(\boldsymbol{x}_j | \boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n})$
        - Left-hand side: The probability density generated by the data $\boldsymbol{x}_{1:N}$
        - Right-hand side: Multiplying the density of each data point $\boldsymbol{x}_i$
        - <span style="color:red">Since the data is known, the problem is to find the most likely (maximum likelihood) parameters $\boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}$ and their likelihood</span>
    - Specifically,
        - Left-hand side $= \prod_{j=1}^N \sum_{i=1}^n \pi_i \mathcal{N}(\boldsymbol{x}_j | \boldsymbol{\mu}_i, \Sigma_i)$

---

- Taking the logarithm, we turn multiplication into addition, making the problem the one of maximizing the <span style="color:red">log-likelihood</span>
    - $\log_e p(\boldsymbol{x}_{1:N} | \boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}) = \sum_{j=1}^N \log_e p(\boldsymbol{x}_j | \boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n})$
- Making the problem equivalent and simpler

---

### Finding parameters that maximize the log-likelihood (similar to the k-means method)

1. First, perform appropriate clustering
2. M-step (maximization step)
    - Calculate $\boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}$ for each cluster that maximizes the likelihood
3. E-step (expectation step)
    - Cluster the data based on $\boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}$
        - Calculate the <span style="color:red">probability</span> that each data point belongs to a cluster at that time.

![](./figs/em.png)

---

### Step E

- For each data point $\boldsymbol{x}_i$, we want to determine the probability of it belonging to which cluster.
    - The Gaussian mixture parameters $\boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}$ are fixed.
    - Unlike k-means, we do not determine that it belongs to a single cluster.
        - <span style="color:red">We leave it vague because we don't know</span>
- Mathematically,
   - We want to find the probability that cluster $k_i$, to which $\boldsymbol{x}_i$ belongs, is the j$th cluster. $\text{Pr}\{ k_i = j |\boldsymbol{x}_i \} = k_{ij}$
       - For all cases where $k_i$ is $1, 2, \dots, n$
   - Variables like $k_{ij}$ are hidden and are called <span style="color:red">latent variables</span>.

![bg right:20% 90%](./figs/belong_prob.png)

---

### How to Calculate $k_{ij}$

- $k_{ij}$ is the density of the Gaussian distribution for cluster $j$ multiplied by the mixture ratio.
- Derivation of the formula
    - $\text{Pr}\{ k_i = j |\boldsymbol{x}_i \} = \eta p(\boldsymbol{x}_i | k_i = j )\text{Pr}\{ k_i = j \}$ (Bayes' Theorem)
        - $p(\boldsymbol{x}_i | k_i = j )$: Gaussian distribution for the $k_i$th cluster
        - $\text{Pr}\{ k_i = j \}$: Probability of data being in the $k$th cluster when information on $\boldsymbol{x}_i$ is unavailable ($=\pi_k$)
    - $k_{ij} = \eta \pi_k \mathcal{N}(\boldsymbol{x}_i | \boldsymbol{\mu}_j, \Sigma_j)$<span style="color:red">←Can be calculated</span>
        - Determine $\eta$ so that the sum of the $k_{ij}$ values ​​for each cluster equals $1$.

---

### M-step

- Calculate distribution parameters with $k_{ij}$ fixed.
- Method (weighted by $k_{ij}$ and perform statistics).
    - Consider the auxiliary parameter $N_j = \sum_{i=1}^N k_{ij}$.
        - Equivalent to the number of elements in each cluster.
    - Calculate the size, mean, and covariance matrix of each cluster based on $N_j$ and $k_{ij}$.
    - $\pi_j = \eta N_j = N_j / \sum_{j=1}^n N_j$.
    - $\boldsymbol{\mu}_j = \dfrac{1}{N_j}\sum_{i=1}^N k_{ij}\boldsymbol{x}_i$
    - $\Sigma_j = \dfrac{1}{N_j-1} \sum_{i=1}^N k_{ij}(\boldsymbol{x}_i - \boldsymbol{\mu}_j)(\boldsymbol{x}_i - \boldsymbol{\mu}_j)^\top$

![bg right:28% 90%](./figs/m-step.png)

---

### What the EM algorithm can/cannot do

- What it can do
- Introduces a probabilistic approach
- (I apologize for the lack of examples, but) Performance is better than k-means
- Leaving unclear points vague reduces the chance of making strange mistakes
- Establishes a criterion of "maximum likelihood" for a probabilistic model
- Can be applied to other probabilistic models
- What is not possible
- It could be more probabilistic
- Parameters also have distributions (Gaussian mixtures also vary probabilistically)
- The number of Gaussian distributions is fixed
- It is not powerful enough to eliminate unnecessary distributions

---

## Supplementary Materials

---

### General Derivation of the EM Method

- The log-likelihood on p. 13 and the latent variables on p. 14 are written as follows (to reduce the number of symbols):
- $p(\boldsymbol{x}_{1:N} | \boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}) = p(X | \boldsymbol{\Theta})$
- $z_{1:N} = Z$
- $\log_e p(X,Z | \boldsymbol{\Theta})$ is transformed
- $\log_e p(X,Z | \boldsymbol{\Theta}) = \log_e p(Z | X, \boldsymbol{\Theta})p(X | \boldsymbol{\Theta})$
$= \log_e p(Z | X, \boldsymbol{\Theta}) + \log_e p(X | \boldsymbol{\Theta})$ (← the last term is the log-likelihood)
- Move the log-likelihood to the right-hand side, multiply each term by $q(Z)$, and integrate with respect to $Z$ ($\int_Z q(Z) \text{d}Z= 1$)
- $\int_Z q(Z) \log_e p(X | \boldsymbol{\Theta}) \text{d}Z = \int_Z q(Z) \log_e p(X,Z | \boldsymbol{\Theta})\text{d}Z$
$\qquad\qquad\qquad\qquad\quad - \int_Z q(Z) \log_e p(Z| X, \boldsymbol{\Theta}) \text{d}Z$
- The integral on the left side can be removed because $Z$ is not within $\log_e p(X | \boldsymbol{\Theta})$.
- $\log_e p(X | \boldsymbol{\Theta}) = \int_Z q(Z) \log_e p(X, Z | \boldsymbol{\Theta})\text{d}Z - \int_Z q(Z) \log_e p(Z |X, \boldsymbol{\Theta}) \text{d}Z$

---

### Deriving the EM Method Considering Latent Variables (continued)

- Add two terms that become zero when added to the right side and distribute them.
- $\log_e p(X | \boldsymbol{\Theta}) = \int_Z q(Z)\log_e p(X, Z | \boldsymbol{\Theta})\text{d}Z - \int_Z q(Z) \log_e p(Z |X, \boldsymbol{\Theta}) \text{d}Z$
$= \int_Z q(Z) \log_e p(X, Z | \boldsymbol{\Theta})\text{d}Z - \int_Z q(Z) \log_e p(Z |X, \boldsymbol{\Theta}) \text{d}Z$
$\quad- \int_Z q(Z) \log_e q(Z) \text{d}Z + \int_Z q(Z) \log_e q(Z) \text{d}Z$
$= \int_Z q(Z) \log_e \dfrac{ p(X, Z | \boldsymbol{\Theta}) }{q(Z)} \text{d}Z - \int_Z q(Z) \log_e \dfrac{p(Z |X, \boldsymbol{\Theta})}{q(Z)} \text{d}Z$
- Define and organize new functions
- $\log_e p(X | \boldsymbol{\Theta}) = \mathcal{L}(q, \boldsymbol{\Theta}) + \text{KL}(q || p)$
- $\mathcal{L}(q, \boldsymbol{\Theta}) = \int_Z q(Z) \log_e \dfrac{ p(X, Z | \boldsymbol{\Theta}) }{q(Z)} \text{d}Z$
- $\text{KL}(q || p) = - \int_Z q(Z) \log_e \dfrac{p(Z |X, \boldsymbol{\Theta})}{q(Z)} \text{d}Z$

---

### The resulting equation

- $\log_e p(\boldsymbol{x}_{1:N} | \boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}) = \mathcal{L}(q, \boldsymbol{\mu}_{1:n}, \Sigma_{1:n}, \pi_{1:n}) + \text{KL}(q || p)$
- $= \mathcal{L}(q, \boldsymbol{\Theta}) + \text{KL}(q || p)$
- $q$($q(Z)$): Distribution of the latent variable
- $\text{KL}(q || p)$: <span style="color:red">Kullback-Leibler distance</span>
- Quantifies the difference in shape between the distributions $q$ and $p(Z | X, \boldsymbol{\Theta})$
(If they match, it is $0$, and as they differ, it becomes a large positive value.)
- $\mathcal{L}$: Variational lower bound
- Log likelihood (The value of the left-hand side cannot be lower than this, because KL is greater than or equal to 0.)

---

### The resulting formula and how to use it

- $\log_e p(X | \boldsymbol{\Theta}) = \mathcal{L}(q, \boldsymbol{\Theta}) + \text{KL}(q || p)$
- $q$($q(Z)$): Distribution of the latent variable
- $\text{KL}(q || p)$: <span style="color:red">Kullback-Leibler distance</span>
- Quantifies the difference in shape between the distributions $q$ and $p(Z |X, \boldsymbol{\Theta})$.
(If they match, it's $0$, and the more they differ, the larger the positive value becomes.)
- $\mathcal{L}$: Variational lower bound
- Log likelihood (The value of the left-hand side cannot be lower than this, because KL is greater than or equal to 0.)
- Usage
- Fix $\boldsymbol{\Theta}$ to $\boldsymbol{\Theta}_\text{old}$ and search for a "good" $q(Z)$ (<span style="color:red">E-step</span>)
- Setting $\text{KL}$ to $0$ seems appropriate. $\Rightarrow \mathcal{L}$ matches the log likelihood.
- Fix $q(Z)$ and update $\boldsymbol{\Theta}_\text{old}$ to $\boldsymbol{\Theta}_\text{new}$ (<span style="color:red">M-step</span>)
- To maximize $\mathcal{L}$ (the log likelihood also increases, resulting in a better result)

---

## Review of Lesson 5

- Consider the "distribution of success rates" based on the success and failure of the experiment.
- Beta distribution: $p(x) = \eta x^{\alpha-1}(1-x)^{\beta-1}$
- As the results of each experiment are reflected one by one, the distribution of success rates changes.
- Figure below: Evolution of the distribution for success, success, failure, and failure
- <span style="color:red">Don't assume the success rate is 1/2</span>
- The distribution change was calculated using Bayes' theorem.

![](./figs/success_distribution.png)

---
## Bayesian inference for Gaussian mixture distributions

- Consider the "distribution of mixture distributions"
- The distribution can be drawn as shown in the right figure.
- Difference from EM method
- Calculates the distribution of distributions themselves, not the maximum likelihood.
- Updates the distribution using Bayes' theorem when data is received.
- Problem: Posterior probabilities cannot be calculated in one go using Bayes' theorem.
- What to do? Gradually change the distribution, as in the $\rightarrow$EM method.
