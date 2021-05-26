# pepu-beamer
Generate an exciting slideshow for friday bottle raffling purposes

## Configuration
You can control the program behaviour a bit by setting configuration constants
directly in `main.py`. See the file for comments.

It is also possible to use a custom `.tex` template.

## Usage
Write raffling participants to `osallistujat.txt`, or whatever you configure the filename to.
Write one name per line. The names should be unique.

Then, simply run
```
./main.py
```

The program outputs a tex-file (default `rigged.tex`).
If the configuration flag `COMPILE_AND_PREVIEW` is set,
the program will also compile and show `rigged.pdf` using `latexmk`.
