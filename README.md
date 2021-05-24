# Tupledict

[![build](https://github.com/cammacrae/tupledict/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/cammacrae/tupledict/actions/workflows/ci.yml)

## Classes

* DictList
* TupleDict


You can use add this using poetry by running (it's not pushed to PyPI):

```zsh
$ poetry add git+https://github.com/cammacrae/tupledict.git
```

Some examples:

```python
>>> from tupledict import TupleDict
```

### Constructor

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

### Retrieving values

We can then retrieve our values as we would with a dict:
```python
>>> td['one']
1
```

TupleDict also implements a select method for this purpose:
```python
>>> td.select('one')
1
```

```select()``` also works with a list of keys:
```python
>>> td.select(['one', 'two'])
[1, 2]
```

which returns a list of values matching the keys. The keys needn't exist:
```python
>>> td.select(['one', 'three'])
[1]
```

and wildcards ```python "*"``` are accepted:
```python
>>> td.select("*")
[1, 2]
```









