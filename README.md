# RefugEASE

![](./assets/logo.png)

## Getting Started

1. Clone the repository
2. `cd` into the repo
3. Install necessary requirements using:

```python
pip install -r requirements.txt
```

4. In the root directory, run:

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

On login, these are set:

```python
{
                "user_id": int,
                "username": str,
                "is_admin": int, # 0 or 1
            }
```

When `MainApplication.DEBUG=TRUE`, then these are automatically set:

```python
self.DEBUG = True
if self.DEBUG:
    self.set_global_state(
        {
            "user_id": 1,
            "username": "admin",
            "is_admin": 1,
        }
    )
```

## Datetime Data Type sqlite3

sqlite3 doesn't have a `datetime` type. All of those fields are `text`.

Therefore, ensure you save any `date` values using `datetime.date`.

## Creating new view

1. Add new view file inside `views` folder. Should be named `lowercase_underscored.py` version of the view class' name.

2. Copy and paste the `views/_view_template.py` content into the file.

3. Register the view inside the `MainApplication.switch_to_view`'s `view_map` dictionary.

### View Structure

Each View is a `tk.Frame`, that inherits from the `BaseView` class, which adds the navbar and other functionality automatically.

#### `self.render_widgets()` method

This is the main method which will put widgets inside the view. These are all inside the View's `self.container` which should be the top level master for any child widgets.

#### `self.render_error_popup_window(message='YOUR MESSAGE')` method

If you need to render a simple popup window, you can use this method, which is automatically added from the `BasveView`.

#### Switching views with `self.master.switch_to_view`

Use the following command, with the key of the view to switch to the view.

```python
self.master.switch_to_view("add_edit_plan")
```


#### Accessing `global_state` dict

The `global_state` tracks useful information for the user's session e.g.

```python
{
                    "user_id": 1,
                    "username": "admin",
                    "is_admin": 1,
                }
```

To access it, first grab the global state, **update** the dictionary as required (so you don't overwrite other data), and then set the new global state:

```python
current_state = self.master.get_global_state()

current_state['new_variable'] = 'new_value'

self.master.set_global_state(current_state)
```

# Tests

Run tests using:

```python
python test.py
```

This is also automatically run on PR.

# Naming conventions

**All views / list view (any view which shows details for many entities e.g. All Plans)**:

```python
all_plans.py # python file name
class AllPlansView # view class name
```

**Detail Views (any view which shows details for a single entity e.g. Refugee Profile)**:
```python
refugee_detail.py # python file name
class RefugeeDetail # view class name
GLOBAL_STATE['refugee_id_to_view'] # global state variable
```

**Add / Edit Forms (these should all be a single view which can both add / edit) e.g. Add / Edit Plan**

```python
add_edit_plan.py # python file name
class AddEditPlanView # view class name
GLOBAL_STATE['plan_name_to_edit'] # global state variable if editing
```

