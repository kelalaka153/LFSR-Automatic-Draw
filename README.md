# LFSR-Automatic-Draw
A python code that output Latex format that can be converted to png image for the desired LFSR.


The code is self explanatory, at least in my view. Go to `The taps` and defind your LFSR with the initial values. Compile with `python3.8 lfsr_draw.py  > lfsr.tex` and next run `pdflatex -shell-escape lfsr.tex` and your lfsr.png is there.

Sample images;

![image](https://i.stack.imgur.com/P8Cs6.png)

![image](https://i.stack.imgur.com/wwAR8.png)

The First LFSR of A5/1 outputted for [another Q](https://crypto.stackexchange.com/a/89981/18298). 

![image](https://i.stack.imgur.com/Wgo8w.png)

Duing working on A5/1's LFSR many bugs were cleaned! Font size is still an issue.


This is used in [Cryptography.SE](https://crypto.stackexchange.com/q/89828/18298) as a meta test.

and you can produce animations, too ( very soon the code is coming)

![image](https://i.stack.imgur.com/GV4IU.gif)

use 

`convert -delay 50 -loop 0 lfsr*.png lfsr.gif`

to produce the gif from the output images.

