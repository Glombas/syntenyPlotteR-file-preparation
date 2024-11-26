# syntenyPlotteR-file-preparation
Here is a python script that takes a [mummer](https://mummer.sourceforge.net/) (nucmer) alignment output and transforms it into a form suitable for the package [syntenyPlotteR](https://github.com/Farre-lab/syntenyPlotteR) in R, and offers other plotting possibilities.

Nucmer output example:

>CM060803.1 A01 51597069 55404493

>1940 7793 107905 113811 163 163 0

>13

>-58

>-3

>...

>7787 8590 119088 119886 25 25 0

>190

>-124

>-1

>...

>8962 15034 125428 131495 265 265 0

>-129

>-1

>-1


Transformed output example in csv format:

>CM060803.1,1940,7793,A01,107905,113811,+

>CM060803.1,7787,8590,A01,119088,119886,+

>CM060803.1,8962,15034,A01,125428,131495,+


### Requirements: glob, numpy, pandas

_Note: I suggest using a python IDE such as [Spyder](https://www.spyder-ide.org/) which has these preinstalled/preloaded if you can't load them._
