# AccuKnox Django Trainee Assignment

A small Django project demonstrating the three Django Signals questions and the iterable `Rectangle` class.

## Requirements

- Python 3.9+
- Django (installed from `requirements.txt`)

## Setup

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

**Windows**
```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Run migrations:

```bash

python manage.py makemigrations signals_demo

python manage.py migrate
```

## Demonstrate the Django Signals answers

```bash
python manage.py demonstrate_signals
```

The command demonstrates:

1. **Synchronous execution:** the receiver finishes before execution continues after `send()`.
2. **Same thread:** the caller and synchronous receiver print the same thread identifier.
3. **Database transaction:** the `post_save` receiver runs inside the caller's `transaction.atomic()` block. An intentional exception rolls back the created row, so the final existence check prints `False`.

The transaction demonstration assumes the default SQLite database configured in this project, which supports transactions.

## Demonstrate Rectangle

```bash
python manage.py shell
```

Then run:

```python
from rectangle_demo.rectangle import Rectangle
rectangle = Rectangle(10, 5)
list(rectangle)
```

Expected result:

```python
[{'length': 10}, {'width': 5}]
```

## Run tests

```bash
python manage.py test
```

## Notes

- `signals_demo` and `rectangle_demo` are separate Django apps.
