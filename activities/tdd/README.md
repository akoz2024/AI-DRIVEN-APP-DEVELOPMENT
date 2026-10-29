# In-class Activity 16: TDD

A Django to-do app (`superlists`) built test-first, following the red/green/refactor loop:
write a failing test, write the least code to pass it, then clean up.

- `functional_tests.py`: Selenium drives Firefox through the user story (title, `<h1>`, input box, list table).
- `lists/tests.py`: Django unit tests (`assertTemplateUsed`, `assertContains`).
- `lists/views.py`, `lists/templates/home.html`, `superlists/urls.py`: the home page.

## Run it

```bash
python3.14 -m venv .venv
source .venv/bin/activate        # Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt

python manage.py test            # unit tests: 2 pass

python manage.py runserver       # in a second terminal
python functional_tests.py       # fails on purpose at self.fail("Finish the test!")
```

The functional test passes every element check and stops at `self.fail("Finish the test!")`.
That's where the class demo ended: the next step is entering and saving to-do items.
