
# coding: utf-8

# 😵 simple __import__s for notebooks and markdown files.  All code elements are executed in order and imported into sys models.

# In[ ]:


__all__, meta_paths, path_hooks = [], [], []


# In[2]:


from literacy.preprocessors import Explode, JoinSource
from importlib.util import spec_from_loader
from importlib.machinery import SourceFileLoader, FileFinder
from nbconvert.exporters.base import export, get_exporter
import sys
from os.path import sep, curdir, extsep, exists
from nbconvert import get_exporter, export
from nbformat.v4 import  new_notebook, new_code_cell


# In[3]:


class Importable(object):
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.Loader, staticmethod):
            cls.Loader = staticmethod(cls.Loader)
        return super(Importable, cls).__new__(cls, *args, **kwargs)

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


class Ipynb(Importable):
    ext = 'ipynb'
    class Loader(SourceFileLoader):
        def get_code(self, nb):
            return exporter.from_filename(self.path)[0].encode('utf-8')


# In[6]:


class BaseLoader(SourceFileLoader):
    def get_code(self, *args):
        with open(self.path) as f:
            return f.read()


# In[7]:


class Md(Importable):
    ext = 'md'
    class Loader(BaseLoader):
        def get_code(self, path):
            return exporter.from_notebook_node(new_notebook(cells=[new_code_cell(
                super().get_code()
            )]))[0].encode('utf-8')


# In[8]:


class Yaml(Importable):
    ext = ['yml', 'yaml']
    class Loader(BaseLoader):
        def get_code(self, path):
            return """data = __import__('yaml').safe_load(\"\"\"{}\"\"\")
            """.strip().format(super().get_code()).encode('utf-8')


# In[15]:


def pandas_loader(ext):
    class Pandas(Importable):
        class Loader(BaseLoader):
            def get_code(self, path):
                return """data=__import__("pandas").read_{ext}("{name}")""".format(
                    ext=ext, name=self.path)
    return type(ext.capitalize(), (Pandas,), {'ext': ext})


# In[16]:


def add_finder(finder):
    sys.meta_path.append(finder())
    meta_paths.append(sys.meta_path[-1])
    for ext in [finder.ext] if isinstance(finder.ext, str) else finder.ext:
        sys.path_hooks.append(FileFinder.path_hook((finder.Loader, [extsep+ext])))
        path_hooks.append(sys.path_hooks[-1])


# In[17]:


def load_ipython_extension(ip=get_ipython()):
    for finder in [Ipynb, Md, Yaml, pandas_loader('csv')]:
        add_finder(finder)
    sys.path_importer_cache.clear()


# In[18]:


def unload_ipython_extension(ip=get_ipython()):
    for _ in sys.meta_path:
        if _ in meta_paths: sys.meta_path.pop(sys.meta_path.index(_))
    for _ in sys.path_hooks:
        if _ in path_hooks: sys.path_hooks.pop(sys.path_hooks.index(_))
    sys.path_importer_cache.clear()


# In[ ]:


if __name__ == '__main__': 
    get_ipython().system('jupyter nbconvert --to script importable.ipynb')


# In[ ]:




