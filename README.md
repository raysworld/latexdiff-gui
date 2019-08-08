# latexdiff-gui

#### Introduction

A Qt-based GUI for [latexdiff](https://www.ctan.org/pkg/latexdiff).

The following introduction for latexdiff is copied from its website:

> La­texd­iff is a Perl script for vi­sual mark up and re­vi­sion of sig­nif­i­cant dif­fer­ences be­tween two LATEX files. Var­i­ous op­tions are avail­able for vi­sual markup us­ing stan­dard LATEX pack­ages such as [color](https://www.ctan.org/pkg/color). Changes not di­rectly af­fect­ing vis­i­ble text, for ex­am­ple in for­mat­ting com­mands, are still marked in the LATEX source. A rudi­men­tary re­vi­sion fa­cilil­ity is pro­vided by an­other Perl script, la­texre­vise, which ac­cepts or re­jects all changes. Man­ual edit­ing of the dif­fer­ence file can be used to over­ride this de­fault be­haviour and ac­cept or re­ject se­lected changes only.

#### Prerequisite

Before using, you need to install Python. After that, please use the following command to install dependencies:

```shell
pip install -r requirements.txt
```

#### How to use

1. Type the following command to open the window:

```shell
python ./latexdiff-gui.py
```

2. Follow the steps on the screenshot to get the output file:

![](https://raw.githubusercontent.com/raysworld/latexdiff-gui/master/figs/how-to-use.png)

#### Markup Styles

1. Underline (default)

   ![](https://raw.githubusercontent.com/raysworld/latexdiff-gui/master/figs/stl_underline.png)

2. CTranditional

   ![](https://raw.githubusercontent.com/raysworld/latexdiff-gui/master/figs/stl_ctraditional.png)

3. Traditional

   ![](https://raw.githubusercontent.com/raysworld/latexdiff-gui/master/figs/stl_traditional.png)

4. CFont

   ![](https://raw.githubusercontent.com/raysworld/latexdiff-gui/master/figs/stl_cfont.png)

5. Fontstrike

   ![](https://raw.githubusercontent.com/raysworld/latexdiff-gui/master/figs/stl_fontstrike.png)