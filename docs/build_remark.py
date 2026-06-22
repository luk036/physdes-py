"""
Build the Remark.js slideshow for doc-fig-py.
Run: python build_remark.py
"""
import re

MD = r"""layout: true
class: typo, typo-selection

---

count: false
class: nord-dark, middle, center

# 🖼️ Embedding Figures in Docs

### Python 🐍 vs Rust 🦀

@luk036 👨‍💻 · 2026 📅

---

### 📋 Feature Comparison

.pull-left[

**Python (Sphinx)** 🐍

| Feature | Status |
|---------|--------|
| 🖼️ Static images | ✅ Native `.. figure::` |
| 📈 Auto-generated plots | ✅ `.. plot::` directive |
| 🎨 ASCII → SVG diagrams | ✅ `.. svgbob::` |
| 📐 Equations | ✅ `.. math::` / `:math:` |
| 📦 Asset pipeline | ✅ Built-in auto-copy |
| 🌐 Hosted (RTD) | ✅ Works out of box |
]

.pull-right[

**Rust (rustdoc)** 🦀

| Feature | Status |
|---------|--------|
| 🖼️ Static images | ❌ No asset bundling |
| 📈 Auto-generated plots | ❌ Not available |
| 🎨 ASCII → SVG diagrams | ❌ Not available |
| 📐 Equations | ✅ `$...$` / `$$...$$` |
| 📦 Asset pipeline | ❌ `embed-doc-image` (workaround) |
| 🌐 Hosted (docs.rs) | ⚠️ Needs `doc-images` feature |
]

---

### 🤔 The Problem

Mathematical & geometric libraries cry out for **visual documentation**:

```python
def halton(n, base1, base2):
    """Generate 2D Halton sequence points."""
    ...
```

```rust
/// Halton sequence generator (bases 2, 3).
pub struct Halton { ... }
```

❌ **Without figures**: Users must imagine the distribution
✅ **With figures**: A scatter plot tells the story instantly

**Core issue**: Neither Sphinx nor rustdoc natively **bundles local image files** into the published documentation output.

**Python has mature solutions** across the board. **Rust** is catching up — but still has gaps.

---

### 🖼️ The Asset Pipeline Gap

**Local build** — seems to work:

```text
# Sphinx                          # rustdoc
docs/_build/html/                 target/doc/my_crate/
├── index.html                    ├── index.html
├── _images/                      ├── images/halton.png
│   └── halton.png                └── ...
└── ...
```

**Published** — images go missing 😱

- **docs.rs** publishes only what `cargo doc` produces — **no asset bundling**
- **ReadTheDocs** copies `_images/` for Sphinx-managed figures — **works correctly**
- Neither tool knows: *"this image is a documentation asset"*

**Python solves this natively** (Sphinx asset pipeline). **Rust** needs a crate.

---

### 💥 Real-World Impact

.pull-left[

**Rust projects affected:**

| Domain | Examples |
|--------|----------|
| 🖌️ GUI | egui, Masonry, Slint |
| 📊 Math | nalgebra, lds-rs |
| 📈 Plotting | plotters, plotly |
| 🎮 Game | Bevy, macroquad |
| 🧪 Science | rust-cv, ndarray-stats |

**Quote from Masonry devs (2024):**
> *"We considered a LOT of alternatives... all of them were pretty fragile. We ultimately decided not to include all images."*

]

.pull-right[

**Python projects — no problem:**

| Domain | Examples |
|--------|----------|
| 📊 Math | numpy, scipy, lds-gen |
| 🧮 Optim. | cvxpy, ellalgo |
| 🧬 Science | biopython, astropy |
| 🏭 EDA | netlistx, physdes-py |

**Sphinx ecosystem** handles images, figures, equations, and diagrams — all natively, all work on ReadTheDocs.

]

---

## 🐍 Python vs 🦀 Rust — Feature by Feature

---

### 🖼️ Static Images

.pull-left[

**Python (Sphinx)** 🐍

```rst
.. figure:: images/halton.png
   :width: 400px
   :alt: Halton 2D scatter

   500 Halton points.
```

✅ Native directive `.. figure::`
✅ Auto-copies to `_images/` in output
✅ Rewrites HTML paths
✅ RTD = works
✅ Zero extra dependencies

**How**: Sphinx detects the directive, copies the file, rewrites the path. All built-in.

]

.pull-right[

**Rust (rustdoc)** 🦀

```rust
//! ![Scatter][plot]
//! 500 Halton points.

#![cfg_attr(feature = "doc-images",
    doc = embed_doc_image::embed_image!(
        "plot", "docs/images/plot.png"
    )
)]
```

❌ No native image bundling
❌ Requires external crate
❌ Requires proc macro
❌ Base64 bloat in HTML
⚠️ docs.rs works with feature flag

**How**: `embed-doc-image` base64-encodes the PNG into a `data:` URI at compile time.

]

---

### 📈 Auto-Generated Plots

.pull-left[

**Python (Sphinx)** 🐍

```rst
.. plot::

   import matplotlib.pyplot as plt
   from lds_gen.lds import Halton

   pts = Halton(base=[2,3]).pop_batch(500)
   plt.scatter(*zip(*pts))
```

✅ Code runs at doc-build time
✅ PNG captured and embedded
✅ Never stale — code IS the figure
✅ External script or inline code
✅ `matplotlib.sphinxext.plot_directive`

**Pipeline**: Source → `sphinx-build` → execute Python → capture PNG → embed in HTML.

]

.pull-right[

**Rust (rustdoc)** 🦀

```rust
// No equivalent.
// Must pre-generate PNGs
// separately (e.g. Python script)
// and embed them as static images.
```

❌ No `.. plot::` equivalent
❌ No `eval`-at-doc-build-time
❌ Must maintain separate script
❌ Must commit PNGs to repo
❌ Or embed via `embed-doc-image`

**Rust has no macro or tool** to run code and capture output during `cargo doc`. Every plot must be pre-rendered externally.

]

---

### 🎨 ASCII → SVG Diagrams

.pull-left[

**Python (Sphinx)** 🐍

```rst
.. svgbob::
   :align: center

      _.-'''''''-._
    ,'    |        `.
   /      |          \
   |       | .        |
   |       |          |
    \      |         /
     `._   |      _.'
        '-......-'
```

✅ ASCII art → inline SVG
✅ No image files to manage
✅ `sphinxcontrib.svgbob`
✅ Renders in RTD

]

.pull-right[

**Rust (rustdoc)** 🦀

```rust
// No equivalent.
// Must render ASCII diagram
// to PNG externally, then
// embed via embed-doc-image
```

❌ No svgbob equivalent
❌ No ASCII-to-SVG in rustdoc
❌ Would need external tool + `embed-doc-image` workaround

]

---

### 📐 Equations

.pull-left[

**Python (Sphinx)** 🐍

```rst
.. math::

   \phi_b(n) =
   \sum_{k=0}^{m} \frac{d_k}{b^{k+1}}
```

```rst
Inline :math:`\phi_2(n)` works too.
```

✅ `.. math::` display equations
✅ `:math:` inline equations
✅ MathJax or imgmath backends
✅ ReadTheDocs compatible
✅ Multiple syntaxes (LaTeX, AsciiMath)

]

.pull-right[

**Rust (rustdoc)** 🦀

```rust
//! Display:
//! $$ \phi_b(n) = \sum_{k=0}^{m} \frac{d_k}{b^{k+1}} $$
//!
//! Inline: $ \phi_2(n) $
```

✅ `$$...$$` display equations
✅ `$...$` inline equations
✅ KaTeX rendered
✅ docs.rs compatible
✅ Markdown-native syntax

**Rust matches Python here** — rustdoc has had KaTeX math support since 2023.

]

---

### 📦 Asset Pipeline

.pull-left[

**Python (Sphinx)** 🐍

```text
Source                      Build                   Output
──────                      ─────                   ──────
docs/
├── conf.py    ─────┐
├── index.rst       │
├── images/         │── sphinx-build ──► docs/_build/html/
│   └── plot.png ───┘                     ├── index.html
├── examples/                              └── _images/
│   └── plot_halton.py                         └── plot.png
```

**Sphinx automatically:**
- Copies `images/` to `_images/` in output
- Detects assets referenced in directives
- Rewrites HTML paths
- Works on RTD without extra config

]

.pull-right[

**Rust (rustdoc)** 🦀

```text
Source                    Build                   Output
──────                    ─────                   ──────
my-crate/
├── Cargo.toml  ─────┐
├── src/             │
│   └── lib.rs ──────┤── cargo doc ──► target/doc/my_crate/
└── docs/            │                   ├── index.html
    └── images/      │                   └── (no assets copied)
        └── plot.png ┘
```

**`cargo doc` does NOT:**
- Copy any files outside `src/`
- Know about documentation assets
- Bundle images for docs.rs

**Workaround**: `embed-doc-image` base64-encodes at compile time.

]

---

### ⚡ Architecture

.mermaid[
<pre>
graph TD
    subgraph "Python (Sphinx)"
        A1["conf.py\nextensions"] --> B1["sphinx-build"]
        C1["images/"] -->|"auto-copy"| B1
        D1["*.rst: .. figure::"] --> B1
        E1["*.rst: .. plot::"] -->|"matplotlib execute"| B1
        F1["*.rst: .. svgbob::"] -->|"ASCII→SVG"| B1
        B1 --> G1["HTML + _images/\non ReadTheDocs"]
    end

    subgraph "Rust (rustdoc)"
        A2["Cargo.toml\nfeatures"] --> B2["cargo doc"]
        C2["lib.rs\nembed_image!"] -->|"base64 encode"| B2
        D2["pre-rendered\nPNG files"] --> C2
        B2 --> E2["HTML with\ndata: URIs\non docs.rs"]
    end

    style A1 fill:#e8f5e9,stroke:#2e7d32
    style D1 fill:#e3f2fd,stroke:#1565c0
    style E1 fill:#c8e6c9,stroke:#2e7d32
    style F1 fill:#fff9c4,stroke:#f9a825
    style G1 fill:#fff3e0,stroke:#e65100
    style A2 fill:#e8f5e9,stroke:#2e7d32
    style C2 fill:#e3f2fd,stroke:#1565c0
    style E2 fill:#fff3e0,stroke:#e65100
</pre>
]

**Python**: Multiple native tools — files copied, code executed, ASCII converted. All built into Sphinx.
**Rust**: Single workaround — pre-rendered PNGs base64-encoded via proc macro.

---

### ⚠️ Pitfalls Side-by-Side

.pull-left[

**Python (Sphinx)**

1. **`html_static_path` config**
   - Must include image directories

2. **Path resolution**
   - Relative: `images/plot.png`
   - Absolute: `/images/plot.png`

3. **`.. plot::` dependencies**
   - Needs matplotlib at build time
   - Code must be importable

4. **RST verbosity**
   - Directives are more verbose than Markdown

]

.pull-right[

**Rust (rustdoc)**

1. **Missing images → compile error**
   ```
   error: proc macro panicked
   message: Failed to load image
   ```

2. **Base64 bloat**
   - 100 KB PNG → ~133 KB in HTML
   - Optimize with `oxipng` / `pngquant`

3. **Feature-gating complexity**
   - `cfg_attr(feature = "doc-images", ...)`
   - Inner attributes need nightly

4. **No auto-generation**
   - Every plot must be pre-rendered externally
   - Rust code cannot generate figures at doc-build time

]

---

### 📊 Results: Four Python Projects

| Project | Plots | Svgbob | Domain |
|---------|-------|--------|--------|
| `lds-gen` | 4 | ✅ 3 diagrams | Low-discrepancy sequences |
| `netlistx` | 2 | — | Netlist algorithms |
| `physdes-py` | 5 | ✅ (docstrings) | Physical design |
| `ellalgo` | 2 | ✅ (docstrings) | Ellipsoid method |
| **Total** | **13** | **All zero warnings** ✅ | |

**Setup cost per project:**
- Static images: 0 lines (Sphinx built-in)
- `.. plot::`: +5 lines in `conf.py`
- `.. svgbob::`: +1 line in `conf.py`

**Maintenance**: Change source → rebuild → docs update. That's it.

---

### 💡 Key Takeaways

.pull-left[

**Python (Sphinx)** — Mature ecosystem ✅

| Need | Solution | Lines |
|------|----------|-------|
| Static image | `.. figure::` | 0 (built-in) |
| Auto plot | `.. plot::` | +1 extension |
| ASCII diagram | `.. svgbob::` | +1 extension |
| Equation | `.. math::` | 0 (built-in) |
| Asset pipeline | Auto-copy to `_images/` | 0 |

**All work on ReadTheDocs. All zero extra runtime deps.**

]

.pull-right[

**Rust (rustdoc)** — Catching up 🛠️

| Need | Solution | Lines |
|------|----------|-------|
| Static image | `embed-doc-image` | 6 (Cargo.toml) + 20 (lib.rs) |
| Auto plot | ❌ Not available | Pre-render externally |
| ASCII diagram | ❌ Not available | Pre-render + embed |
| Equation | `$$...$$` | 0 (built-in) |
| Asset pipeline | `embed-doc-image` base64 | Same as above |

**Rust needs RFC #3397** for native asset bundling. Until then, `embed-doc-image` is the workaround.

]

---

### 📈 Future: Rust RFC #3397

**Proposal**: Native asset bundling in rustdoc

```rust
//! This would be the dream:
//!
//! ![Scatter](docs/images/plot.png)
//!
//! cargo doc automatically copies
//! docs/ to output
```

**Status**: On hold — blocked on `cargo` source format evolution

**Tracking**: [github.com/rust-lang/rfcs/issues/3397](https://github.com/rust-lang/rfcs/issues/3397)

**Python has had this for 20+ years.** Rust will get there too.

---

class: nord-light, middle, center

## ❓ Questions?

---

count: false
class: nord-dark, middle, center

# 🙏 Thank You

### Document with Pictures! 🖼️

**Slides**: [`luk036.github.io/idea/doc-fig-py-remark`](https://luk036.github.io/idea/doc-fig-py-remark.html)

**Reference slides**:
- [`doc-eqn-py-remark`](https://luk036.github.io/idea/doc-eqn-py-remark.html) — Equations in Python
- [`doc-eqn-remark`](https://luk036.github.io/idea/doc-eqn-remark.html) — Equations in Rust

**Key crates**:
- [`embed-doc-image`](https://crates.io/crates/embed-doc-image)
- [`lds-gen`](https://crates.io/crates/lds-gen)

**Repositories**:
- [`github.com/luk036/lds-rs`](https://github.com/luk036/lds-rs)
- [`github.com/luk036/lds-gen`](https://github.com/luk036/lds-gen) (Python)
- [`github.com/luk036/netlistx`](https://github.com/luk036/netlistx)
- [`github.com/luk036/physdes-py`](https://github.com/luk036/physdes-py)
- [`github.com/luk036/ellalgo`](https://github.com/luk036/ellalgo)

@luk036 👨‍💻 · 2026 📅
"""

