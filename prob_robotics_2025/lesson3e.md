---
marp: true
---

<!-- footer: Probabilistic Robotics, Lecture 3 -->

# Probabilistic Robotics, Lecture 3: Expected Value

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

- Expected value
- Calculating expected value, calculations using expected value

---

## Expected Value

- (Rough) Definition: the expected or predicted average value of a function of random variables
- Question: There is a gambling game where you pay 3700 yen and get back 1000 times the number on the dice. What is the expected value of the money you will win in one try?
    - Answer
        * $1000/6 + 1000\cdot 2/6 + 1000\cdot 3/6 + 1000\cdot 4/6$
$+ 1000 \cdot 5/6 + 1000 \cdot 6/6 - 3700 = 1000(3.5) - 3700$ <span style="color:red">$= -200$</span>

---

### The Significance of Expected Value in Everyday Life

- It enables us to think numerically, not intuition about the return you'll get from making a decision for probabilistic events.
- (Just to be clear) Don't oversimplify things and think in terms of expected value.
    - Example
        - The expected value of a lottery ticket is half the amount you bet, but people have actually won hundreds of millions of yen.
        - If you just aim to get credits for lectures with a profession "I live by maximizing expected value," you won't learn anything.

---

### The significance of expected value in robotics

- Appears in calculations when deciding on an action
   - Only one action can be chosen at a given time. $\rightarrow$ All possibilities are aggregated into a single numerical value.
