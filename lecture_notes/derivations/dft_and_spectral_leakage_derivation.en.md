# DFT Periodicity and Spectral Leakage

This note shows, side-by-side, how the two main limitations of a digital seismic trace — **discrete sampling** and **finite length** — appear in the frequency domain. It follows the standard Fourier relationship:

> A restriction in one domain is a convolution in the other domain.

The level is intended for students who have met Fourier transforms and complex exponentials before but need a practical, step-by-step reminder of why DFT spectra look the way they do.

---

## 1. Three representations of the same signal

A seismic trace starts as a continuous function of time $x(t)$. In the computer it becomes a finite list of numbers $x[n]$, $n = 0, \dots, N-1$. The move from $x(t)$ to $x[n]$ involves two operations:

1. **Sampling**: keep only the values at $t = n\Delta t$.
2. **Windowing**: keep only those values inside a finite interval of length $T = N\Delta t$.

The order does not matter for the final result, but it is convenient to think about one effect at a time.

| Time-domain operation | Frequency-domain consequence |
|---|---|
| Continuous signal $x(t)$ | Continuous spectrum $X(f)$ |
| Sampling (discrete time) | Spectrum becomes periodic with period $f_s = 1/\Delta t$ |
| Windowing (finite length) | Spectrum is smeared by a sinc-shaped function |

---

## 2. The continuous Fourier transform pair

For a continuous, non-periodic signal $x(t)$ the Fourier transform is

$$
X(f) = \int_{-\infty}^{\infty} x(t) \, e^{-i 2\pi f t} \, dt,
$$

and the inverse transform is

$$
x(t) = \int_{-\infty}^{\infty} X(f) \, e^{i 2\pi f t} \, df.
$$

The two functions contain the same information: $X(f)$ tells us how much of each frequency is present in $x(t)$, and the phase of each frequency component.

In the continuous world there is no upper frequency limit and no periodicity: $X(f)$ can be non-zero at any frequency.

---

## 3. Effect 1: discretization creates periodicity

### Sampling in time

Sampling means we replace the continuous time variable $t$ by the discrete set $t_n = n\Delta t$. We can write this as multiplying $x(t)$ by a comb of delta functions:

$$
x_s(t) = x(t) \, \sum_{n=-\infty}^{\infty} \delta(t - n\Delta t).
$$

Only the values at the sample instants survive.

### What the comb looks like in frequency

The Fourier transform of a comb of delta functions in time is another comb of delta functions in frequency:

$$
\mathcal{F}\!\left\{ \sum_{n=-\infty}^{\infty} \delta(t - n\Delta t) \right\}
= \frac{1}{\Delta t} \sum_{k=-\infty}^{\infty} \delta\!\left(f - \frac{k}{\Delta t}\right).
$$

The spacing between the delta functions in frequency is the sampling frequency

$$
f_s = \frac{1}{\Delta t}.
$$

### Multiplication in time = convolution in frequency

Because multiplication in time corresponds to convolution in frequency, the spectrum of the sampled signal is the original spectrum convolved with the frequency comb:

$$
\boxed{
X_s(f) = \frac{1}{\Delta t} \sum_{k=-\infty}^{\infty} X\!\left(f - k f_s\right)
}
$$

This equation is the heart of the result:

> Sampling makes the spectrum **periodic**. Copies of the original spectrum are repeated at intervals of $f_s = 1/\Delta t$.

If the original spectrum is band-limited and the copies do not overlap, the baseband copy ($k=0$) is undistorted. If they overlap, the high frequencies of one copy leak into the baseband of another — this is **aliasing**.

### The Nyquist frequency

The centre of each copy is at $k f_s$, and the copies touch first at half the sampling frequency. The **Nyquist frequency** is

$$
\boxed{
f_N = \frac{f_s}{2} = \frac{1}{2\Delta t}
}
$$

