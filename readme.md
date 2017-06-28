
# importable 

> __importable__ makes files importable into python.

---

<code>pip install git+https://github.com/tonyfast/importable</code>



```python
    %load_ext importable
```

* Notebooks and markdown files are importable.


```python
    foo = 42
    import readme
    readme.foo, readme.__file__
```




    (42, './readme.ipynb')




```python
    if True and __name__ == '__main__':        
        !jupyter nbconvert --to markdown readme.ipynb
```


```python

```
