---
# Build (from paper/):
#   pandoc --citeproc -s -t beamer --slide-level=2 \
#     --include-in-header=preamble.tex \
#     rpolygon-creation-and-cut-talk.md -o rpolygon-creation-and-cut-talk.tex
#   lualatex -interaction=nonstopmode -halt-on-error rpolygon-creation-and-cut-talk.tex
#   lualatex -interaction=nonstopmode -halt-on-error rpolygon-creation-and-cut-talk.tex
title: "Even-Index Representations and Recursive Decomposition of Rectilinear Polygons"
subtitle: "Representation, monotone repair, and three-step rectangle decomposition"
author: "Wai-Shing Luk"
institute: "physdes"
date: "\\today"
theme: "Frankfurt"
aspectratio: 169
bibliography: phys_des.bib
csl: ieee.csl
link-citations: true
---

# Outline

## Outline

```{=latex}
\tableofcontents
```

# Introduction

## Rectilinear Geometry in Physical Design

- VLSI layouts are overwhelmingly **Manhattan**: every edge is horizontal or vertical.
- Rectilinear polygons model **obstacles**, **regions**, and **layout fracturing** patterns [@sherwani1999algorithms; @kahng2011vlsi].
- Coordinates are **integers**; rounding is not merely inaccurate but illegal.
- The polygons of interest are small: $n \le 100$ vertices.
- Consequently, **quadratic algorithms are acceptable**; clarity and exactness dominate.

## Problem Statement and Contributions

**Input.** A simple rectilinear polygon $P$ and its even-index encoding
$S=(s_0,\ldots,s_{m-1})$ with $s_i\in\mathbb{Z}^2$.

**Tasks.**

1. A compact even-index representation and its local structural condition.
2. Monotone repair and betweenness-safe collinear cleanup that preserve the
   represented polygon.
3. A three-step rectangle decomposition: convex decomposition, explicit
   $270^\circ$ handling, and implicit $270^\circ$ handling.
4. C++20 implementation and verification.

**Contributions.** The local condition of the encoding, the compressed area
formula, a betweenness-safe cleanup, a three-step rectangle decomposition, and
output-class tests that area checks alone cannot replace.

# Representation

## Full Boundary and Even-Index Encoding

:::: {.columns}
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.62, font=\scriptsize]
  \draw[thick, fill=nordblue!18] (0,0)--(4,0)--(4,4)--(3,4)--(3,1)--(1,1)--(1,4)--(0,4)--cycle;
  \foreach \p in {(0,0),(4,0),(4,4),(3,4),(3,1),(1,1),(1,4),(0,4)} \fill[nordblue] \p circle[radius=2.2pt];
  \node[below left] at (0,0) {$v_0$};
  \node[below right] at (4,0) {$v_1$};
  \node[above right] at (4,4) {$v_2$};
  \node[above] at (3,4) {$v_3$};
  \node[right] at (3,1) {$v_4$};
  \node[left] at (1,1) {$v_5$};
  \node[above] at (1,4) {$v_6$};
  \node[above left] at (0,4) {$v_7$};
\end{tikzpicture}
\end{center}
```
:::
::: {.column width="48%"}
```{=latex}
\begin{center}
\includegraphics[width=0.9\linewidth,height=0.42\textheight,keepaspectratio]{figures/fig_even_index.pdf}
\end{center}
```
:::
::::

**Definition.** For a full boundary $V=(v_0,\ldots,v_{n-1})$ with $n$ even, the
even-index encoding is $S=(v_0,v_2,\ldots,v_{n-2})$.

- The odd-index vertices are implicit; only $m=n/2$ points are stored.
- The represented polygon is recovered by the x-first rule below.

## x-First Expansion

```{=latex}
\begin{center}
\begin{tikzpicture}[scale=1.0, font=\scriptsize]
  \draw[->] (-0.3,0)--(3.7,0) node[right] {$x$};
  \draw[->] (0,-0.3)--(0,2.7) node[above] {$y$};
  \fill[nordblue] (0,0) circle[radius=2.5pt] node[below left] {$S_i=(x_0,y_0)$};
  \fill[nordblue] (3,2) circle[radius=2.5pt] node[above right] {$S_{i+1}=(x_1,y_1)$};
  \fill[nordpurple] (3,0) circle[radius=2.0pt] node[below right] {$I_i=(x_1,y_0)$};
  \draw[nordred, dashed, thick] (0,0)--(3,2);
  \draw[thick] (0,0)--(3,0)--(3,2);
