====================================
Tail recursion elimination in python
====================================

Python does not support tail call recursion elimination by design.
Much has been discussed about that and Guido closed the disccussion with a
blog post:
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

More elaborated decorator that is thread safe, handles mutual recursion and
works with any function.

Uses the `trampoline <http://en.wikipedia.org/wiki/Trampoline_%28computers%29>`_
technique to avoid recursion.
Uses global thredlocal variables allow the same function to start the
trampoline iteration, execute the orinal function and return a trampoline call
instead of a recursion call.
