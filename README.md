# intro-programming-group-4

## Setup

In the root directory, run:

```python
python main.py
```

## SQL Querying

Use the helper function `run_query_get_rows` to perform most SQL queries:

```python
from utilities.db import run_query_get_rows

users = run_query_get_rows(query="SELECT * FROM User*")
```

This accepts a SQL `query` (str) as its only arg and returns a list of dictionaries containing rows.

You can **insert values** using `insert_query_with_values`. See its use inside db.py for further details.

## Global State

Global state variables can be accessed through `MainApplication.get_global_state()` and `MainApplication.set_global_state()`.

## Datetime Data Type sqlite3

sqlite3 doesn't have a `datetime` type. All of those fields are `text`.

Therefore, ensure you save any `datetime` values using `convert_to_sqlite3_date` helper function.