\end{tikzpicture}
\end{center}
```

**Definition (x-first expansion).** For consecutive stored points
$S_i=(x_0,y_0)$ and $S_{i+1}=(x_1,y_1)$, insert
$$I_i=(x_{i+1},y_i)$$
before $S_{i+1}$, including the closing pair $S_{m-1}\to S_0$.

- The diagonal chord $S_iS_{i+1}$ is **not** a boundary edge.
- The y-first form $(x_0,y_1)$ reconstructs a different polygon.

## Minimal Encodings

:::: {.columns}
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.82, font=\scriptsize]
  \draw[thick, fill=nordblue!15] (0,0)--(3,0)--(3,2)--(0,2)--cycle;
  \fill[nordblue] (0,0) circle[radius=2.5pt] node[below left] {$S_0$};
  \fill[nordblue] (3,2) circle[radius=2.5pt] node[above right] {$S_1$};
  \fill[nordpurple] (3,0) circle[radius=2pt];
  \fill[nordpurple] (0,2) circle[radius=2pt];
\end{tikzpicture}
\end{center}
```
:::
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.82, font=\scriptsize]
  \draw[thick, fill=nordblue!15] (0,0)--(3,0)--(3,2)--(1,2)--(1,3)--(0,3)--cycle;
  \fill[nordblue] (0,0) circle[radius=2.5pt] node[below left] {$S_0$};
  \fill[nordblue] (3,2) circle[radius=2.5pt] node[right] {$S_1$};
  \fill[nordblue] (1,3) circle[radius=2.5pt] node[above] {$S_2$};
  \fill[nordpurple] (3,0) circle[radius=2pt];
  \fill[nordpurple] (1,2) circle[radius=2pt];
  \fill[nordpurple] (0,3) circle[radius=2pt];
\end{tikzpicture}
\end{center}
```
:::
::::

- **2 stored points** represent a rectangle: $E(S)$ has four corners.
- **3 stored points** represent a monotone / $L$-shaped piece: six corners.
- These are not degenerate cases; they are the base cases of the decomposition.

**Local condition.** For a simple input polygon, every cyclic consecutive pair
of stored points differs in both coordinates. This is a property of the
encoding, not a validity test; simplicity is an assumption on the input.

## Local Condition

**Definition.** A stored sequence $S=(s_0,\ldots,s_{m-1})$ satisfies the
**local condition** if

1. $m\ge 2$ and the $s_i$ are pairwise distinct, and
2. for every $i$ (indices modulo $m$),
$$x_i \ne x_{i+1}\quad\text{and}\quad y_i \ne y_{i+1}.$$

```text
if |S| < 2: return false
if duplicate points: return false
for each cyclic pair:
    if same x or same y: return false
