Templates for Plom Tests
========================

These are example templates you can use for preparing a test or exam
for using with Plom.


LaTeX templates
---------------

We provide `latexTemplate.tex`, an example with good margins that work
well with our QR code placement.


Using a word processor
----------------------

Of course, you do not need to use LaTeX to prepare your test.  The
included `idBox.pdf` should be used as a template for students to
enter their name and student number.  This standard template will help
with the automated optical character recongnition of student numbers.


Extra sheets
------------

Generally we recommend leaving lots of space on the page.  But if a
student runs out of space and needs extra paper, you can have them
write on any paper, just make sure its labelled with their student
number and their Plom test number.  We provide an appropriate
template for this called `extraSheets.tex`.

If you want to enforce blind-grading, see `extraSheets_noname.tex`.

Make sure you print these double-sided!


Source code for misc support files
----------------------------------

There are several ways to build `idBox` and `idBox2` from sources. First, with fewer steps, run
  * `pdflatex idBox2-source.tex`
  * `pdfcrop --margins -1 idBox2-source.pdf idBox2.pdf`
  * `pdf2svg idBox2.pdf idBox2.svg`

Or, if you have inkscape installed you can get pdf and svg easily:
  * `pdflatex idBox2-source.tex`
  * `inkscape --pdf-poppler --export-area-drawing idBox2-source.pdf -o idBox2.pdf`
  * `inkscape --pdf-poppler --export-area-drawing --export-plain-svg idBox2-source.pdf -o idBox2.svg`

Alternatively, with more steps and intermediaries, run
  * `latex idBox2-source.tex`
  * `dvips idBox2-source.dvi`
  * `ps2epsi idBox2-source.ps`    (note that this produces a large and not especially good eps file)
  * `epspdf idBox2-source.epsi idBox2.pdf`
  * `pdf2svg idBox2.pdf idBox2.svg`

Note that without the extra `margins` argument pdfcrop leaves a 1pt white margin around the idbox. Also note that the intermediate .epsi file is quite large but the final cropped pdf is reasonably sized.
