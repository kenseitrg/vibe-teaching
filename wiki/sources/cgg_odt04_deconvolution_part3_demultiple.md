---
title: CGG ODT04 Part 3 — Deconvolution as De-multiple
type: training slides
year: 2015
author: CGG (internal training)
source_file: papers/deconvolution/ODT04_DECONVOLUTION_PART3_v7.0_deconvolution_demult.pptx
status: reviewed
tags: [demultiple, predictive-deconvolution, water-layer-reverberation, ghosts, marine]
---

# CGG ODT04 Part 3 — Deconvolution as De-multiple

## Source

- **Author:** CGG UK Training
- **Title:** ODT04 Deconvolution Part 3: Deconvolution as De-multiple
- **Version:** 7.0, June 2015
- **Type:** Internal training slides
- **File:** `papers/deconvolution/ODT04_DECONVOLUTION_PART3_v7.0_deconvolution_demult.pptx`

**Note:** Internal CGG training document; images do not have show rights. Use for understanding and structure.

## Main message

Spiking deconvolution can serve dual purposes: (1) compressing the wavelet to improve resolution (signature deconvolution), and (2) attenuating short-period multiples when the operator length extends to include the multiple period in the autocorrelation. Predictive deconvolution separates these two goals, allowing controlled-phase processing without wavelet compression.

## Key points

### 1. Deconvolution as de-multiple

- **Short operator** (covers only wavelet portion of ACF): performs signature deconvolution only.
- **Long operator** (extends to include first multiple period in ACF): performs signature deconvolution AND de-multiple simultaneously.
- The ACF of the seismic includes correlation between multiples separated by one period. A longer operator exploits this to collapse all multiple orders to a single spike.
- **1D assumption:** predictive deconvolution assumes multiples are exact time-shifted copies of primaries. In reality, this breaks down at non-zero offset (moveout differences).

### 2. Predictive deconvolution

- After zero-phasing, we have a zero-phase wavelet that we don't want to disturb.
- **Goal:** remove multiples without changing the wavelet or boosting noise.
- **Approach:** design an operator that predicts the multiple from the primary (shifts by multiple period, matches amplitude).
- **Prediction gap (α):** the time lag at which we start predicting. For water-bottom multiple at two-way time T, set α ≈ T.
- **Operator length:** must be long enough to capture the predictive relationship.
- **Result:** the predictive filter outputs the predicted multiple, which is then adaptively subtracted from the data.

### 3. Relationship between ghosts and multiples

- Ghosts are a special case of short-period multiples.
- Source ghost: reflection at sea surface of upward source energy.
- Receiver ghost: reflection at sea surface of upward recorded energy.
- Both are multiples with very short periods (period = 2 × depth / velocity).
- **Key insight:** ghosts modify the wavelet itself, so they are removed by designature (signature deconvolution), not by predictive deconvolution.
- Predictive deconvolution is for longer-period multiples (water-bottom reverberations, internal multiples).

### 4. Practical workflow

Typical marine processing flow:
1. **De-bubble** (if bubble energy is significant).
2. **Zero-phase conversion** (or spiking decon with caution).
3. **Predictive deconvolution** (for water-layer multiples).
4. **Deghosting** (for receiver/source ghosts — separate step, not handled by predictive decon).

### 5. Limitations

- Predictive deconvolution assumes multiples are predictable (stationary, linear).
- Breaks down for:
  - Non-zero offset (moveout differences between primary and multiple).
  - Non-stationary multiples (velocity changes, depth variations).
  - Internal multiples (not related to water layer).
- For these cases, more advanced methods are needed (SRME, Radon filtering, etc.).

## Key equations

**Wiener filter for predictive deconvolution:**

$$
\mathbf{R} \mathbf{a} = \mathbf{r}
$$

where:
- $\mathbf{R}$ is the autocorrelation matrix of the input (from seismic ACF).
- $\mathbf{a}$ is the predictive filter vector.
- $\mathbf{r}$ is the cross-correlation vector at lag α (prediction gap).

**Prediction error filter:**

$$
e(t) = x(t) - \sum_{k=1}^{L} a_k x(t - k - \alpha + 1)
$$

where α is the prediction gap, L is the operator length.

## Practical implications

- **Operator length choice:** short operator = signature decon only; long operator = signature decon + demultiple.
- **Prediction gap:** controls which multiples are targeted. For water-bottom at T = 200 ms, set α ≈ 200 ms.
- **Pre-whitening:** needed to stabilize the operator, but reduces bandwidth and resolution.
- **Separate deghosting:** ghosts are part of the wavelet, so they require designature, not predictive decon.

## Implications for teaching

- Excellent source for understanding the dual role of spiking deconvolution (signature + demultiple).
- Clarifies the distinction between ghosts (wavelet effect → designature) and longer-period multiples (predictable → predictive decon).
- Provides concrete examples of ACF behavior with multiples.
- Explains why predictive deconvolution is 1D and breaks down at offset.

## Concepts informed

- [Marine deghosting](../concepts/marine_deghosting.md)
- [Predictive deconvolution](../concepts/predictive_deconvolution.md)
- [Deconvolution](../concepts/deconvolution.md)
- [Statistical deconvolution](../concepts/statistical_deconvolution.md)

## Quotes / memorable lines

> "So spiking deconvolution can be used to improve resolution and to perform de-multiple."

> "Short operators will do signature deconvolution. Extending the length of the operator to include the multiple in the autocorrelation will both perform signature deconvolution and de-multiple."

> "Deconvolution is strictly 1D, because in reality we know this is not true. For example, even for a 1D earth model we know as soon as we move away from zero offset then the timing between multiples begins to change."

> "One definition of a short period multiple is where the multiple period is short enough that we can treat the multiple as part of the wavelet."
