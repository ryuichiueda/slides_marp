---
marp: true
---

<!-- footer: Probabilistic Robotics Lecture 6 -->

# Probabilistic Robotics, Lecture 6: Motion of Probability Distribution (Part 2)

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

- Moving objects and probability
    - Distribution transitions and predictions when a "nonlinear robot" moves

![bg right:30% 95%](https://upload.wikimedia.org/wikipedia/commons/d/d1/2022%E5%B9%B4%E5%8F%B0%E9%A2%A814%E5%8F%B7%E3%81%AE%E4%BA%88%E5%A0%B1%E5%86%86_%28%E6%B0%97%E8%B1%A1%E5%BA%81%29.jpg)

<span style="font-size:50%"><a href="https://ja.wikipedia.org/wiki/%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB:2022%E5%B9%B4%E5%8F%B0%E9%A2%A814%E5%8F%B7%E3%81%AE%E4%BA%88%E5%A0%B1%E5%86%86_(%E6%B0%97%E8%B1%A1%E5%BA%81).jpg">画像: 気象庁 CC BY-SA 4.0</a></span>

---

## Position Prediction for "Nonlinear Robots"

- In other words, position prediction for ordinary robots

---

### "Linear" and "Nonlinear"

- Linear state equation
   - $\boldsymbol{x}_t = A \boldsymbol{x}_{t-1} + B \boldsymbol{u}_t + \boldsymbol{\varepsilon}$
- The robot has a direction, so it doesn't look like the one above (<span style="color:red">nonlinear</span>).
    - Example: for the robot shown on the right (Control commands are velocity and angular velocity)
        - <span style="font-size:90%">$\begin{pmatrix} x_t \\ y_t \\ \theta_t \end{pmatrix} = \begin{pmatrix} x_{t-1} \\ y_{t-1} \\ \theta_{t-1} \end{pmatrix} + \nu_t\omega_t^{-1} \begin{pmatrix} \sin( \theta_{t-1} + \omega_t \Delta t ) - \sin\theta_{t-1} \\ -\cos( \theta_{t-1} + \omega_t \Delta t ) + \cos\theta_{t-1} \\ \omega_t \Delta t\end{pmatrix}$</span><br />
            - $\Delta t$: The (continuous, not discrete) time between $t$ and $t-1$

![bg right:17% 95%](./figs/control_output.png)

---

### Difficulties in nonlinear cases

- <span style="color:red">Reproducibility disappears</span>
    - As the robot moves, the pdf becomes non-Gaussian.
- Right: The experiment in Chapter 4 repeated 100 times.
    - The more the orientation shifts due to noise, the slower the progress along the $x$ axis becomes.
$\Longrightarrow$ Banana-shaped distribution

Let's calculate $p_t$ as far as possible.

![bg right:25% 95%](./figs/simulated_on.png)

---

### Calculating robot movement

- Consider the movement $\Delta \boldsymbol{x}_t'$ in the robot coordinate system $\Sigma_\text{robot}$ as the control command and set up the state equation.
    - $\Delta \boldsymbol{x}_t' = (\Delta x_t' \ \ \Delta y_t' \ \ \Delta \theta_t')^\top$
    - $\Sigma_\text{robot}$ is based on the pose before movement.
- Policy
     - Consider the movement $\Delta \boldsymbol{x}_t$ in the world coordinate system $\Sigma_\text{world}$.
- $\Delta \boldsymbol{x}_t = (\Delta x_t \ \ \Delta y_t \ \ \Delta \theta_t)^\top$
- Derive the equation $\boldsymbol{x}_t = \boldsymbol{f}(\Delta \boldsymbol{x}'_t)$, which relates $\Delta\boldsymbol{x}_t'$ and $\Delta\boldsymbol{x}_t$.
- $\boldsymbol{x}_t =\Delta \boldsymbol{x}_t + \boldsymbol{x}_{t-1}= \boldsymbol{f}(\Delta \boldsymbol{x}'_t) + \boldsymbol{x}_{t-1}$
As the equation of state.

The answer is on the next page.

![bg right:22% 95%](./figs/robot_coordinate2.png)

---

### Calculating the Robot's Movement (Answer)

- The relationship between the $x$ and $y$ coordinates can be expressed using a rotation matrix.
- $\begin{pmatrix} \Delta x_t \\ \Delta y_t \end{pmatrix} = R(\theta_{t-1}) \begin{pmatrix} \Delta x'_t \\ \Delta y'_t \end{pmatrix}$
- The change in $\theta$ is the same in both coordinate systems. $\Rightarrow \Delta \theta_t = \Delta \theta_t'$
- In summary
- $\Delta \boldsymbol{x}_t = T(\boldsymbol{x}_{t-1}) \Delta \boldsymbol{x}_t'$
- Here, $T(\boldsymbol{x}_{t-1}) =
\begin{pmatrix}
\cos \theta_{t-1} & -\sin \theta_{t-1} & 0 \\
\sin \theta_{t-1} & \cos \theta_{t-1} & 0 \\
0 & 0 & 1
\end{pmatrix}$
(Homogeneous transformation matrix)
- State equation: $\boldsymbol{x}_t = T(\boldsymbol{x}_{t-1}) \Delta \boldsymbol{x}_t' + \boldsymbol{x}_{t-1}$

![bg right:22% 95%](./figs/robot_coordinate2.png)

---

### Checking for nonlinearity and countermeasures

- State equation: $\boldsymbol{x}_t = T(\boldsymbol{x}_{t-1}) \Delta \boldsymbol{x}_t' + \boldsymbol{x}_{t-1}$
- It does not become a linear equation, $\boldsymbol{x}_t = A \Delta \boldsymbol{x}_t' + B \boldsymbol{x}_{t-1}$.
- $\theta_t$ in $\boldsymbol{x}_t$ is mixed into $A$.
- When calculating $p_t(\boldsymbol{x})$ from $p_{t-1}(\boldsymbol{x})$ (assumed to be Gaussian), the movement of $\boldsymbol{x}$ within the distribution of $p_{t-1}$ is not aligned in one direction, so $p_t$ is distorted and not a Gaussian distribution.
- How do we calculate $p_t$? - Do not use reproducibility (later)
- <span style="color:red">Linear approximation</span>

![bg right:22% 95%](./figs/nonlinear_motion.png)

---

### Linear approximation

- Approximate $\Delta \boldsymbol{x}_t = T(\boldsymbol{x}_{t-1}) \Delta \boldsymbol{x}_t'\simeq T(\boldsymbol{\mu}_{t-1}) \Delta \boldsymbol{x}_t' + G (\boldsymbol{x}_{t-1} - \boldsymbol{\mu}_{t-1})$

- Substitute $T(\boldsymbol{x}_{t-1})$ for $T(\boldsymbol{\mu}_{t-1})$
- $\boldsymbol{\mu}_{t-1}$: The center of the distribution of $p_{t-1}$
- $T(\boldsymbol{x}_{t-1}) =
\begin{pmatrix}
R(\theta_{t-1})& \boldsymbol{0} \\
\boldsymbol{0} & 1
\end{pmatrix}$
Therefore, $\theta_{t-1}$ is substituted with the $\theta$ component of $\boldsymbol{\mu}_{t-1}$.
- $G (\boldsymbol{x}_{t-1} - \boldsymbol{\mu}_{t-1})$: Correction of deviation due to approximation
- The further away from the center, the greater the correction required.

<span style="color:red">How do we calculate $G$? </span>

![bg right:30% 95%](./figs/linearization.png)

---

### Calculating $G$

- Reprint: $\Delta \boldsymbol{x}_t \simeq T(\boldsymbol{\mu}_{t-1}) \Delta \boldsymbol{x}_t' + G (\boldsymbol{x}_{t-1} - \boldsymbol{\mu}_{t-1})$
- What is $G$?
- The percentage of deviation of $\Delta \boldsymbol{x}_t$ when $\boldsymbol{x}_{t-1}$ deviates from $\boldsymbol{\mu}_{t-1}$.
<span style="color:red"
