====================================
Tail recursion elimination in python
====================================

Python does not support tail call recursion elimination by design.
Much has been discussed about that and Guido close the issue with a blog post:
http://neopythonic.blogspot.com.es/2009/04/tail-recursion-elimination.html

Here is my futil attempt to create a decorator that provides TRE via decorators
in pure python.