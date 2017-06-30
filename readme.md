
# importable 

> __importable__ makes files importable into python.  Files on disk should be easy to access.

---

<code>pip install git+https://github.com/tonyfast/importable</code>



```python
    foo = 42
    if __name__ == '__main__':
        import importable
```

## Import  notebooks


```python
    import readme
    readme.foo, readme.__file__
```

    Overwriting test_importable.json2





    (42, './readme.ipynb')



## Custom Finder


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




```python
    if True and __name__ == '__main__':        
        !jupyter nbconvert --to markdown readme.ipynb
```

    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 1060 bytes to readme.md

