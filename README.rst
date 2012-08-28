====================================
Tail recursion elimination in python
====================================

Python does not support tail call recursion elimination by design.
Much has been discussed about that and Guido close the issue with a blog post:
http://neopythonic.blogspot.com.es/2009/04/tail-recursion-elimination.html

Here is my futil attempt to create a decorator that provides TRE via decorators
in pure python.

tre.tre_global
--------------

Naive aproximation that only works single thread with global functions.
The global namespace of the function is patched with an identity function to
break recursion.


tre.tre_trampoline
------------------

More elaborated decorator that is thread safe and works with any function