- Many other examples appear in the calculation process (we'll do this today).

---

### Definition of expected value

- Expected value = $\text{Pr}\{$A$\}f($A$) + \text{Pr}\{$B$\}f($B$) + \cdots \text{Pr}\{$E$\}f($E$)$
    - Events A, B, C, ..., E are mutually exclusive, and the probability of any event other than A through E is 0.
        - $f$: A function that determines a numerical value, such as money, for an event.
- Notation using random variables
    - $\langle f \rangle_P = \sum_{x=-\infty}^{x=\infty}f(x)P(x)$
        - It can also be written as $\langle f(x) \rangle_{P(x)}$ 
            - When it is inconvenient if the variables are unknown
    - Notations such as $\text{E}_P(f)$ are also used
        - Note: $P$ is sometimes omitted, which can be confusing.

---

### Probability Distributions and Expected Values

- The mean and variance of a probability distribution can be expressed as expected values.
- The mean and variance of data $x_{1:N}$
    - $\bar{x}_{1:N} = \dfrac{x_1 + x_2 + \dots + x_N}{N} = \dfrac{1}{N} \sum_{i=1}^N x_i$
    - $s^2 = \dfrac{1}{N-1}\sum_{i=1}^{N} ( x_i - \bar{x})^2$
- If $x \sim P$, then
    - Mean value: Expected value of $x$
        - $\mu = \langle x \rangle_{P(x)}$
    - Variance: Expected value of the squared difference from the mean
        - $\sigma^2 = \langle (x - \mu)^2\rangle_{P(x)}$
            - Note: We'll discuss later the problem of $N-1$

---

### Linearity of expected value

- Problem: After paying 100 yen, you roll a dice. Let's consider the expected value if A and B give (or take) money as follows:
- Person A: roll $\times 100$ yen
- Person B: $(10 -$square of the roll$)\times 100$ yen

<center>After calculations, please go to the next page</center>

---

### Answer

- Probability distribution of the roll: $P(x) = 1/6$
- Function of the amount of money received when the dice are $x$
    - $f(x) = -100 + 100x + 100(10-x^2) = 900 + 100x - 100x^2$
- Calculation
    - $\langle f \rangle_P = \sum_{x=1}^6 (900 + 100x - 100x^2)/6$
<span style="color:red">$= 900 + 100 \cdot \dfrac{1}{6}\sum_{x=1}^6 x - 100 \cdot \dfrac{1}{6}\sum_{x=1}^6 x^2$</span>
$= 900 + 100 \cdot 3.5 - 100 \cdot (1+4+9+16+25+36)/6$
$= 900 + 350 - 100 \cdot 91/6 \approx -267$ yen

---

### Generalization of the example on the previous page

- What is the expected value of $f(x) = w_0 + w_1 g_1(x) + \dots + w_n g_n(x)$ when $x \sim P$?
    - Example from the previous page:
        - $g_1(x)=x, g_2(x)=x^2$
        - $w_0=w_1=100, w_2=-100$
- Answer
    * $\langle f \rangle_P = \sum_{x=-\infty}^\infty P(x)f(x)$
$= \sum_{x=-\infty}^\infty \{ w_0P(x) + w_1P(x)g_1(x) + \cdots + w_nP(x)g_n(x) \}$
$= w_0 \sum_{x=-\infty}^\infty P(x) + w_1 \sum_{x=-\infty}^\infty P(x)g_1(x) + \cdots + w_n\sum_{x=-\infty}^\infty P(x)g_n(x)$
$= w_0 \langle 1 \rangle_P + w_1 \langle g_1 \rangle_P+ \cdots + w_n \langle g_n \rangle_P$
* <span style="color:red">The expected value of a function $f$ = the sum of the expected values ​​of each term in $f$</span>
    - This is called "linearity of expectation."

---

### Example of using linearity: Calculating variance

- Simplifying the variance formula for probability distribution $P$
    - $\sigma^2 = \langle (x - \mu)^2\rangle_{P(x)}$
        - Let's decompose it using linearity.
- Answer
    * $\sigma^2 = \langle x^2 -2 x\mu + \mu^2\rangle_{P(x)}$
$= \langle x^2 \rangle_{P(x)} -2 \mu \langle x\rangle_{P(x)} + \mu^2 \langle 1 \rangle_{P(x)}$ 
$= \langle x^2 \rangle_{P(x)} -2 \mu \mu + \mu^2$ 
$= \langle x^2 \rangle_{P(x)} - \mu^2$


---

### Other properties of expected value1


- $\big\langle f(x) \big\rangle_{P(x,y)} = \big\langle f(x) \big\rangle_{P(x)}$ 
    - Why?
- Answer (from the marginalization formula)
    * $\big\langle f(x) \big\rangle_{P(x,y)}= \sum_{x=-\infty}^\infty \sum_{y=-\infty}^\infty f(x) P(x,y)$
$= \sum_{x=-\infty}^\infty f(x) \sum_{y=-\infty}^\infty P(x,y)$
$= \sum_{x=-\infty}^\infty f(x) P(x)$
$= \big\langle f(x) \big\rangle_{P(x)}$

---

### Other properties of expected value 2

- $\big\langle \langle h(x,y) \rangle_{P(y)} \big\rangle_{P(x)} = \big\langle h(x,y) \big\rangle_{P(x)P(y)}$
    - Why?
- Answer
    * $\sum_{x=-\infty}^\infty P(x) \sum_{y=-\infty}^\infty h(x,y) P(y)$
$= \sum_{x=-\infty}^\infty \sum_{y=-\infty}^\infty h(x,y) P(x)P(y)$

---

### Other Properties of Expected Values ​​3

- $\big\langle f(x)g(y) \big\rangle_{P(x)P(y)} = \big\langle f(x) \big\rangle_{P(x)} \big\langle g(y) \big\rangle_{P(y)}$
    - Let's derive it without using $\Sigma$
* Left-hand side $=\big\langle \langle f(x)g(y)\rangle_{P(x)} \big\rangle_{P(y)}$ (from Property 2)
$= \big\langle \langle f(x)\rangle_{P(x)}g(y) \big\rangle_{P(y)}$ (the part unrelated to $x$ is outside the inner $\langle\rangle$)
$= \big\langle f(x) \big\rangle_{P(x)} \big\langle g(y) \big\rangle_{P(y)}$ (the part unrelated to $y$ is outside the outer $\langle\rangle$)

---

## Calculation using expected value

---

### Simplifying the marginalization formula

- $P(x) = \langle P(x|y) \rangle_{P(y)}$
    - Derivation
       * $P(x) = \sum_{y=-\infty}^\infty P(x,y) = \sum_{y=-\infty}^\infty P(x|y)P(y) = \langle P(x|y) \rangle_{P(y)}$
    - Convenient because no need to write $\Sigma$ or $\infty$

---

### Variance of the sum of two variables

- Let's calculate the variance of $(x+y)$, the sum of random variables $x$ and $y$.
- <span style="color:red">Covariance</span> $\Sigma_{xy} = \big\langle (x- \mu_x )(y-\mu_y) Simplify using \big\rangle_{P(x,y)}$
- See the next page for information on covariance.
- Answer
* $\sigma_{x+y}^2 = \left\langle \left\{ (x+y) - (\mu_x + \mu_y )\right\}^2 \right\rangle_{P(x,y)}$
$= \langle (x- \mu_x )^2 \rangle_{P(x,y)} + \langle (y- \mu_y )^2 \rangle_{P(x,y)} + 2 \big\langle (x- \mu_x )(y-\mu_y) \big\rangle_{P(x,y)}$
$= \langle (x- \mu_x )^2 \rangle_{P(x)} + \langle (y- \mu_y )^2 \rangle_{P(y)} + 2 \sigma_{xy}$
(From $\uparrow$p.12)
$= \sigma_x^2 + \sigma_y^2 + 2 \sigma_{xy}$
- Add the variances and then add the $2\times$ covariance.

---

### Covariance

- $\sigma_{xy} = \big\langle (x- \mu_x )(y-\mu_y) \big\rangle_{P(x,y)}$
- Inside $\langle\ \rangle$
- Positive if $x$ and $y$ exceed their respective means.
- Negative if one is above and the other below.
$\rightarrow$The positive and negative values ​​indicate the correlation between $x$ and $y$.
- Note that this is different from the correlation coefficient (please investigate this yourself).

---

### Simplifying the Covariance Formula

- Break down and streamline $\sigma_{xy} = \big\langle (x- \mu_x )(y-\mu_y) \big\rangle_{P(x,y)}$
- Answer
* $\sigma_{xy} = \big\langle xy - x\mu_y - y\mu_x + \mu_x \mu_y \big\rangle_{P(x,y)}$
$= \big\langle xy \big\rangle_{P(x,y)} - \big\langle x \big\rangle_{P(x,y)}\mu_y - \big\langle y \big\rangle_{P(x,y)}\mu_x + \mu_x \mu_y$
$= \big\langle xy \big\rangle_{P(x,y)} - \big\langle x \big\rangle_{P(x)}\mu_y - \big\langle y \big\rangle_{P(y)}\mu_x + \mu_x \mu_y$
$= \big\langle xy \big\rangle_{P(x,y)} - \mu_x\mu_y - \mu_y\mu_x + \mu_x \mu_y$
$= \big\langle xy \big\rangle_{P(x,y)} - \mu_x\mu_y$
- From this equation, the properties on the next page can be derived.

---

### Covariance when $x$ and $y$ are independent

- $\sigma_{xy} = \big\langle xy \big\rangle_{P(x,y)} - \mu_x\mu_y$ is further simplified.
- Calculation
* $= \big\langle xy \big\rangle_{P(x)P(y)} - \mu_x\mu_y= \langle x \rangle_{P(x)} \langle y \rangle_{P(y)} - \mu_x\mu_y = 0$
(Using the property on p.14)
$\Longrightarrow$<span style="color:red">If $x$ and $y$ are independent, the covariance is $0$</span>
- Formula derived from the above property
- $\sigma^2_{x+y}= \sigma_x^2 + \sigma_y^2 \quad (x \bot\!\!\!\!\bot y)$
- For independent variables, variances are additive (a convenient property)
- $\sigma^2_{x_1+x_2+\dots+x_n} = \sum_{i=1}^n \sigma^2_i\quad$ ($x_{1:n}$ are mutually independent or identically distributed)

---

### The relationship between unbiased variance and the variance of probability distributions (Today's final boss)

- When $x_{1:N} \overset{\text{iid}}{\sim} P$, do these two coincide?
- $s^2 = \dfrac{1}{N-1}\sum_{i=1}^{N} ( x_i - \bar{x})^2$ (expected value)
- $\sigma^2 = \langle (x - \mu)^2\rangle_{P(x)}$
- Let's check.
- Let the expected value of $s^2$ be $\langle s^2 \rangle_{Q(x_{1:N})} = \left\langle \dfrac{1}{N-1}\sum_{i=1}^{N} ( x_i - \bar{x})^2 \right\rangle_{Q(x_{1:N})}$.
- Here,
- $Q(x_{1:N})=P(x_1)P(x_2)\dots P(x_N)$
- $\bar{x} = (\sum_{i=1}^N x_i)/N$
- Let's transform $\langle s^2 \rangle_{Q(x_{1:N})}$ (next page)
- Hint: Make good use of the average value $\mu$ of $P(x)$

---

### Transformation of $\langle s^2 \rangle_{Q(x_{1:N})}$

- $(N-1)\langle s^2 \rangle_{Q(x_{1:N})} = \left\langle \sum_{i=1}^{N} \left\{ (x_i - \mu) + (\mu - \bar{x})\right\}^2 \right\rangle_{Q(x_{1:N})}$
$= \left\langle \sum_{i=1}^{N} (x_i - \mu)^2 + 2(\mu - \bar{x}) \sum_{i=1}^{N} (x_i - \mu) + \sum_{i=1}^{N} (\mu - \bar{x})^2 \right\rangle_{Q(x_{1:N})}$
$= \left\langle \sum_{i=1}^{N} (x_i - \mu)^2 + 2(\mu - \bar{x}) N (\bar{x} - \mu) + N (\mu - \bar{x})^2 \right\rangle_{Q(x_{1:N})}$
$= \left\langle \sum_{i=1}^{N} (x_i - \mu)^2 - N (\mu - \bar{x})^2 \right\rangle_{Q(x_{1:N})}$
$= \sum_{i=1}^{N} \left\langle (x_i - \mu)^2 \right\rangle_{Q(x_{1:N})} - N \left\langle
(\bar{x} - \mu)^2 \right\rangle_{Q(x_{1:N})}$
$= \sum_{i=1}^{N} \left\langle (x_i - \mu)^2 \right\rangle_{P(x_i)} - N \left\langle
\Big( \dfrac{\sum_{i=1}^{N} x_i}{N} - \mu \Big)^2 \right\rangle_{Q(x_{1:N})}$
($\uparrow$ Term 1: Eliminate unnecessary variables based on the property on p.12)

---

### Transformation of $\langle s^2 \rangle_{Q(x_{1:N})}$ (continued)

- $(N-1)\langle s^2 \rangle_{Q(x_{1:N})} = \sum_{i=1}^{N} \left\langle (x_i - \mu)^2 \right\rangle_{P(x_i)} - \dfrac{1}{N}
\left\langle \Big( \sum_{i=1}^{N} x_i - N\mu \Big)^2 \right\rangle_{Q(x_{1:N})}$
- First term on the right-hand side: The sum of the variances of $x_1, x_2, \dots, and x_N$
- Second term on the right-hand side: The variance of $x_1 + x_2 + \dots + x_N$ divided by $N$
(The property on p. 20 can be used.)
- Therefore
- $(N-1)\langle s^2 \rangle_{Q(x_{1:N})} = N\sigma^2 - N\sigma^2/N = (N-1)\sigma^2$
$\Longrightarrow$ <span style="color:red">$\langle s^2 \rangle_{Q(x_{1:N})} = \sigma^2$</span>
- The expected value of the unbiased variance and the expected value of the distribution are the same.
- Dividing by $N-1$ is appropriate.

---

## Summary

- Expected value
- Useful for profit and loss calculations
- Also useful for calculating probability (thanks for your hard work)
