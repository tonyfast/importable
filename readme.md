
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




    (42, './readme.ipynb')




```python
    if True and __name__ == '__main__':        
        !jupyter nbconvert --to markdown readme.ipynb
```

    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 655 bytes to readme.md

