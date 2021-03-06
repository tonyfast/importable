
# importable 

`pip install git+`<a href="https://github.com/tonyfast/importable"><code>https://github.com/tonyfast/importable</code></a>

> __importable__ is an IPython magic that permits python imports from notebook sources. [See the source.](https://github.com/tonyfast/importable/blob/master/importable.ipynb)


```python
    %reload_ext importable 
```


```python
    foo = 42
    import readme
    readme.foo, readme.readme, readme.__file__
```




    (42, <module 'readme' from './readme.ipynb'>, './readme.ipynb')



Once __importable__ is loaded any notebook can be used as source.  For example, [literacy](https://github.com/tonyfast/literacy) is a literate programming extension for the notebook [written with notebooks as source](https://github.com/tonyfast/literacy/blob/master/literacy/__init__.py#L1).

__importable__ works in Python 2 and 3, reloading only works in python 3.

# Installation

`pip install git+`<a href="https://github.com/tonyfast/importable"><code>https://github.com/tonyfast/importable</code></a>

## Advanced: Custom Finder


```python
    from importable import finder
```


```python
    if __name__ == '__main__':
        with open('test_file.json', 'w') as f: __import__('json').dump(['foo', 'bar'], f)
```


```python
    @finder('json')
    def load_json(self, path):
        """Import files ending in json"""
        return """with open('{}') as f: data = __import__('json').load(f)
        """.strip().format(self.path)
```


```python
    import test_file
    test_file.data
```




    ['foo', 'bar']




```python
    if True and __name__ == '__main__':        
        !jupyter nbconvert --to markdown readme.ipynb
```

## References

* http://brandonio21.com/2016/10/custom-fileextension-path-based-importers-in-python/
* https://chaobin.github.io/2015/06/22/understand-import-system-of-python/
* http://xion.org.pl/2012/05/06/hacking-python-imports/
* https://android.googlesource.com/toolchain/benchmark/+/master/python/src/Demo/imputil/importers.py
* https://docs.python.org/2.7/library/imputil.html
* PEPs: [302](https://www.python.org/dev/peps/pep-0302/), [420](https://www.python.org/dev/peps/pep-0420/), [451](https://www.python.org/dev/peps/pep-0451/)
