
# coding: utf-8

# 😵 simple __import__s for notebooks and markdown files.  All code elements are executed in order and imported into sys models.

# In[1]:


__all__ = 'finder',
meta_paths, path_hooks = [], []


# In[2]:


from literacy.preprocessors import Explode, JoinSource
from importlib.util import spec_from_loader
from importlib.machinery import SourceFileLoader, FileFinder
from nbconvert.exporters.base import export, get_exporter
import sys
from os.path import sep, curdir, extsep, exists
from nbconvert import get_exporter
from nbformat.v4 import  new_notebook, new_code_cell


# In[3]:


class Importable(object):
    def __new__(cls):
        if not isinstance(cls.Loader, staticmethod):
            cls.Loader = staticmethod(cls.Loader)
        return super(Importable, cls).__new__(cls)

    def find_spec(self, name, paths, target=None):
        for ext in type(self.ext) is str and [self.ext] or self.ext:
            for path in paths or [curdir]:
                path = extsep.join([sep.join([path, name.split('.')[-1]]), ext])
                if exists(path):
                    return spec_from_loader(name, self.Loader(name, path))
        return None


# In[4]:


exporter = get_exporter('python')(config={'Exporter': {'preprocessors': [Explode(), JoinSource()]}})


# In[5]:


def add_finder(finder):
    sys.meta_path.append(finder())
    meta_paths.append(sys.meta_path[-1])
    for ext in [finder.ext] if isinstance(finder.ext, str) else finder.ext:
        sys.path_hooks.append(FileFinder.path_hook((finder.Loader, [extsep+ext])))
        path_hooks.append(sys.path_hooks[-1])
    return finder


# In[6]:


def finder(ext, bases=(SourceFileLoader,), **kwargs):
    def importer(func):
        kwargs.update(get_code=func, ext=ext)
        return add_finder(type(func.__name__, (Importable,),{
            'ext': ext,
            'Loader': type(func.__name__.capitalize()+'Loader', bases, kwargs)
        }))
    return importer


# In[7]:


def Ipynb(self, path):
    return exporter.from_filename(self.path)[0].encode('utf-8')


# In[8]:


def get_stream(module, path):
    return """with open('{}', 'r') as f:
        data=__import__('{}').{}(f)""".format(path, *module.split('.', 1)).encode('utf-8')


# In[9]:


def Yaml(self, path):
    return get_stream('yaml.safe_load', self.path)


# In[10]:


def Json(self, path):
    return get_stream('json.load', self.path)


# In[11]:


def Markdown(self, path):
    with open(self.path, 'r') as f:    
        code = exporter.from_notebook_node(new_notebook(cells=[new_code_cell(
            f.read())]))[0].encode('utf-8')
    return code


# In[12]:


def Pandasify(self, path):
    return """data=__import__("pandas").read_{ext}("{name}")""".format(
        ext=self.ext, name=self.path)


# In[13]:


def load_ipython_extension(ip=get_ipython()):
    for cls, ext in [
        (Yaml, ['yml', 'yaml']), (Ipynb, 'ipynb'),# (Markdown, 'md'),
        (Json, 'json'),# (Pandasify, 'csv')
    ]:
        finder(ext)(cls)
    sys.path_importer_cache.clear()


# In[14]:


def unload_ipython_extension(ip=get_ipython()):
    for _ in sys.meta_path:
        if _ in meta_paths: sys.meta_path.pop(sys.meta_path.index(_))
    for _ in sys.path_hooks:
        if _ in path_hooks: sys.path_hooks.pop(sys.path_hooks.index(_))
    sys.path_importer_cache.clear()


# In[32]:


if __name__ == '__main__': 
    get_ipython().system('jupyter nbconvert --to script importable.ipynb')


# In[ ]:




