News
====

1.1 Brooks
----------

 * HTTP/HTTPS endpoints have been added, to be used with a reverse
   proxy.
 * The input field has various new parameters including autofocus and
   a URL datatype.
 * The htdocs `doclick()` function now includes a regular expression to
   strip leading `http(s)://`.
 * Sysvinit now correctly loads defaults before checking if package is
   installed.
 * Relative URLs are now handled properly.
 * py-streamhtmlparser has been split off into its own project at
   <https://github.com/swiperproxy/py-streamhtmlparser>. Both the
   streamhtmlparser library and the py-streamhtmlparser wrapper are
   still included but will be properly split from distribution in the 2.0
   release. 
 * A generic favicon has been added.
 * htdocs now use an external css file to simplify custom styling, and
   supports minified css.
 * htdocs now include a variety of meta information.
 * Libraries loaded in the landing page no longer return 403 errors.
 * A variety of inherited code has been refactored.
 * The PyDev project file is now distributed with the source code.
 * The Bootstrap library has been updated to version 3.3.5.
 * The jQuery library has been updated to version 2.2.4.

1.0.1 Aria
----------

 * The license URL now points to the correct location.

1.0 Aria
--------

 * Initial release.