If $X(f)$ contains no energy above $f_N$, the copies do not overlap and the original signal can be recovered from the samples. If energy is present above $f_N$, it folds back into the band $[-f_N, f_N]$ and cannot be separated from real low-frequency energy.

### Practical seismic example

For a typical seismic sample interval of $4$ ms:

$$
f_s = \frac{1}{0.004\ \text{s}} = 250\ \text{Hz}, \qquad
f_N = 125\ \text{Hz}.
$$

A $150$ Hz component sampled at $4$ ms will be indistinguishable from a $100$ Hz component:

$$
f_{\text{apparent}} = |150 - 250| = 100\ \text{Hz}.
$$

That is why field recording systems apply an analog anti-alias filter before the digitiser.

---

## 4. Effect 2: windowing smears the spectrum

### A finite-length trace is a windowed signal

A computer trace is not only sampled, it is also finite. In the continuous description we can think of this as multiplying the infinite sampled signal by a rectangular window:

$$
w(t) =
\begin{cases}
1, & 0 \le t \le T, \\
0, & \text{otherwise}.
\end{cases}
$$

The windowed signal is $x_w(t) = x_s(t)\, w(t)$. The length of the window is $T = N\Delta t$.

### Spectrum of the rectangular window

The Fourier transform of the rectangular window is a sinc function:

$$
W(f) = T \, \frac{\sin(\pi f T)}{\pi f T} \, e^{-i\pi f T}.
$$

The magnitude is proportional to $|\operatorname{sinc}(f T)|$, with the first zero at $f = 1/T$. A wider window has a narrower sinc main lobe, i.e. better frequency resolution.

### Convolution in frequency

Because multiplication in time is convolution in frequency, the spectrum of the finite sampled signal is

$$
\boxed{
X_w(f) = X_s(f) * W(f) = \int_{-\infty}^{\infty} X_s(f') \, W(f - f') \, df'
}
$$

The true spectrum $X_s(f)$ is **smeared** by the sinc function $W(f)$. This means:

- A single frequency line is no longer a sharp spike; it becomes a sinc-shaped peak.
- Energy from adjacent frequencies leaks into one another — **spectral leakage**.
- Two frequencies closer than about $1/T$ cannot be resolved.

---

## 5. The DFT combines both effects

The **discrete Fourier transform** (DFT) is the practical tool that computes the spectrum of the finite, sampled trace. For $N$ samples spaced by $\Delta t$, the DFT is

$$
\boxed{
X[k] = \sum_{n=0}^{N-1} x[n] \, e^{-i 2\pi k n / N}, \qquad k = 0, \dots, N-1
}
$$

and the inverse DFT is

$$
\boxed{
x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] \, e^{i 2\pi k n / N}
}
$$

The DFT frequency corresponding to bin $k$ is

$$
f_k = k \, \Delta f = \frac{k}{N\Delta t} = \frac{k}{T}.
$$

So the frequency spacing is

$$
\Delta f = \frac{1}{T} = \frac{1}{N\Delta t}.
$$

### DFT properties that follow from sampling and windowing

| Property | Origin | Consequence |
|---|---|---|
| Periodicity | Time-domain sampling | $X[k+N] = X[k]$; only bins $0$ to $N-1$ are produced, but the spectrum repeats every $N$ bins. |
| Real-signal symmetry | Input $x[n]$ is real | $X[-k] = X^*[k]$; only bins $0$ to $N/2$ are independent. |
| Nyquist bin | Sampling at $f_s$ | Bin $k = N/2$ corresponds to $f_N = f_s/2$. |
| Frequency resolution | Finite window length $T$ | $\Delta f = 1/T$; two frequencies closer than this cannot be separated. |
| Spectral leakage | Rectangular window | A pure frequency appears as a sinc-shaped peak and leaks into neighbouring bins. |

---

## 6. A worked example: a single cosine in a rectangular window

Consider a continuous cosine of frequency $f_0$:

$$
x(t) = \cos(2\pi f_0 t).
$$