return true
```

- The implementation keeps the name `is_canonical`; the paper calls this the
  local condition (admissibility).
- Duplicate detection is $O(m^2)$ naively, or $O(m\log m)$ by sorting.
- The consecutive-pair test is $O(m)$.

## Local Condition and Repair

:::: {.columns}
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.82, font=\scriptsize]
  \draw[thick, fill=nordblue!15] (2,1)--(2,0)--(3,0)--(3,-3)--(2,-3)--cycle;
  \draw[nordred, line width=2pt] (2,1)--(2,0);
  \draw[nordred, line width=2pt] (2,-3)--(2,1);
  \fill[nordblue] (2,1) circle[radius=2.5pt] node[above right] {$S_0$};
  \fill[nordblue] (2,0) circle[radius=2.5pt] node[right] {$S_1$};
  \fill[nordblue] (3,-3) circle[radius=2.5pt] node[right] {$S_2$};
  \fill[nordpurple] (3,0) circle[radius=2pt];
  \fill[nordpurple] (2,-3) circle[radius=2pt];
  \node[nordred, below] at (2.5,-3.6) {not locally admissible};
\end{tikzpicture}
\end{center}
```
:::
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.82, font=\scriptsize]
  \draw[thick, fill=nordgreen!18] (2,1)--(3,1)--(3,-3)--(2,-3)--cycle;
  \fill[nordblue] (2,1) circle[radius=2.5pt] node[above left] {$S_0$};
  \fill[nordblue] (3,-3) circle[radius=2.5pt] node[right] {$S_1$};
  \fill[nordpurple] (3,1) circle[radius=2pt];
  \fill[nordpurple] (2,-3) circle[radius=2pt];
  \node[nordgreen!45!black, below] at (2.5,-3.6) {locally admissible};
\end{tikzpicture}
\end{center}
```
:::
::::

- $S=((2,1),(2,0),(3,-3))$ fails the local condition: the expansion contains
  two consecutive vertical segments.
- Its repaired form is $((2,1),(3,-3))$.
- Area alone cannot detect this defect; the local condition is **structural**.
- For a simple input polygon, the local condition holds by Lemma 1; no global
  check is needed.

## Orientation and Signed Area

For a simple polygon with vertices $(x_i,y_i)$,

$$A=\frac12\sum_i\left(x_i y_{i+1}-x_{i+1}y_i\right).$$

- $A>0$: anticlockwise; $A<0$: clockwise.
- The even-index encoding admits an $O(m)$ evaluation over the stored points.
- The sign drives the repair and cut branches and serves as a cheap
  postcondition.

**Lemma.** The signed area is invariant under the x-first expansion $E$.

*Proof sketch.* Each inserted vertex is collinear with an axis-aligned edge and
contributes zero net area. $\square$

## Creation Outputs Are Not Locally Admissible

```{=latex}
\begin{center}
\includegraphics[width=0.48\linewidth]{figures/f-noncanonical-xmono.pdf}\hfill
\includegraphics[width=0.48\linewidth]{figures/f-noncanonical-ymono.pdf}
\end{center}
```

- Raw creation orderings contain consecutive collinear triples.
- The monotone repair and cleanup turn them into locally admissible encodings.

# Monotone Hulls and Repair

## Monotonicity and Convexity

```{=latex}
\begin{center}
\includegraphics[width=0.9\linewidth]{figures/fig_monotone.pdf}
\end{center}
```

**Definition.** A rectilinear polygon is $x$-monotone if every vertical line
meets it in a single interval; $y$-monotone is defined symmetrically.

**Lemma.** A rectilinear polygon is orthogonally convex if and only if it is
both $x$-monotone and $y$-monotone.

## Monotone Hulls and Repair Algorithm

- Let $p,c,n$ be the previous, current, and next stored vertices.
- A vertex is removed when monotonicity is violated and the turn has the wrong
  sign:
$$\Delta=(y_c-y_p)(x_n-x_c).$$
- A circular doubly-linked list makes removal $O(1)$.
- Two passes: minimum to maximum, then maximum to minimum.

```text
for c in chain:
    if dir(c) > dir(n) or dir(p) > dir(c):
        if wrong_sign(Delta):
            remove(c); c = prev(c)
        else:
            c = next(c)
    else:
        c = next(c)
```

**Complexity.** Each sweep is $O(m)$; the betweenness-safe cleanup is $O(m^2)$
worst case, so the composed repair is $O(m^2)$.

## Collinear Cleanup

:::: {.columns}
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.70, font=\scriptsize]
  \draw[thick] (-0.5,0)--(3,0)--(3,2);
  \fill[nordblue] (-0.5,0) circle[radius=2pt] node[below left] {$s_i$};
  \fill[nordred] (1.5,0) circle[radius=2pt] node[below] {$s_{i+1}$};
  \fill[nordblue] (3,2) circle[radius=2pt] node[right] {$s_{i+2}$};
  \draw[nordred, dashed, ->] (1.5,0)--(1.5,-0.6) node[below] {drop};
  \node[below] at (1.2,-1.0) {same $y$: drop the second};
\end{tikzpicture}
\end{center}
```
:::
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.70, font=\scriptsize]
  \draw[thick] (-2,0)--(0,0)--(0,4)--(2,5);
  \fill[nordblue] (-2,0) circle[radius=2pt] node[left] {$s_{i-1}$};
  \fill[nordred] (0,1) circle[radius=2pt] node[right] {$s_i$};
  \fill[nordblue] (0,4) circle[radius=2pt] node[right] {$s_{i+1}$};
  \fill[nordblue] (2,5) circle[radius=2pt] node[right] {$s_{i+2}$};
  \draw[nordred, dashed, ->] (0,1)--(1,1) node[right] {drop};
  \node[below] at (0,-0.4) {same $x$: drop the first};
\end{tikzpicture}
\end{center}
```
:::
::::

- A same-$y$ pair drops the second point when it lies strictly between its
  neighbours; a same-$x$ pair drops the first analogously.
- If no removable point remains but an adjacent pair still shares an axis, the
  list is not admissible.
- Under betweenness, cleanup preserves the boundary and area; otherwise it
  reports failure.

## Hull Composition and Repair

```{=latex}
\begin{center}
\includegraphics[width=0.72\linewidth,height=0.52\textheight,keepaspectratio]{figures/f-hull.pdf}
\end{center}
```

- $x$-hull then $y$-hull yields the rectilinear convex hull.
- Hulls also give monotone enclosures and preprocessing for decomposition.
- The same passes repair raw creation orderings.
- The output is checked for the local condition and monotonicity; the composed
  cost is $O(m^2)$ worst case.

# Recursive Decomposition

## Three-Step Decomposition

```{=latex}
\begin{center}
\begin{tikzpicture}[node distance=3.5mm, font=\scriptsize]
  \node[nyellow] (p) {Rectilinear\\polygon};
  \node[nblue, right=of p] (c) {Convex\\cut};
  \node[ngreen, right=of c] (e) {Explicit\\270};
  \node[nred, right=of e] (i) {Implicit\\270};
  \node[nblue, right=of i] (r) {Rectangle\\pieces};
  \draw[ar] (p)--(c); \draw[ar] (c)--(e); \draw[ar] (e)--(i); \draw[ar] (i)--(r);
\end{tikzpicture}
\end{center}
```

- **Step 1: convex cut.** Remove concavities; simplify the remaining geometry.
- **Step 2: explicit $270^\circ$.** Resolve reflex corners that are stored vertices.
- **Step 3: implicit $270^\circ$.** Resolve reflex corners introduced by expansion.
- Steps 2 and 3 repeat until neither type remains; the final pieces are
  rectangles, suitable for layout fracturing and DRC
  [@kahng2008layout; @liebmann2003layout].

## Cut Primitive

```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.62, font=\scriptsize]
  \begin{scope}
    \draw[thick, fill=nordblue!15] (0,0)--(3,0)--(3,3)--(2,3)--(2,1)--(1,1)--(1,3)--(0,3)--cycle;
    \draw[nordred, line width=1.5pt] (2,1) circle[radius=3pt];
    \draw[nordred, line width=1.5pt] (1,1) circle[radius=3pt];
    \node[below] at (1.5,-0.4) {(a) concave vertices};
  \end{scope}
  \begin{scope}[xshift=4.4cm]
    \draw[thick, fill=nordblue!15] (0,0)--(3,0)--(3,3)--(2,3)--(2,1)--(1,1)--(1,3)--(0,3)--cycle;
    \draw[nordred, dashed, thick] (2,1)--(2,0);
    \draw[nordred, dashed] (2,1)--(1,1);
    \fill[nordred] (2,0) circle[radius=2pt];
    \node[below] at (1.5,-0.4) {(b) minimum cut};
  \end{scope}
  \begin{scope}[xshift=8.8cm]
    \fill[nordgreen!35] (0,0)--(2,0)--(2,1)--(1,1)--(1,3)--(0,3)--cycle;
    \fill[nordpurple!35] (2,0)--(3,0)--(3,3)--(2,3)--(2,1)--cycle;
    \draw[thick] (0,0)--(2,0)--(2,1)--(1,1)--(1,3)--(0,3)--cycle;
    \draw[thick] (2,0)--(3,0)--(3,3)--(2,3)--(2,1)--cycle;
    \node[below] at (1.5,-0.4) {(c) split and recurse};
  \end{scope}
