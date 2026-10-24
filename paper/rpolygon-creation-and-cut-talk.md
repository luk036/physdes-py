---
# Build (from paper/):
#   pandoc --citeproc -s -t beamer --slide-level=2 \
#     --include-in-header=preamble.tex \
#     rpolygon-creation-and-cut-talk.md -o rpolygon-creation-and-cut-talk.tex
#   lualatex -interaction=nonstopmode -halt-on-error rpolygon-creation-and-cut-talk.tex
#   lualatex -interaction=nonstopmode -halt-on-error rpolygon-creation-and-cut-talk.tex
title: "Canonical Even-Index Representations and Recursive Decomposition of Rectilinear Polygons"
subtitle: "Representation, monotone hulls, and exact canonical verification"
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

**Input.** A point sequence $S=(s_0,\ldots,s_{m-1})$ with $s_i\in\mathbb{Z}^2$.

**Tasks.**

1. A canonical representation with an exact structural predicate.
2. Monotone and convex hulls that preserve the represented polygon.
3. Recursive decomposition into convex pieces and rectangles.
4. Cross-language verification (Python and C++20).

**Contributions.** A template-method treatment of $x$ and $y$, a collinear-cleanup
step for even-index hulls, and a canonicality invariant that area checks cannot
replace.

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
\begin{tikzpicture}[scale=0.62, font=\scriptsize]
  \draw[thick, fill=nordgreen!18] (0,0)--(4,0)--(4,4)--(3,4)--(3,1)--(1,1)--(1,4)--(0,4)--cycle;
  \foreach \p in {(0,0),(4,4),(3,1),(1,4)} \fill[nordblue] \p circle[radius=2.6pt];
  \foreach \p in {(4,0),(3,4),(1,1),(0,4)} \fill[nordpurple] \p circle[radius=1.8pt];
  \node[below left] at (0,0) {$S_0$};
  \node[above right] at (4,4) {$S_1$};
  \node[right] at (3,1) {$S_2$};
  \node[above] at (1,4) {$S_3$};
\end{tikzpicture}
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

**Lemma.** $E(S)$ is a closed rectilinear polygon if and only if every cyclic
consecutive pair of stored points differs in both coordinates.

*Proof sketch.* Each pair contributes a horizontal edge followed by a vertical
edge; sharing an axis collapses one edge to zero. $\square$

## Canonical Form

**Definition.** A stored sequence $S=(s_0,\ldots,s_{m-1})$ is **canonical** if

1. the $s_i$ are pairwise distinct, and
2. for every $i$ (indices modulo $m$),
$$x_i \ne x_{i+1}\quad\text{and}\quad y_i \ne y_{i+1}.$$

```python
def is_canonical(S):
    if len(S) < 2:
        return True
    if len(set(S)) != len(S):
        return False
    return all(
        a[0] != b[0] and a[1] != b[1]
        for a, b in zip(S, S[1:] + S[:1])
    )
```

- Duplicate detection is $O(m^2)$ naively, or $O(m\log m)$ by sorting.
- The consecutive-pair test is $O(m)$.

## Canonical Validation

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
  \node[nordred, below] at (2.5,-3.6) {not canonical};
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
  \node[nordgreen!45!black, below] at (2.5,-3.6) {canonical};
