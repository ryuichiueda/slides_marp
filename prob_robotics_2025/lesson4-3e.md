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

- Convert an ellipse that satisfies $\dfrac{a^2}{\sigma_a^2} + \dfrac{b^2}{\sigma_b^2} = n^2$ in the $ab$-coordinate system to the $xy$-coordinate system
    - $\boldsymbol{a} = (a \ \ b)^\top = R(-\theta)(\boldsymbol{x} - \boldsymbol{\mu})$
- Rotate by $\theta$ and translate by $\mu$

$\qquad\qquad\qquad$![w:600](./figs/ellipse.png)

---

### Draw with actual values

- $\Sigma = \begin{pmatrix}
0.016 & -0.029 \\
-0.029 & 0.197 \\
\end{pmatrix}$
$= R(-8.9$deg$)
\begin{pmatrix}
0.107^2 & 0 \\
0 & 0.449^2 \\
\end{pmatrix}R(-8.9$deg$)$
$\boldsymbol{\mu}
= \begin{pmatrix}
3.88 \\
0.51
\end{pmatrix}$
- Right: Drawing ellipses for $n=1, 2, 3$
    - This is called the <span style="color:red">error ellipse</span>

![bg right:30% 95%](./figs/robot_final_pos_ellipse.png)

---

## Calculating the multivariate Gaussian distribution

- Is there reproducibility?

---

### Reproducibility and linear transformations

