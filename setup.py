# coding: utf-8

# In[85]:

from os.path import join, dirname
import setuptools


def read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()


from distutils.core import setup, Command
# you can also import from setuptools

setuptools.setup(
    name="importable",
    version="0.0.1",
    author="Tony Fast",
    author_email="tony.fast@gmail.com",
    description="Import anything in python.",
    license="BSD-3-Clause",
    keywords="IPython Jupyter Imports",
    url="http://github.com/tonyfast/importable",
    py_modules=['importable'],
    #     long_description=read("readme.rst"),
    classifiers=[
        "Topic :: Utilities",
        "Framework :: IPython",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=[
        'nbconvert', 'entrypoints'
    ], tests_require=[])
