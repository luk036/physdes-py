# Build phys_des.pdf from phys_des.md. Run from paper/.
#
# Flag rationale (md-to-latex skill), so the knowledge is not tribal:
#  - Title/author/abstract live in the .md YAML front matter, so the body
#    headings start at `##`; `--shift-heading-level-by=-1` maps them to
#    \section (otherwise pandoc emits no \section and numbering degrades).
#  - `-F pandoc-crossref` resolves the {#sec:..}/{#eq:..} labels.
#  - `--citeproc` builds the reference list from phys_des.bib using the vendored,
#    self-contained ieee.csl (no independent-parent): offline and reproducible.
#  - Build options live in paper/latex.yaml (IEEEtran journal class, algorithm
#    packages, hyperlinks) and paper/crossref.yaml (reference prefixes).
#  - Two-column IEEEtran: pandoc emits `longtable` for pipe tables, illegal in
#    two-column mode, so the tables are authored as raw LaTeX `table*` floats.
#  - pdflatex cannot embed SVG; the *.svg sources live in figures/ and their
#    *.pdf twins are committed, so a normal build never needs the converter.
#    Run `make figures` only after editing an SVG; do not use ImageMagick (it
#    rasterizes)---cairosvg keeps the figure vector.

PANDOC := pandoc
FLAGS  := -F pandoc-crossref --citeproc -s -t latex -N --reference-links \
          --shift-heading-level-by=-1 --pdf-engine=pdflatex \
          --metadata-file=latex.yaml --metadata-file=crossref.yaml

FIG_SVG := $(wildcard figures/*.svg)
FIG_PDF := $(FIG_SVG:.svg=.pdf)

.PHONY: paper talk figures clean

paper: phys_des.pdf

phys_des.pdf: phys_des.md phys_des.bib ieee.csl latex.yaml crossref.yaml $(FIG_PDF)
	$(PANDOC) $(FLAGS) phys_des.md -o $@

figures: $(FIG_PDF)

figures/%.pdf: figures/%.svg
	python -c "import cairosvg,sys; cairosvg.svg2pdf(url=sys.argv[1], write_to=sys.argv[2])" "$<" "$@"

# --- Beamer talk -----------------------------------------------------------
# The deck needs LuaLaTeX (emoji font fallback) and two passes (outline and
# navigation), so emit phys_des-talk.tex with pandoc, then run lualatex twice.
# --include-in-header must be a CLI flag: pandoc mangles raw LaTeX in YAML.
talk: phys_des-talk.pdf

phys_des-talk.tex: phys_des-talk.md beamer.yaml preamble.tex phys_des.bib ieee.csl
	pandoc --citeproc -s -t beamer --slide-level=2 \
	  --metadata-file=beamer.yaml --include-in-header=preamble.tex \
	  phys_des-talk.md -o $@

phys_des-talk.pdf: phys_des-talk.tex $(FIG_PDF)
	lualatex -interaction=nonstopmode -halt-on-error phys_des-talk.tex
	lualatex -interaction=nonstopmode -halt-on-error phys_des-talk.tex

clean:
	-@rm -f phys_des.tex phys_des.aux phys_des.log phys_des.out phys_des.toc \
	       phys_des-talk.tex phys_des-talk.aux phys_des-talk.log \
	       phys_des-talk.out phys_des-talk.toc phys_des-talk.nav \
	       phys_des-talk.snm phys_des-talk.vrb ; true