- Example 1: When $\boldsymbol{x}_i \sim \mathcal{N}(\boldsymbol{\mu}_i, \Sigma_i)\ (i=1,2)$, what is the distribution of $\boldsymbol{x} = \boldsymbol{x}_1 + \boldsymbol{x}_2$?
- $\boldsymbol{x}_1 and \boldsymbol{x}_2$ are independent.
- Answer (Let's write this by analogy with the 1-dimensional case):
* $\boldsymbol{x} \sim \mathcal{N}(\boldsymbol{\mu}_1 + \boldsymbol{\mu}_2, \Sigma_1 + \Sigma_2)$
- A derivation example is available in Detailed Explanation of Probabilistic Robotics.
- Example 2: When $\boldsymbol{x} \sim \mathcal{N}(\boldsymbol{\mu}, \Sigma)$, what is the distribution of $\boldsymbol{y} = A\boldsymbol{x} + \boldsymbol{b}$?
- Answer (this will be covered on the next page):
* $\boldsymbol{y} \sim \mathcal{N}(A\boldsymbol{\mu} +\boldsymbol{b}, A\Sigma A^\top )$
- $A\Sigma A^\top$: This form appears frequently.

---

### Linear transformation of the Gaussian distribution

- When transforming from the coordinate system of $\boldsymbol{x}$ to the coordinate system of $\boldsymbol{y} = A \boldsymbol{x} + \boldsymbol{b}$, the space is stretched by $|\det(A)|$ [[Sugiura 1985]](https://www.utp.or.jp/book/b302043.html)
- The area ratio of the green part in the diagram below is $1:|\det(A)|$
- Additional information: $|\det(A)|$ is the absolute value of the determinant of $A$
(Writing it as $||A||$ is confusing, so we use this notation.)
![w:600](https://upload.wikimedia.org/wikipedia/commons/3/34/DeterminantOfMatrix.png)
<span style="font-size:50%">[(Image: CC0)](https://commons.wikimedia.org/wiki/File:DeterminantOfMatrix.png)</span>

---

### Linear transformation of the Gaussian distribution (continued)

- When space is stretched $|\det(A)|$, the density is diluted by $1/|\det(A)|$
- $p(\boldsymbol{y}) = \mathcal{N}(\boldsymbol{x} | \boldsymbol{\mu}, \Sigma ) \big/ |\det(A)|$
$= \mathcal{N}\big[ A^{-1}(\boldsymbol{y} - \boldsymbol{b}) | \boldsymbol{\mu}, \Sigma \big] \big/ |\det(A)|$
$= \frac{1}{\sqrt{(2\pi)^n |\Sigma| |A|^2}}
\cdot\exp\left\{ 
-\frac{1}{2}\left[ A^{-1}(\boldsymbol{y} - \boldsymbol{b}) - \boldsymbol{\mu} \right]^T \Sigma^{-1} \left[ A^{-1}(\boldsymbol{y} - \boldsymbol{b}) - \boldsymbol{\mu}\right] 
\right\}$ 
- $|\Sigma| outside the exponent About |A|^2$$|\Sigma||A|^2 = |A| |\Sigma| |A^\top|= |A\Sigma A^\top|$ 
- $= in parentheses of exponent part -\frac{1}{2} \left[ 
A^{-1} ( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} ) 
\right]^\top \Sigma^{-1} A^{-1} ( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )$ 
$= -\frac{1}{2} 
( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )^\top 
(A^{-1})^\top \Sigma^{-1} A^{-1} ( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )$ 
$= -\frac{1}{2} 
( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )^\top 
(A \Sigma A^\top )^{-1} 
( \boldsymbol{y} - \boldsymbol{b} - A \boldsymbol{\mu} )$

$\Longrightarrow p(\boldsymbol{y}) = \mathcal{N}(\boldsymbol{y} | A\boldsymbol{\mu} + \boldsymbol{b}, A\Sigma A^\top)$

---

### Product of multivariate Gaussian distributions

- Problem:
$p(\boldsymbol{x}) = \eta \mathcal{N}(\boldsymbol{a} | What kind of distribution is A\boldsymbol{x} + \boldsymbol{b}, sB) \mathcal{N}(\boldsymbol{x} | \boldsymbol{c}, sC)$?
- This will be discussed in the second half of the lecture.
- Solution: Simply transform the equation.
- A note for the second half: Do not incorporate $s$ into $\eta$.
- $s > 0$

---

### Product of Multivariate Gaussian Distributions (Solution)

- First, simplify the expansion $\mathcal{N}$ by formulating it.
- $p(\boldsymbol{x}) = \eta
\dfrac{1}{\sqrt{(2\pi)^k |sB| }}
\dfrac{1}{\sqrt{(2\pi)^\ell |sC| }}$
$\cdot \exp\Big\{
-\dfrac{1}{2s}(\boldsymbol{a} - A\boldsymbol{x} - \boldsymbol{b})^\top B^{-1} (\boldsymbol{a} - A\boldsymbol{x} - \boldsymbol{b})
-\dfrac{1}{2s}(\boldsymbol{x} - \boldsymbol{c})^\top C^{-1}(\boldsymbol{x} - \boldsymbol{c})
\Big\}$
$= \dfrac{\eta}{s}
\exp\Big\{ -\dfrac{1}{2s} L(\boldsymbol{x}) \Big\}$
- where $L(\boldsymbol{x})$ is the exponent multiplied by $-2s$.

---

### Multivariate Gaussian Product (Answer, continued)

- Rearranging $L$
- $L(\boldsymbol{x}) = (A\boldsymbol{x})^\top B^{-1}(A\boldsymbol{x}) + \boldsymbol{x}^\top C^{-1}\boldsymbol{x}$
$\qquad\quad - (A\boldsymbol{x})^\top B^{-1}(\boldsymbol{a}- \boldsymbol{b} ) - \boldsymbol{x}^\top C^{-1}\boldsymbol{c}$
$\qquad\quad - (\boldsymbol{a}- \boldsymbol{b} )^\top B^{-1} (A\boldsymbol{x}) - \boldsymbol{c}^\top C^{-1} \boldsymbol{x} + U'$
- $U'$ is a term unrelated to $\boldsymbol{x}$
- $(XY)^\top = Y^\top X^\top$. ​​Using the property that the covariance matrix is ​​symmetric,
- $L(\boldsymbol{x}) = (A\boldsymbol{x})^\top B^{-1}(A\boldsymbol{x}) + \boldsymbol{x}^\top C^{-1}\boldsymbol{x}$
$\qquad\quad - 2(A\boldsymbol{x})^\top B^{-1}(\boldsymbol{a}- \boldsymbol{b} ) - 2\boldsymbol{x}^\top C^{-1}\boldsymbol{c} + U'$
$\qquad = \boldsymbol{x}^\top(A^\top B^{-1} A + C^{-1})\boldsymbol{x}- 2\boldsymbol{x}^\top \left\{ A^\top B^{-1}(\boldsymbol{a}- \boldsymbol{b} ) + C^{-1}\boldsymbol{c} \right\} + U'$

---

### Product of Multivariate Gaussian Distributions (Answer, continued)

- Replace the last line on the previous page with the following:
- $D^{-1} = A^\top B^{-1} A + C^{-1}$
- $\boldsy
