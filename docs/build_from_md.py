"""
Build Remark.js HTML from slides markdown.
Run: python build_from_md.py
"""
import re

with open('D:/github/py/physdes-py/docs/slides_content.md', 'r', encoding='utf-8') as f:
    md = f.read()

# Split into slides
slides = [s.strip() for s in re.split(r'\n---\n', md) if s.strip()]

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

# Escape for HTML textarea
remark_content = remark_content.replace('</textarea>', '&lt;/textarea&gt;')

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

out = 'D:/github/luk036.github.io/idea/doc-fig-py-remark-v2.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Written {len(html)} bytes, {len(slides)} slides to {out}')