# Split into slides
slides = [s.strip() for s in re.split(r'\n---\n', MD) if s.strip()]

# Annotate slides
annotated = []
for i, slide in enumerate(slides):
    first_line = slide.split('\n')[0]
    is_qa = '❓ Questions' in first_line
    is_end = '🙏 Thank You' in first_line
    if i == 0 or is_qa or is_end:
        annotated.append(f'count: false\nclass: nord-dark, middle, center\n\n{slide}')
    elif first_line.startswith('## 🐍'):
        annotated.append(f'class: nord-light, middle, center\n\n{slide}')
    else:
        annotated.append(slide)

remark_content = 'layout: true\nclass: typo, typo-selection\n\n---\n' + '\n\n---\n\n'.join(annotated)

html = f'''<!doctype html>
<html>
  <head>
    <title>Embedding Figures in Docs — Python &amp; Rust</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="user-scalable=no,initial-scale=1,maximum-scale=1,minimum-scale=1,width=device-width" />
    <link rel="stylesheet" type="text/css" href="../katex/katex.min.css" />
    <link rel="stylesheet" type="text/css" href="../css/spaces.css" />
    <link rel="stylesheet" type="text/css" href="../css/slides.css" />
    <link rel="stylesheet" type="text/css" href="../css/nord-dark.css" />
    <link rel="stylesheet" type="text/css" href="../css/nord-light.css" />
    <link rel="stylesheet" type="text/css" href="../css/font-nord.css" />
    <link rel="stylesheet" type="text/css" href="../css/bg-nord.css" />
    <link rel="stylesheet" type="text/css" href="../css/style.css" />
  </head>
  <body>
    <textarea id="source">
{remark_content}
    </textarea>
    <script src="../js/remark.min.js"></script>
    <script src="../katex/katex.min.js" type="text/javascript"></script>
    <script src="../katex/contrib/auto-render.min.js" type="text/javascript"></script>
    <script src="../js/mermaid.min.js"></script>
    <script type="text/javascript">
      var renderMath = function () {{
        renderMathInElement(document.body, {{
          delimiters: [
            {{ left: '$$', right: '$$', display: true }},
            {{ left: '$', right: '$', display: false }},
          ],
          ignoredTags: ['pre', 'code'],
        }});
      }};
      var slideshow = remark.create({{
        ratio: '16:10',
        highlightStyle: 'tomorrow-night-blue',
        highlightLines: true,
        countIncrementalSlides: false,
        navigation: {{
          scroll: false,
          touch: true,
          click: false,
        }},
      }}, renderMath);
    </script>
    <script src="../js/mermaid-init.js"></script>
  </body>
</html>'''

with open('D:/github/luk036.github.io/idea/doc-fig-py-remark.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Written {len(html)} bytes, {len(slides)} slides')