\end{tikzpicture}
\end{center}
```
:::
::::

- $S=((2,1),(2,0),(3,-3))$: the expansion contains two consecutive vertical
  segments and is **not** a canonical even-index list.
- Its canonical form is $((2,1),(3,-3))$.
- Area alone cannot detect this defect; the predicate is **structural**.

## Orientation and Signed Area

For a simple polygon with vertices $(x_i,y_i)$,

$$A=\frac12\sum_i\left(x_i y_{i+1}-x_{i+1}y_i\right).$$

- $A>0$: anticlockwise; $A<0$: clockwise.
- The even-index encoding admits an $O(m)$ evaluation over the stored points.
- The sign drives the hull and cut branches and serves as a cheap postcondition.

**Lemma.** The signed area is invariant under the x-first expansion $E$.

*Proof sketch.* Each inserted vertex is collinear with an axis-aligned edge and
contributes zero net area. $\square$

# Monotone Hulls

## Monotonicity and Convexity

:::: {.columns}
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.66, font=\scriptsize]
  \draw[thick, fill=nordblue!15] (0,0)--(4,0)--(4,4)--(3,4)--(3,2)--(1,2)--(1,4)--(0,4)--cycle;
  \draw[nordred, dashed] (2,-0.3)--(2,4.3);
  \node[below] at (2,-0.5) {$x$-monotone, not $y$-monotone};
\end{tikzpicture}
\end{center}
```
:::
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.66, font=\scriptsize]
  \draw[thick, fill=nordblue!15] (0,0)--(0,4)--(4,4)--(4,3)--(2,3)--(2,1)--(4,1)--(4,0)--cycle;
  \draw[nordred, dashed] (-0.3,2)--(4.3,2);
  \node[below] at (2,-0.5) {$y$-monotone, not $x$-monotone};
\end{tikzpicture}
\end{center}
```
:::
::::

**Definition.** A rectilinear polygon is $x$-monotone if every vertical line
meets it in a single interval; $y$-monotone is defined symmetrically.

**Lemma.** A rectilinear polygon is orthogonally convex if and only if it is
both $x$-monotone and $y$-monotone.

## Monotone Hull Algorithm

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

**Complexity.** $O(m)$ time and $O(m)$ space per hull.

## Collinear Cleanup

:::: {.columns}
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.78, font=\scriptsize]
  \draw[thick] (0,0)--(2,0)--(3,2);
  \draw[nordred, dashed] (2,0)--(3,0);
  \fill[nordblue] (0,0) circle[radius=2pt] node[below left] {$A$};
  \fill[nordred] (2,0) circle[radius=2pt] node[below] {$B$};
  \fill[nordblue] (3,2) circle[radius=2pt] node[right] {$C$};
  \node[nordred] at (2.4,0.35) {drop};
  \node[below] at (1.5,-0.5) {same $y$: drop the second};
\end{tikzpicture}
\end{center}
```
:::
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.78, font=\scriptsize]
  \draw[thick] (-2,1)--(0,0)--(0,2)--(2,3);
  \fill[nordblue] (-2,1) circle[radius=2pt] node[left] {$P$};
  \fill[nordred] (0,0) circle[radius=2pt] node[below] {$A$};
  \fill[nordblue] (0,2) circle[radius=2pt] node[right] {$B$};
  \fill[nordblue] (2,3) circle[radius=2pt] node[right] {$C$};
  \node[nordred] at (0.55,0.45) {drop};
  \node[below] at (0,-0.5) {same $x$: drop the first};
\end{tikzpicture}
\end{center}
```
:::
::::

- A monotone hull can still contain collinear even-index points.
- Remove the second point of a same-$y$ pair; remove the first of a same-$x$ pair.
- Repeat until no adjacent pair shares an axis.

**Lemma.** The cleanup preserves the represented boundary and the signed area.

*Proof sketch.* The removed point lies in the interior of a straight boundary
edge; deleting it merges two collinear edges into one. $\square$

## Hull Composition and Correctness

:::: {.columns}
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.62, font=\scriptsize]
  \draw[thick, fill=nordblue!15] (0,0)--(4,0)--(4,4)--(3,4)--(3,2)--(1,2)--(1,4)--(0,4)--cycle;
  \draw[nordred, line width=1.5pt] (3,2) circle[radius=3pt];
  \draw[nordred, line width=1.5pt] (1,2) circle[radius=3pt];
  \node[below] at (2,-0.4) {before};
\end{tikzpicture}
\end{center}
```
:::
::: {.column width="48%"}
```{=latex}
\begin{center}
\begin{tikzpicture}[scale=0.62, font=\scriptsize]
  \draw[thick, fill=nordgreen!18] (0,0)--(4,0)--(4,4)--(0,4)--cycle;
  \node[below] at (2,-0.4) {after};
\end{tikzpicture}
\end{center}
```
:::
::::

