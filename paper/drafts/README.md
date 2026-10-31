# Paper formats

- `track2.pdf`: LaTeX research paper with an abstract, bold section headings,
  typeset equations and publication-style tables. Ten pages of main text and
  figures, followed by one page of references and the AI statement.
- `track2_full_paper.docx`: editable Word version of the full paper.
- `track2_d_e_sections.docx`: Sections 1, 5 and 6, references and AI statement.

The numbered Markdown files in `paper/` are the editable section sources.
`paper/track2.tex` is the editable LaTeX source for the PDF. From `paper/`,
compile it with [Tectonic](https://tectonic-typesetting.github.io/):

```bash
tectonic --outdir drafts track2.tex
```

The LaTeX source uses the existing images in `outputs/figures/`; keep that
folder alongside `paper/` when copying the project. The full paper condenses
Section 3 and the figure discussion to fit the page limit. Full statistics
remain in `outputs/summary_stats.csv`. Numerical results reproduce from raw
data with the commands in the repository README.
