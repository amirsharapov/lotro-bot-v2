from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(r"C:\Users\Amir Sharapov\Code\bots\lotro-bot-v2\bots\testing_bot\test_cy.pyx"))
