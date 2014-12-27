from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("streamhtmlparser", ["py-streamhtmlparser.pyx"], include_dirs=[".."], libraries=['streamhtmlparser'], library_dirs=['../../.libs'])]

setup(
    name = 'Python streamhtmlparser',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)