- $x$-hull then $y$-hull yields the rectilinear convex hull.
- Both hulls are idempotent on canonical inputs.
- The composition preserves the represented polygon and its area.
- With cleanup, the output satisfies `is_canonical`.

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
- The final pieces are rectangles, suitable for layout fracturing and DRC
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
- Find the nearest vertex by Manhattan distance (horizontal or vertical).
- Insert the cut point; split the circular list; recurse on both pieces.

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

**Recurrence.** $T(n)=T(k)+T(n-k+1)+O(n)$, hence $T(n)=O(n^2)$.

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

## Rectangle Cutting and Canonicality

- A rectangle piece has **2 stored points**: two opposite corners.
- The test `x_0 \ne x_1` and `y_0 \ne y_1` is exactly the canonical predicate
  for a 2-point list.
- Rectangle pieces are therefore canonical by construction.
- For larger pieces, canonicality must be checked explicitly; area and
  convexity do not imply it.

## Correctness Invariants and Complexity

**Invariants.**

1. **Area:** the sum of signed piece areas equals the signed area of the input.
2. **Convexity:** every piece is rectilinearly convex.
3. **Canonicality:** every piece is a valid even-index list; where the
   algorithm guarantees it, `is_canonical` holds.

**Complexity.**

| operation | cost |
|:----------|:-----|
| concave-vertex scan | $O(n)$ |
| nearest-vertex scan | $O(n)$ |
| insert / split | $O(1)$ |
| total decomposition | $O(n^2)$ |

For $n\le 100$, quadratic time is preferable to a complicated sub-quadratic
implementation.

# Verification

## Implementation and Tests

:::: {.columns}
::: {.column width="47%"}
**Python**

- canonical predicate tests
- hull-before-check assertions
- area + canonical checks on cut pieces
- full suite: **627 passed**

:::
::: {.column width="47%"}
**C++20 (xmake)**

- `xmake build test_recti`
- `xmake run test_recti`
- **139 test cases**
- **934 assertions**
- **0 failures**

:::
::::

- The hull is applied before the canonical check; raw creation is only an
  ordering, not a canonical representation.
- Three mixed even-index cut fixtures deliberately do not assert canonicality:
  their pieces can still contain implicit collinear points.

## Limitations and Threats to Validity

1. **Representation-specific predicate.** `is_canonical` enforces the x-first
   even-index convention; a geometrically valid rectangle can be written with a
   same-axis pair and must be rewritten.
2. **Synthetic inputs.** The evaluation uses generated point sets, not foundry
   data; the claims are algorithmic, not signoff.
3. **Quadratic scaling.** Decomposition is $O(n^2)$; $n>10^3$ is open.
4. **Cut completeness.** Some implicit collinear points require the cleanup
   phase; the cut algorithm alone does not guarantee canonical output.
5. **Robustness.** Integer arithmetic is exact; degenerate input handling is
   outside the present scope [@edelsbrunner1990sos].

# Conclusion

## Contributions and Open Problems

**Contributions.**

- A canonical even-index representation with an exact structural predicate.
- A template-method treatment of creation and monotone hulls.
- A collinear-cleanup lemma for even-index hulls.
- A recursive decomposition with explicit and implicit $270^\circ$ handling.
- Cross-language verification in Python and C++20.

**Open problems.**

- Sub-quadratic decomposition for large polygons.
- Canonical output for every cut variant, without a post-processing pass.
- Integration with detailed routing and DRC flows.
- Three-dimensional rectilinear decomposition.

## Q&A

- Code: `physdes-py` and `physdes-cpp` under the `luk036` organization.
- Thank you.

## References {.allowframebreaks}
