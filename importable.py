
# coding: utf-8

# # importable 
# 
# `pip install git+`<a href="https://github.com/tonyfast/importable"><code>https://github.com/tonyfast/importable</code></a>
# 
# > __importable__ is an IPython magic that permits python imports from notebook sources [See the source.](https://github.com/tonyfast/importable/blob/master/importable.ipynb)

# In[1]:


from __future__ import print_function
__all__ = 'finder',
meta_paths = []


# In[2]:


from types import ModuleType

from importlib import *
from importlib.util import spec_from_loader
from importlib.machinery import SourceFileLoader as Base, ModuleSpec
from nbconvert.exporters.base import export, get_exporter
import sys, imp
from pathlib import Path
from os.path import sep, curdir, extsep, exists
from nbconvert import get_exporter, preprocessors
from nbformat import v4
from nbformat import *
from importlib import reload
PY2 = sys.version_info.major is 2

from inspect import *


# In[3]:


exporter = get_exporter('python')()


# In[4]:


class Importable(Base, object):
    """Base class for Python 2 or Python 3 imports.  Python 2 imports are not reloadable."""
    def find_spec(self, name, paths, target=None):
        loader =  self.find_module(name, paths, target)
        return loader and spec_from_loader(name, loader)

    def find_module(self, name, paths, target=None):
        for ext in type(self.ext) is str and [self.ext] or self.ext:
            for path in paths or [curdir]:
                path = Path(name).with_suffix('.'+ext)
                if path.exists(): 
                    return type(self)(name, str(path))
        return None

    def create_module(self, spec):
        return ModuleType(self.name)
    
    def exec_module(self, module):
        for cell in reads(Path(self.path).read_text(), 4).cells:
            try:
                code = self.func(cell)
                exec(code, module.__dict__, module.__dict__)
            except:
                raise RuntimeError(code)
        return module    
    
    def get_source(self, path):
        return exporter.from_filename(path)[0]


# > `finder` all custom extensions.

# In[5]:


def finder(ext, bases=[], **kwargs):
    def add_finder(finder):
        global meta_paths
        sys.meta_path.append(finder(None, None)), meta_paths.append(sys.meta_path[-1])
        return finder
    
    def importer(func):
        return add_finder(type(
            func.__name__, (Importable,), kwargs.update(func=func, ext=ext) or kwargs))
    return importer


# > `load_ipython_extension` and `unload_ipython_extension` are `ipython` namespaces; they define the `%load_ext` and `%unload_ext`, respectively. 

# In[6]:


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
        if _ in meta_paths: 
            sys.meta_path.pop(sys.meta_path.index(_))
    sys.path_importer_cache.clear()

unload = unload_ipython_extension


# ## Notebook importer

# > an `nbconvert` exporter to create python code from notebooks.

# In[7]:


def Ipynb(self, cell):
    return exporter.from_notebook_node(v4.new_notebook(cells=[cell]))[0]


# In[ ]:


#     load_ipython_extension()


# In[ ]:


if __name__ == '__main__':
    get_ipython().system('jupyter nbconvert --to python importable.ipynb')

