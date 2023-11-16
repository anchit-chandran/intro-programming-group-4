# intro-programming-group-4

## Setup

In the root directory, run:

```python
python main.py
```

## Global State

Global state variables can be accessed through `MainApplication.get_global_state()` and `MainApplication.set_global_state()`.

## Datetime Data Type sqlite3

sqlite3 doesn't have a `datetime` type. All of those fields are `text`.

Therefore, ensure you save any `datetime` values using the Python `datetime` object's `.strftime('%Y-%m-%d %H:%M:%S')` method.