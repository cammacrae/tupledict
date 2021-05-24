# Tupledict

[![build](https://github.com/cammacrae/tupledict/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/cammacrae/tupledict/actions/workflows/ci.yml)

## Classes

* DictList
* TupleDict


You can use add this using poetry by running (it's not pushed to PyPI):

```$ poetry add git+https://github.com/cammacrae/tupledict.git```

Some examples:

```python
>>> from tupledict import TupleDict
```

The constructor accepts no arguments:
```python
>>> td = TupleDict()
```

Or a dict:
```python
>>> td = TupleDict({"one": 1, "two": 2})
```

Or an iterable containing key, value pairs:
```python
>>> td = TupleDict([("one", 1), ("two", 2)])
```

It also accepts keyword arguments:
```python
>>> td = TupleDict(one=1, two=2)
```

Or a mixed bag:
```python
>>> td = TupleDict({"one": 1, "two": 2}, three=3, four=4)
```
