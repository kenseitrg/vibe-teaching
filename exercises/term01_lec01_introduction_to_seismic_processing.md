# Exercises — Term 1 Lecture 1: Introduction to seismic data processing

## Concept-check questions

1. **Processing goal.** In your own words, explain the main goal of seismic data processing. Why can we not interpret the raw records directly?

2. **Kinematic vs dynamic.** For each task below, decide whether it is mainly a kinematic or a dynamic problem:
   - (a) Correcting reflection arrival times for near-surface delays.
   - (b) Compensating for amplitude decay with distance from the source.
   - (c) Flattening a hyperbolic reflection in a CMP gather.
   - (d) Removing a free-surface multiple.
   - (e) Moving a dipping reflector to its correct subsurface position.

3. **Signal or noise?** Classify each event as "usually signal", "usually noise", or "depends on the task":
   - Primary reflection from a target horizon.
   - Water-bottom multiple.
   - Ground roll.
   - First-break refraction.
   - Random background noise.

4. **CMP method.** Why does recording the same subsurface point at many different offsets help us estimate velocities and improve signal-to-noise ratio?

## Numerical problems

5. **Fold calculation.** A 2D marine survey uses 180 channels, a receiver group interval of 12.5 m, and a shot interval of 25 m.
   - (a) What is the CMP spacing?
   - (b) What is the moveup?
   - (c) What is the nominal fold?

6. **Acquisition parameters.** A land 2D line has a receiver interval of 25 m and a source interval of 50 m. There are 120 channels per shot.
   - (a) What is the CMP spacing?
   - (b) What is the moveup?
   - (c) What is the nominal fold?
   - (d) If the shot interval is reduced to 25 m while everything else stays the same, what is the new fold?

## Short discussion

7. **Geometry assignment.** Why is it dangerous to start velocity analysis or stacking before geometry has been checked? Give one concrete example of what can go wrong.

8. **Processing phases.** Describe a realistic situation in which a processor would iterate between kinematic and dynamic processing rather than running them strictly one after another.

## Optional mini-project

9. **Inspect a SEG-Y header.** If you have access to a small SEG-Y file (or a demo file provided by the instructor), use a Python snippet with ObsPy or segyio to print the first few trace headers. Identify:
   - shot/receiver line and point numbers (if present);
   - source and receiver X, Y coordinates;
   - offset;
   - number of samples and sample interval.

   Comment on whether the header values look physically reasonable for a 2D line.

---

## Answers

1. The goal is to remove or compensate for acquisition effects and wave-propagation phenomena so that the remaining data represent geology as faithfully as possible. Raw records contain source wavelets, noise, multiples, static shifts, amplitude decay, etc., all of which mask the underlying reflectivity.

2. (a) kinematic; (b) dynamic; (c) kinematic; (d) dynamic (amplitudes/multiples); (e) kinematic.

3. Primary reflection — signal; water-bottom multiple — usually noise; ground roll — usually noise; first-break refraction — depends (noise for stacking, signal for statics); random background noise — noise.

4. Different offsets give different normal moveout, from which velocity can be estimated. After NMO correction, aligned traces stack constructively for signal and suppress uncorrelated random noise by roughly $\sqrt{N}$.

5. (a) 6.25 m; (b) 4; (c) $180 / (2 \times 4) = 22.5$ → effective nominal fold is 22 or 23 depending on exact geometry.

6. (a) 12.5 m; (b) 2; (c) $120 / (2 \times 2) = 30$; (d) with shot interval 25 m, moveup = 1, fold = $120 / (2 \times 1) = 60$.

7. If geometry is wrong, traces are assigned to incorrect CMPs and offsets. For example, a mis-mapped shot point number shifts whole CMP gathers, producing a discontinuity in the stack or wrong stacking velocities.

8. After an initial velocity analysis and NMO, demultiple may reveal primary energy that was previously masked. The improved signal can support a refined velocity pick, which in turn improves migration. This loop is common in modern processing.
