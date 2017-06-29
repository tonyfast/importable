
# importable 

> __importable__ makes files importable into python.  Files on disk should be easy to access.

---

<code>pip install git+https://github.com/tonyfast/importable</code>



```python
    foo = 42
    if __name__ == '__main__':
        %load_ext importable
```

## Import  notebooks


```python
    import readme
    readme.foo, readme.__file__
```

    Writing test_importable.json2





    (42, './readme.ipynb')



## Loader


```python
    from importable import finder
```


```python
    %%file test_importable.json2
    ["foo", "bar"]
```

    Overwriting test_importable.json2



```python
    @finder('json2')
    def load_json2(self, path):
        """Import files ending in json2"""
        return """with open('{}') as f: data = __import__('json').load(f)
        """.strip().format(self.path)
```


```python
    import test_importable
    test_importable.data
```




    ['foo', 'bar']



## Notes

* This project uses notebooks as source code.  The only python file is __init__.py.  All other modules using the <code>importable.Ipynb</code> __loader__.


```python
    import importable
    importable.stream.__file__
```




    '/Users/tonyfast/importables/importable/stream.ipynb'




```python
    if True and __name__ == '__main__':        
        !jupyter nbconvert --to markdown readme.ipynb
```

    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 1152 bytes to readme.md

