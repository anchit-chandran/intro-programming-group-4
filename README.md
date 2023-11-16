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

Therefore, ensure you save any `datetime` values using `convert_to_sqlite3_date` helper function.