\end{tikzpicture}
\end{center}
```

- Find a concave vertex: a direction reversal with the correct area sign.
- Project $v$ onto each edge; choose the nearest visible edge and insert the
  intersection point.
- Splice the new node, split the circular list, and recurse on both pieces.

## Convex Decomposition Example

```{=latex}
\begin{center}
\includegraphics[width=0.85\linewidth,height=0.50\textheight,keepaspectratio]{figures/fig_convex_example.pdf}
\end{center}
```

- Three orthogonally convex pieces.
- Areas $1,9,10$; total area $20$.

## Base Cases and Recursion

**Base cases.**

- 2 stored points: a rectangle; stop.
- 3 stored points: a monotone / $L$-shaped piece; stop in the convex variant.
- The explicit variant has no 3-point base case; it continues until no concave
  vertex remains.

```text
cut(v1):
    v2, v3 = v1.next, v1.next.next
    if v3 == v1:
        return [v1, v2]
    if triangle_base and v3.next == v1:
        return [v1, v2, v3]
    c = find_concave(v1)
    if c is None:
        return all_vertices(v1)
    vmin, vertical = find_min_dist(c)
    new = insert_cut(c, vmin, vertical)
    return cut(c) + cut(new)
```

**Complexity.** Each cut adds $O(1)$ list surgery; there are $O(n)$ cuts, so the
total is $O(n^2)$. A degenerate two-node split handles a cut that duplicates an
adjacent vertex.

## Explicit and Implicit 270° Vertices

```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.78, font=\scriptsize]
  \draw[thick, fill=nordblue!15] (0,0)--(3,0)--(3,3)--(2,3)--(2,1)--(1,1)--(1,3)--(0,3)--cycle;
  \fill[nordblue] (0,0) circle[radius=2.4pt];
  \fill[nordblue] (3,3) circle[radius=2.4pt];
  \fill[nordblue] (2,1) circle[radius=2.4pt] node[below right] {explicit};
  \fill[nordblue] (1,3) circle[radius=2.4pt];
  \fill[nordpurple] (3,0) circle[radius=2pt];
  \fill[nordpurple] (2,3) circle[radius=2pt];
  \fill[nordpurple] (1,1) circle[radius=2pt] node[above left] {implicit};
  \fill[nordpurple] (0,3) circle[radius=2pt];