Its continuous spectrum consists of two delta functions at $f = \pm f_0$.

### After sampling

Sampling at interval $\Delta t$ repeats the spectrum at multiples of $f_s = 1/\Delta t$. The delta functions now appear at

$$
f = f_0 + k f_s \quad \text{and} \quad f = -f_0 + k f_s,
\qquad k = 0, \pm 1, \pm 2, \dots
$$

### After windowing

Each delta function is smeared by the sinc function $W(f)$, so the spectrum becomes two sinc peaks centred at $\pm f_0$. The width of each main lobe is approximately $2/T$.

### After the DFT

The DFT evaluates this smeared spectrum at the discrete frequencies $f_k = k/T$. There are two important cases:

1. **Exact-bin case**: $f_0$ is an integer multiple of $\Delta f$, i.e. $f_0 = k_0 \Delta f$. The sinc peak is sampled exactly at its centre and at its zeros, so the DFT shows energy only in bins $k_0$ and $N-k_0$.

2. **Off-bin case**: $f_0$ is not an integer multiple of $\Delta f$. The sinc peak is sampled off-centre, so energy leaks into many neighbouring bins. This is the leakage seen in real spectral estimates.

### Numerical illustration

Take $\Delta t = 4$ ms, $N = 250$, so $T = 1.0$ s and $\Delta f = 1$ Hz.

- If $f_0 = 10$ Hz, it falls exactly on bin 10. The DFT shows energy in bin 10 and bin $N-10 = 240$ only.
- If $f_0 = 10.5$ Hz, it falls between bins 10 and 11. The DFT shows energy spread across many bins because the sinc is sampled off-centre.

This leakage is not a numerical error; it is a direct consequence of the finite window length.

---

## 7. Reducing leakage: windowing

Leakage can be reduced by multiplying the finite trace by a tapered window (e.g., Hanning, Hamming, Blackman) instead of the rectangular window. The tapered window has a wider main lobe but much lower sidelobes, so the leakage is smaller. The cost is slightly worse frequency resolution because the effective window length is reduced.

---

## 8. Summary table

| Time-domain process | Mathematical operation | Frequency-domain effect |
|---|---|---|
| Continuous signal | $x(t)$ | Continuous spectrum $X(f)$ |
| Sampling | Multiply by delta comb $\sum_n \delta(t - n\Delta t)$ | Spectrum becomes periodic with period $f_s = 1/\Delta t$; Nyquist frequency $f_N = 1/(2\Delta t)$ |
| Finite window | Multiply by rectangular window $w(t)$ | Spectrum is convolved with sinc; spectral leakage; frequency resolution $\Delta f = 1/T$ |
| DFT | Sample $N$ points and compute discrete sum | Periodic, finite set of bins; $X[k+N] = X[k]$; real-signal symmetry $X[-k] = X^*[k]$ |

---

## 9. Key takeaway

A digital seismic trace is **sampled** and **finite**. Therefore its DFT spectrum is:

1. **Periodic**, because of sampling; the Nyquist frequency is the highest unambiguous frequency.
2. **Smeared**, because of the finite window; two frequencies closer than $1/T$ cannot be separated and a pure frequency leaks into neighbouring bins.

These are not artefacts of the DFT algorithm; they are fundamental properties of moving a continuous signal into a finite digital representation. Understanding them is essential for interpreting spectra and designing filters in seismic processing.

---

## Further reading

- Section 2 of the Lecture 5 notes (`term01_lec05`) uses these ideas in the context of seismic spectra and filters.
- Hatton, Worthington & Makin (1986), Chapter 2.3 — DFT definition, periodicity, and the Nyquist criterion.
- Margrave (2006), *Methods of Seismic Data Processing*, Chapter 2 — convolution, Fourier transforms, DFT, sampling, and spectral estimation.
- Yilmaz, *Practical Seismic Data Analysis*, §1.2–1.3 — sampled time series, aliasing, and the Fourier amplitude spectrum.
