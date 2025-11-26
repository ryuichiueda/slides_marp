---
marp: true
---

<!-- footer: Probabilistic Robotics Lecture 8 -->

# Probabilistic Robotics Lecture 8: Machine Learning (Part 1)

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

- Least squares method and loss function
- When the least squares Method cannot be analytically solved
- Bayesian linear regression

---

## Before That (From the First Advanced Vision Lesson)

- Review of Neurons
    ![w:300](./figs/Retina-diagram.svg.png)<span style="font-size:40%">(https://commons.wikimedia.org/wiki/File:Retina-diagram.svg, by S. R. Y. Cajal and Chrkl, CC-BY-SA 3.0)</span>
    - Light enters from the left and is received by the photoreceptor cells (two types, 130 million) on the right, converting them into electrical signals.
    - The electrical signals are processed to the right and then sent to the brain via the downward red line in the diagram.
        - The red lines in each part of the retina form a bundle of 1 million optic nerves and reach the brain.

---

- Because of this structure,
    - when we look at something, 130 million individual signals are received.
        - In the case of a black-and-white image, this can be simplified to 130 million ON/OFF switch signals.

<center style="color:red">How can we see the shape even though the signals are so individual? </center>

---

### Basic Idea

- Data is generated due to some cause.
    - For example, if a couple wearing pink clothes is standing in front of you, a lot of pink signals will be received by your photoreceptor cells.
- <span style="color:red">If the cause is modeled mathematically, the observed data is thought to arise from it.</span>
    - Example 1: The cause is the function $\boldsymbol{y} = f(\boldsymbol{x})$
        - Data $(\boldsymbol{x}, \boldsymbol{y})_1, (\boldsymbol{x}, \boldsymbol{y})_2,\dots,(\boldsymbol{x}, \boldsymbol{y})_N$ is observed.
    - Example 2: The cause is the probability distribution $\boldsymbol{x} \sim P$
        - Data $\boldsymbol{x}_1, \boldsymbol{x}_2, \dots, \boldsymbol{x}_N$ is observed (creating some characteristic distribution)

<span style="color:red">A problem of calculating the cause $f$ and $P$ from data. $\Rightarrow$ Regression problem (self-localization is one example)</span>

---

### How to solve regression problems

- Various methods, from least squares to artificial neural networks (ANNs)
- Let's start with the basic least squares method.
    - Flow of story: Least squares is not probabilistic, so it has limitations. $\rightarrow$ Introducing probability.

---
## Least squares method

- Finding the trend $y = f(x)$ of the vertical axis values ​​relative to the horizontal axis values ​​($x$)
- Example (data from the [Japan Society of Hospital Pharmacists](https://www.jshp.or.jp/))
- What I want to know
- What is the relationship between height and weight?
- What is the relationship between blood pressure and triglyceride concentration?
- The vertical distribution is large, but I want to find a central pattern for now.
(This is just an example, not a solution.)

![bg right:30% 100%](./figs/relations.png)

---

### Situations for Using Regression

For the data on the right, it seems reasonable to apply a probability distribution.

- There's no point/interest in considering the horizontal distribution.
- When it's meaningless: Time series data, etc.
(e.g., stock prices, population trends)
- There's no need to treat time as a distribution.

![bg right:30% 100%](./figs/relations.png)

---

### Fitting a Linear Equation Using the Least Squares Method

- For the points $(x, y)_{1:N}$, find $w_1, w_0$, where the line $y=w_1 x + w_0$ passes through the middle.
- $w_1$ is the slope, and $w_0$ is the intercept.
- The most basic regression you've probably studied somewhere.

![bg right:30% 100%](./figs/lsm_liner.png)

<br />
<center style="color:red">How do we determine the "center"?</center>

---

### How do we determine the "center"?

- Consider the distance between the line and each point along the y-axis as the loss, and minimize it by adding the square of the distance.
- <span style="color:red">Loss function</span>$\mathcal{L}(w_{0:1}| x_{1:N}, y_{1:N}) = \{w_1 x_1 + w_0 -y_1\}^2$
$\qquad\qquad+\{w_1 x_2 + w_0 -y_2\}^2+\dots$
$\qquad\qquad+\{w_1 x_N + w_0 -y_N\}^2$
Minimize the value of $= \sum_{i=1}^N \{w_1 x_i + w_0 -y_i\}^2$
- Why square it?: It's not necessary, but it makes sense if you interpret it as minimizing variance.
- The loss function is also important in ANNs.
- The process is not very different.

![bg right:30% 100%](./figs/lsm_loss.png)

---

### Derive parameters to minimize the loss function

- Partially differentiate the loss function with respect to the parameters to find the parameters that make $0$.
- $\nabla \mathcal{L}(w_{0:1} | x_{1:N}, y_{1:N} ) = \left( \dfrac{\partial\mathcal{L}}{\partial w_0}, \dfrac{\partial\mathcal{L}}{\partial w_1} \right) = \boldsymbol{0}$
- No matter how $w_0$ and $w_1$ are shifted, the value of $\mathcal{L}$ does not change.
$\Rightarrow$If there are no other such points, the value at that point is the minimum value of $\mathcal{L}$.
- Let's try solving the equation on the previous page.
- $\mathcal{L}(w_{0:1}| x_{1:N}, y_{1:N}) = \sum_{i=1}^N \{w_1 x_i + w_0 -y_i\}^2$
- Set simultaneous equations by differentiating with respect to $w_0$ and $w_1$.

---

### Answer

We set $(x,y) = (x \ y)^\top$.

- $\nabla L(w_{0:1}) = 2 \sum_{i=1}^N \begin{pmatrix} 
\left\{ (w_1 x_i + w_0 ) - y_i \right\} \\ 
\left\{ (w_1 x_i + w_0 ) - y_i \right\}x_i 
\end{pmatrix}$ 
$= 2N \begin{pmatrix} 
w_1 \bar{x} + w_0 - \bar{y}\\ 
w_1 \overline{x^2} + w_0 \bar{x} - \overline{xy} 
\end{pmatrix} = \boldsymbol{0}$ ($\overline{\ }$ is the average value)
<span style="color:red">$\Longrightarrow (w_0 , w_1) = \left(
\dfrac{\overline{x^2}\bar{y} - \overline{xy}\bar{x}}{\overline{x^2} - \bar{x}^2},
\dfrac{\overline{xy} - \bar{x}\bar{y}}{\overline{x^2} - \bar{x}^2}
\right)$</span>
- The problem can be solved by simply rearranging the equations, so there's no need to use an ANN.

---

### Let's do the calculation.

- Apply the least squares method to $(x,y) = (2,3), (6,2), (-3,1), (-6,2)$.
- Equation (found earlier): $(w_0 , w_1) = \left(
\dfrac{\overline{x^2}\bar{y} - \overline{xy}\bar{x}}{\overline{x^2} - \bar{x}^2},
\dfrac{\overline{xy} - \bar{x}\bar{y}}{\overline{x^2} - \bar{x}^2}
\right)$

![bg right:40% 100%](./figs/lms_problem.png)

---

### Answer

- Apply least squares to $(x,y) = (2,3), (6,2), (-3,1), (-6,2)$
- Calculate various means
- $\overline{x}= -1/4$
- $\overline{y}= 2$
- $\overline{x^2}= 85/4$
- $\overline{xy}= 3/4$
- $w_0 = (\overline{x^2}\bar{y} - \overline{xy}\bar{x})/(\overline{x^2} - \bar{x}^2)= 2.01$
- $w_1 = (\overline{xy} - \bar{x}\bar{y})/(\overline{x^2} - \bar{x}^2)= 0.0590$
$\Longrightarrow y=0.0590 x + 2.01$

![bg right:40% 100%](./figs/lms_ans.png)

---

## Optimization when partial differential equations cannot be solved

- Consider optimizing a loss function consisting of $n$ parameters
- $\mathcal{L}(w_{1:n}| x_{1:N}, y_{1:N})$
- How do we find $w_
