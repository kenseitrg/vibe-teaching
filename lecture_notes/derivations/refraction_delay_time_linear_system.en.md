# Delay-time derivation for refraction statics

## 1. Two-layer refraction geometry

Consider a flat two-layer model:

- Layer 1 (weathering): velocity $V_1$, thickness $h$.
- Layer 2 (sub-weathering): velocity $V_2 > V_1$.

A source at $S$ and a receiver at $R$ are separated by offset $X$. At offsets larger than the **crossover distance**, the first arrival is a head wave that travels along the base of the weathering layer.

The ray path of the head wave is:

1. Down from the source to the base of the weathering layer at the **critical angle** $i_c$.
2. Horizontally along the interface at velocity $V_2$.
3. Up to the receiver at the critical angle $i_c$.

From Snell’s law at the critical refraction point,

$$\sin i_c = \frac{V_1}{V_2}.$$

## 2. Traveltime of the refracted head wave

The downgoing and upgoing segments inside the weathering layer each have length $h / \cos i_c$, so each takes time

$$t_{\text{down}} = t_{\text{up}} = \frac{h}{V_1 \cos i_c}.$$

The horizontal projection of each slanted segment is $h \tan i_c$, so the horizontal distance travelled at the higher velocity $V_2$ is

$$X_{\text{high}} = X - 2 h \tan i_c.$$

The traveltime along this segment is

$$t_{\text{high}} = \frac{X - 2 h \tan i_c}{V_2}.$$

Adding the three pieces gives the total refracted traveltime:

$$T_{\text{ref}}(X) = \frac{X - 2 h \tan i_c}{V_2} + \frac{2 h}{V_1 \cos i_c}.$$

Rearranging,

$$T_{\text{ref}}(X) = \frac{X}{V_2} + 2 h \left(\frac{1}{V_1 \cos i_c} - \frac{\tan i_c}{V_2}\right).$$

Using $\tan i_c = \sin i_c / \cos i_c$ and $\sin i_c = V_1 / V_2$, the term in parentheses simplifies:

$$\frac{1}{V_1 \cos i_c} - \frac{\sin i_c}{V_2 \cos i_c} = \frac{1}{V_1 \cos i_c} - \frac{V_1}{V_2^2 \cos i_c} = \frac{1}{V_1 \cos i_c}\left(1 - \frac{V_1^2}{V_2^2}\right) = \frac{\cos i_c}{V_1}.$$

Therefore the refracted traveltime is

$$T_{\text{ref}}(X) = \frac{X}{V_2} + \frac{2 h \cos i_c}{V_1}.$$

The second term is independent of offset $X$ and depends only on the near-surface properties at the source and receiver.

## 3. Source and receiver delay times

It is convenient to split the offset-independent term into a **source delay time** $\tau_S$ and a **receiver delay time** $\tau_R$:

$$\tau_S = \frac{h_S \cos i_c}{V_1}, \qquad \tau_R = \frac{h_R \cos i_c}{V_1},$$

where $h_S$ and $h_R$ are the weathering thicknesses beneath the source and receiver locations. Then

$$T_{\text{ref}}(X) = \frac{X}{V_2} + \tau_S + \tau_R.$$

Equivalently, the **delay time** is the difference between the observed refracted traveltime and the time that would be spent travelling the same horizontal distance at the sub-weathering velocity $V_2$:

$$\tau_S + \tau_R = T_{\text{ref}}(X) - \frac{X}{V_2}.$$

This isolates the near-surface contribution and is the basis for refraction statics.

## 4. From delay time to weathering thickness

Once the delay time $\tau$ at a surface location is known, the weathering thickness is recovered from

$$h = \frac{\tau V_1}{\cos i_c}.$$

The static correction to apply to a trace recorded at that location is the difference between the actual near-surface traveltime and the traveltime that would be observed if the weathering layer were replaced by the replacement velocity $V_\text{rep}$.

## 5. System of linear equations

In a field survey, refracted first arrivals are picked for many source–receiver pairs. For each pair $(i, j)$ with source $i$, receiver $j$, and offset $X_{ij}$, the observed first-arrival time $T_{ij}$ can be written as

$$T_{ij} = \frac{X_{ij}}{V_2} + \tau_i + \tau_j + \epsilon_{ij},$$

where $\epsilon_{ij}$ is the pick noise or model error. If $V_2$ is known from separate analysis (or assumed), the unknowns are the source and receiver delay times $\tau_i$ and $\tau_j$. Because the same $\tau_i$ appears for every trace that uses source $i$ (and similarly for receiver $j$), the whole data set forms an **overdetermined linear system**:

$$\mathbf{G} \boldsymbol{\tau} = \mathbf{d}.$$

Here:

- $\mathbf{d}$ is the vector of observed traveltimes minus the $X/V_2$ contribution.
- $\boldsymbol{\tau}$ is the vector of unknown delay times at all source and receiver surface locations.
- $\mathbf{G}$ is the design matrix with one row per trace; each row contains two ones in the columns corresponding to the source and receiver delay times.

The system is usually solved by least squares, minimizing $\|\mathbf{G}\boldsymbol{\tau} - \mathbf{d}\|^2$ plus any regularization that enforces smoothness or ties the solution to uphole control.

## 6. Classical near-surface modelling methods

Several practical methods solve this linear system, or variants of it, with different assumptions:

- **Hagedoorn plus–minus (ABC) method.** Uses a pair of reciprocal shots and a common receiver between them. The plus term gives the delay time directly from the sum of reciprocal traveltimes, and the minus term gives the sub-weathering velocity. It is analytically simple but needs reciprocal coverage.

- **Generalized Reciprocal Method (GRM).** Extends the ABC idea to non-reciprocal geometry and layered models. It estimates delay times and the sub-weathering velocity by searching for the offset at which the refracted arrivals are most symmetric.

- **Generalized Linear Inversion (GLI).** Solves the full linear system $\mathbf{G}\boldsymbol{\tau} = \mathbf{d}$ by least squares. It can handle arbitrary acquisition geometry, layer velocities, and inequality constraints, and it is the basis for most modern refraction-statics software.

Modern extensions add **diving-wave tomography** and **full-waveform inversion (FWI)** to refine the near-surface model beyond the simple two-layer delay-time approximation.

## 7. Summary

- The refracted head-wave traveltime is the sum of a horizontal-distance term $X/V_2$ and source/receiver delay times.
- Delay times isolate the near-surface effect and are related to weathering thickness by $h = \tau V_1 / \cos i_c$.
- A survey of refraction picks yields a sparse, overdetermined linear system for the unknown delay times.
- Classical methods (ABC, GRM) and modern least-squares inversion (GLI) are different ways of solving this system.
