---
marp: true
---

<!-- footer: Probabilistic Robotics, Lecture 4 (Part 3) -->

# Probabilistic Robotics, Lecture 4: Continuous Values and Multivariate Functions (Part 3)

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

- Multivariate Gaussian distribution
- Calculations for multivariate Gaussian distribution

---

## Multivariate Gaussian Distribution

- Gaussian-distributed variables $x_{1:n}$ can be collectively expressed as a single multidimensional Gaussian distribution.
    - $\mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}, \Sigma) = \dfrac{1}{\sqrt{(2\pi)^n |\Sigma|}}
\exp\left\{-\dfrac{1}{2}(\boldsymbol{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu}) \right\}$
        - Here, 
$\boldsymbol{x} = \begin{pmatrix} 
x_1 \\ x_2 \\ \vdots \\ x_n 
\end{pmatrix}, \ 
\boldsymbol{\mu} = \begin{pmatrix} 
\mu_1 \\ \mu_2 \\ \vdots \\ \mu_n 
\end{pmatrix}, \ 
\Sigma = \begin{pmatrix} 
\sigma^2_1 & \sigma_{12} & \dots & \sigma_{1n} \\ 
\sigma_{12} & \sigma^2_2 & \dots & \sigma_{2n} \\ 
\vdots & \vdots & \ddots & \vdots \\ 
\sigma_{1n} & \sigma_{2n} & \dots & \sigma^2_n \\
\end{pmatrix}$

---

### Variance-covariance matrix

- $\Sigma$ on the previous page: a matrix combining the variances and covariances of each variable
    - $\Sigma = \begin{pmatrix}
\sigma^2_1 & \sigma_{12} & \dots & \sigma_{1n} \\
\sigma_{12} & \sigma^2_2 & \dots & \sigma_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
\sigma_{1n} & \sigma_{2n} & \dots & \sigma^2_n \\
\end{pmatrix}$
        - $\sigma_{ij} = \big\langle (x_i - \mu_i )(x_j-\mu_j) \big\rangle_{\mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}, \Sigma)}$
- In normal conversation, "covariance matrix" is acceptable.

---

### Example: Mobile Robot Experiment

- Let's fit $x$ and $y$ from the experimental data to a multivariate Gaussian distribution (2D Gaussian distribution).
- [Data for 20 trials](./misc/xy_data.txt)
    - Column 1: $x$[m], Column 2: $y$[m]
- Parameters to be calculated
    - Mean and variance of $x$ and $y$
    - Covariance of $x$ and $y$
        - <span style="color:red">How to calculate covariance from data</span>: $s_{ab} = \dfrac{1}{N-1}\sum_{i=1}^n (a_i - \bar{a})(b_i - \bar{b})$
            - For $N$ data pairs $(a,b)_{1:N}$

![bg right:30% 95%](./figs/robot_final_pos_b.png)

---

### Calculation Results

- Example using `datamash`
```bash
### Mean ###
$ cat xy_data.txt | tr ' ' \\t | datamash mean 1 mean 2
3.8822 0.51035
### Variance ###
$ cat xy_data.txt | tr ' ' \\t | datamash svar 1 svar 2
0.016455957894737 0.19727097631579
### Covariance ###
$ cat xy_data.txt |tr ' ' \\t | datamash scov 1:2
-0.029138231578947
```
- Write the Gaussian distribution equation using these values.

---

### Answer

- $\mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}, \Sigma) = \dfrac{1}{\sqrt{(2\pi)^2 |\Sigma|}}
\exp\left\{-\dfrac{1}{2}(\boldsymbol{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu}) \right\}$
    - $\Sigma
= \begin{pmatrix}
0.016 & -0.029 \\
-0.029 & 0.197 \\
\end{pmatrix},
\boldsymbol{\mu}
= \begin{pmatrix}
3.88 \\
0.51
\end{pmatrix}$
- We understand the formula, but I'm not sure how to interpret it.
    - Let's try drawing a graph.

---

### Drawing a Bivariate Gaussian Distribution

- Let's start by drawing the point that is Mahalanobis distance $n$ from the center.
    - Mahalanobis distance: $D_\text{M}(\boldsymbol{x}) = \sqrt{
(\boldsymbol{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu})}$
        - Compare with a 1-dimensional model.
- The figure is an ellipse.
    - Ellipse formula: $\dfrac{(x - \mu_x)^2}{a^2} + \dfrac{(y - \mu_y)^2}{b^2} = 1$
        - Converting $(\boldsymbol{x} - \boldsymbol{\mu})^\top \Sigma^{-1} (\boldsymbol{x} - \boldsymbol{\mu})$ into a polynomial results in the same form (verify on the next page).

![bg right:30% 95%](./figs/2d_gauss_draw_question.png)

---

### Diagonalize first

- Decompose $\Sigma$ as follows:
    - $\Sigma = R(-\theta)^\top S R(-\theta)$
        - $R(\theta) =
\begin{pmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{pmatrix}$: Rotation matrix
        - $S =
\begin{pmatrix}
\sigma_a^2 & 0 \\
0 & \sigma_b^2 \\
\end{pmatrix}
= \text{diag}(\sigma_a^2, \sigma_b^2)$: Diagonal matrix
- Then
    - $D_\text{M}(\boldsymbol{x})
= \sqrt{
(\boldsymbol{x} - \boldsymbol{\mu})^\top \{
R(-\theta)^\top S R(-\theta)
\}^{-1} (\boldsymbol{x} - \boldsymbol{\mu})
}$
$=
\sqrt{
(\boldsymbol{x} - \boldsymbol{\mu})^\top 
R(-\theta)^{-1} S^{-1} \{R(-\theta)^{\top}\}^{-1} 
(\boldsymbol{x} - \boldsymbol{\mu}) 
}$ 
$= 
\sqrt{ 
(\boldsymbol{x} - \boldsymbol{\mu})^\top 
R(-\theta)^{\top} S^{-1}R(-\theta) 
(\boldsymbol{x} - \boldsymbol{\mu}) 
}$ 
$= 
\sqrt{ 
\{R(-\theta)(\boldsymbol{x} - \boldsymbol{\mu})\}^\top 
S^{-1} \{ R(-\theta) 
(\boldsymbol{x} - \boldsymbol{\mu}) \} 
}$

---

### Coordinate transformation

- Last equation on the previous page: $D_\text{M}(\boldsymbol{x}) =
\sqrt{
\{R(-\theta)(\boldsymbol{x} - \boldsymbol{\mu})\}^\top
S^{-1} \{ R(-\theta)
(\boldsymbol{x} - \boldsymbol{\mu}) \}
}$
- Substituting the following, we get $D_\text{M}(\boldsymbol{x}) = \sqrt{ a^2/\sigma_a^2 + b^2 / \sigma_b^2}$
- $\boldsymbol{a} = (a \ \ b)^\top = R(-\theta)(\boldsymbol{x} - \boldsymbol{\mu})$
- $S = \text{diag}(\sigma_a^2, \sigma_b^2)$
- Therefore
- The figure drawn by points whose Mahalanobis distance is $n$:
The ellipse that satisfies $\dfrac{a^2}{\sigma_a^2} + \dfrac{b^2}{\sigma_b^2} = n^2$ in the $ab$-coordinate system

---

### Return coordinates

- The ellipse that satisfies $\dfrac{a^2}{\sigma_a^2} + \dfrac{b^2}{\sigma_b^2} = n^2$ in the $ab$-coordinate system
