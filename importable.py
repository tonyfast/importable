
# coding: utf-8

# 😵 simple __import__s for notebooks and markdown files.  All code elements are executed in order and imported into sys models.

# In[1]:


from __future__ import print_function
__all__ = 'finder',
meta_paths = []


# In[2]:


try:
    from importlib.util import spec_from_loader
    from importlib.machinery import SourceFileLoader as Base
except:
    from imputil import _FilesystemImporter as Base

from nbconvert.exporters.base import export, get_exporter
import sys, imp
from os.path import sep, curdir, extsep, exists
from nbconvert import get_exporter   
PY2 = sys.version_info.major is 2


# In[3]:


class Importable(Base, object):
    def find_spec(self, name, paths, target=None):
        loader =  self.find_module(name, paths, target)
        if loader:
            print(loader)
            loader = spec_from_loader(name, loader)
        return loader
    
    def find_module(self, name, paths, target=None):
        for ext in type(self.ext) is str and [self.ext] or self.ext:
            for path in paths or [curdir]:
                path = extsep.join([sep.join([path, name.split('.')[-1]]), ext])
                if exists(path):
                    return type(self)(name, path)
        return None
    
    def get_code(self, path):
        return compile(self.func(path), self.path, 'exec')


# In[4]:


class Patched(Importable):
    def __init__(self, name=None, path=None):
        self.name = name
        self.path = path 
    
    def load_module(self, name):
        return self.import_top(name)
                                
    def get_code(self, parent, name, fqname):
        return 0, super(Patched, self).get_code(self.path), dict(__file__=self.path, __importer__=self)


# In[5]:


exporter = get_exporter('python')()


# In[6]:


def add_finder(finder):
    return sys.meta_path.append(finder(None, None)) or meta_paths.append(sys.meta_path[-1]) or finder


# In[7]:


def finder(ext, bases=[], **kwargs):
    """A decorator to create a new ext loader by defining the get_code method.
    """
    def importer(func):
        return add_finder(type(
            func.__name__, 
            (PY2 and Patched or Importable,), 
            kwargs.update(func=func, ext=ext) or kwargs
        ))
    return importer


# In[8]:


def load_ipython_extension(ip=None):
    finder('ipynb')(Ipynb)
    sys.path_importer_cache.clear()


# In[9]:


def Ipynb(self, path):
    script = exporter.from_filename(self.path)[0]
    if PY2:
        script = '\n'.join(script.splitlines()[2:])
    return script


# As proof-of-concept, create a finder for ipynb files.

# In[10]:


def unload_ipython_extension(ip=None):
    for _ in sys.meta_path:
        if _ in meta_paths: sys.meta_path.pop(sys.meta_path.index(_))
    sys.path_importer_cache.clear()


# In[11]:


if True and __name__ == '__main__': 
    get_ipython().system('jupyter nbconvert --to script importable.ipynb')