\end{tikzpicture}
\end{center}
```

- **Explicit $270^\circ$:** the reflex corner is a stored even-index vertex.
- **Implicit $270^\circ$:** the reflex corner is created by the x-first expansion.
- The same compressed U-shape contains both kinds.
- The convex cut handles the shape; the explicit and implicit cuts handle the
  corner types.

## Implicit Cut of an L-Shape

```{=latex}
\begin{center}
\includegraphics[width=0.62\linewidth,height=0.48\textheight,keepaspectratio]{figures/fig_implicit_l.pdf}
\end{center}
```

- The implicit corner $(1,1)$ is reflex.
- A horizontal cut yields rectangles of areas $2$ and $1$.

## Rectangle Output and Local Condition

- A rectangle piece has **2 stored points**: two opposite corners.
- The local condition for a 2-point list is exactly
  `x_0 != x_1` and `y_0 != y_1`.
- The three-step algorithm outputs rectangles; the tests assert the two-point
  form, the local condition, and the area.
- For larger intermediate pieces, the local condition and orthogonal convexity
  are checked on the expanded boundary.

## Rectangle Decomposition

```{=latex}
\begin{center}
\includegraphics[width=0.82\linewidth,height=0.52\textheight,keepaspectratio]{figures/fig_rect7.pdf}
\end{center}
```

- Seven rectangles, areas $1,1,2,2,4,4,6$.
- Total area $20$.

## Correctness Invariants and Complexity

**Invariants.**

1. **Area:** the sum of signed piece areas equals the signed area of the input.
2. **Rectangle output:** the three-step algorithm returns two-point rectangles.
3. **Local condition:** checked on the expanded boundary.

**Complexity.**

| operation | cost |
|:----------|:-----|
| concave-vertex scan | $O(n)$ |
| nearest-edge scan | $O(n)$ |
| insert / split | $O(1)$ |
| total decomposition | $O(n^2)$ |

For $n\le 100$, quadratic time is preferable to a complicated sub-quadratic
implementation.

# Verification

## Implementation and Tests

**C++20 (xmake)**

- `xmake build test_recti`
- `xmake run test_recti`
- **142 test cases**
- **962 assertions**
- **0 failures**

- The repair is applied before the local-condition check; raw creation is only
  an ordering, not a polygon.
- The tests assert the output class: local condition, orthogonal convexity,
  and rectangle shape.
- A bridged-hole fixture is cut into three pieces of areas 2, 15, and 10;
  the area is preserved.
- Two AGPLIB polygons and the bridged-hole fixture are tested in C++.

## Limitations and Threats to Validity

1. **Local condition.** It is a property of the encoding; simplicity is an
   assumption on the input.
2. **Synthetic inputs.** The evaluation uses generated point sets and hand-built
   fixtures, not foundry data; the claims are algorithmic, not signoff.
3. **Quadratic scaling.** Decomposition is $O(n^2)$; for $n\le 100$ this is
   appropriate, and sub-quadratic methods are not addressed here.
4. **No optimality claim.** The three-step algorithm returns a rectangle
   partition, not a minimum-cardinality one.
5. **Robustness.** Integer arithmetic is exact; degenerate input handling beyond
   the stated invariants is outside the present scope
   [@edelsbrunner1990sos].

## Polygons with Holes

```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.9, font=\scriptsize]
  \draw[thick, fill=nordblue!15] (0,0) rectangle (4,4);
  \draw[thick, fill=white] (1.5,1.5) rectangle (2.5,2.5);
  \draw[nordred, dashed, line width=1.4pt] (4,2)--(2.5,2);
  \node[nordred, above] at (3.25,2.05) {bridge};
  \node[below] at (2,0) {outer boundary};
  \node[below] at (2,1.45) {hole};
\end{tikzpicture}
\end{center}
```

- A bridge cut from the outer boundary to a hole merges the boundaries into a
  single cycle; a zero-width bridge gives a weakly simple boundary, a narrow
  bridge gives a simple one.
- The bridge is traversed in both directions, so the area is unchanged.
- The even-index encoding and the cut algorithms then apply; repeated bridge
  vertices are handled by the degenerate split.
- This is standard boundary bookkeeping, not specific to the even-index
  representation.

# Conclusion

## Contributions and Open Problems

**Contributions.**

- A local structural condition for the encoding.
- A monotone-repair pass with betweenness-safe collinear cleanup.
- A three-step rectangle decomposition: convex decomposition, explicit
  $270^\circ$ handling, and implicit $270^\circ$ handling.
- Output-class tests and C++20 verification.

**Open problems.**

- A formal proof that the compressed predicate characterizes orthogonal
  convexity.
- Minimum-cardinality rectangle partitioning.
- Cross-language differential testing on random polygons.

## Q&A

- Code: `physdes-cpp` under the `luk036` organization.
- Thank you.

## References {.allowframebreaks}
