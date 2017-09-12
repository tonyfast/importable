
# coding: utf-8

# # importable 
# 
# `pip install git+`<a href="https://github.com/tonyfast/importable"><code>https://github.com/tonyfast/importable</code></a>
# 
# > __importable__ is an IPython magic that permits python imports from notebook sources [See the source.](https://github.com/tonyfast/importable/blob/master/importable.ipynb)

# In[13]:


from __future__ import print_function
__all__ = 'finder',
meta_paths = []


# In[14]:


try:
    # Python 3 imports
    from importlib.util import spec_from_loader
    from importlib.machinery import SourceFileLoader as Base
except:
    # Python 2 imports
    from imputil import _FilesystemImporter as Base

from nbconvert.exporters.base import export, get_exporter
import sys, imp
from os.path import sep, curdir, extsep, exists
from nbconvert import get_exporter   
PY2 = sys.version_info.major is 2


# In[16]:


class Importable(Base, object):
    """Base class for Python 2 or Python 3 imports.  Python 2 imports are not reloadable."""
    def find_spec(self, name, paths, target=None):
        # () -> ModuleSpec
        """Python 3 finder uses the result from the Python 2 finder."""
        loader =  self.find_module(name, paths, target)
        return loader and spec_from_loader(name, loader)

    def find_module(self, name, paths, target=None):
        # () -> Importable
        """Python 2 finder"""
        for ext in type(self.ext) is str and [self.ext] or self.ext:
            for path in paths or [curdir]:
                path = extsep.join([sep.join([path, name.split('.')[-1]]), ext])
                if exists(path):
                    return type(self)(name, path)
        return None

    def get_code(self, path):
        """Python 3 get_code from that returns a code object."""
        return compile(self.func(path), self.path, 'exec')


# In[4]:


class Patched(Importable):
    """A patch for python 2"""
    def __init__(self, name=None, path=None):
        self.name, self.path = name, path 

    def load_module(self, name):
        """Python 2 loader."""
        return self.import_top(name)

    def get_code(self, parent, name, fqname):
        """Python 2 get_code function shim."""
        return 0, super(Patched, self).get_code(self.path), dict(__file__=self.path, __importer__=self)


# In[6]:


def add_finder(finder):
    """Add a MetaFinder to the import manager."""
    sys.meta_path.append(finder(None, None)) or meta_paths.append(sys.meta_path[-1])
    return finder


# > `finder` all custom extensions.

# In[7]:


def finder(ext, bases=[], **kwargs):
    """A decorator to create a new ext loader by defining a custom func method."""            
    def importer(func):
        return add_finder(type(
            func.__name__, (PY2 and Patched or Importable,), kwargs.update(func=func, ext=ext) or kwargs))
    return importer


# > `load_ipython_extension` and `unload_ipython_extension` are `ipython` namespaces; they define the `%load_ext` and `%unload_ext`, respectively. 

# In[17]:


def load_ipython_extension(ip=None):
    """An Ipython extension to import notebooks.

    %load_ext importable
    """
    finder('ipynb')(Ipynb)
    sys.path_importer_cache.clear()
    
load = load_ipython_extension

def unload_ipython_extension(ip=None):
    """An Ipython extension to import notebooks.

    %load_ext importable
    """
    for _ in sys.meta_path:
        if isinstance(_, Importable): 
            sys.meta_path.pop(sys.meta_path.index(_))
    sys.path_importer_cache.clear()

unload = unload_ipython_extension


# ## Notebook importer

# > an `nbconvert` exporter to create python code from notebooks.

# In[5]:


exporter = get_exporter('python')()


# In[10]:


def Ipynb(self, path):
    """Custom loader from Ipynb files using the nbconvert exporter.

    This pattern can be reused to create other finders."""
    script = exporter.from_filename(self.path)[0]
    if PY2:
        script = '\n'.join(script.splitlines()[2:])
    return script


# ## Create source

# In[ ]:


if True and __name__ == '__main__': 
    get_ipython().system('jupyter nbconvert --to script importable.ipynb')


# In[ ]:




