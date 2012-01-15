mush - memorable url shortener
==============================
This is just a pet project to test out AppEngine. I find that many times
when using url shorteners it's nice to have a string I can remember in my
head. mush is intended to be minimalistic as I found that far too many url
shorteners have unncessary functionality and clutter. I just wanted
something that generates urls that are short, easy to write without
ambiguity and memorable. Basic analytic data is also provided to show how
many hits a link is getting.

Shortcode Generation
--------------------
One problem I often find is that after I generate a shortened URL, as soon
as I try to enter it on another device I've forgotten it. So I wanted my
shortcodes (the hash of the url) to be memorable. I realized that the
shortcodes are similar to passwords of which there are quite a few
algorithms for generating memorable password strings. Namely, Morrie
Gasser's [original generator](http://www.multicians.org/thvv/gpw.html). The
basic premise of the algorithm is to use statistics on the frequency of
three-letter sequences (trigraphs) in English to generate passwords. The
statistics are generated from a dictionary of words arranged in a lookup
matrix.

I started to code up my own implementation but fortunately came across a
Python module,
[pygpw](http://www.preetk.com/node/pygpw-generate-pronouncable-words/),
which is based on Gasser's algorithm. pygpw adds a few enhancements, like
adding leet speak generation, but also speeds up generation by using a
cache file. However, as Google App Engine does not allow programs to write
or create files, I modified the module to remove the caching functionality.

I call the module using the trigraph algorithm with a length of eight
characters, the default. This produces a string like 'blubbons'. As well as
being a good length for memorability it also provides around 200 billion
(26^8) unique variations -- more than enough for this purpose.

A sample running on AppEngine Can be found at http://memorsh.appspot.com
