# rDany
rDany is a virtual assistant designed to locally.

Features:
- Lightweight
- Multilanguage
- Modular

## Installation

```
$ mkdir rdany
$ cd rdany
$ git clone https://github.com/Eibriel/rdany.git
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r rdany/requirements.txt
(venv)$ cp rdany/config_example.py rdany/config.py
(venv)$ python rdany/rdany.py
```

To start ask:
```
> ¿Qué puedes hacer?
```
## Improving rDany

On `processors` folder are all the different "skills" for rDany
separated by language.

### Adding Hello World skill
We want to create a skill that returns "Hello World" when the user
says "this is a test"

Create the file `processor/es/hello_world.py` and add the following content:

```
import re
```

We will be using Regular Expressions.
Then add:

```
class processor:
    example = "This is a test"
    keywords = [
        "this",
        "test"
    ]
```

This code initializes the `processor` class, and we add an example
(must be well written, following grammar rules), and we add a list
of keywords that will be used to detect the language.

Then we add:

```

    @staticmethod
    def check_string(string, context):
        asktest = re.search(r"this\s+is\s+a\s+test", string, re.IGNORECASE)
        if asktest:
            return {"text": "Hello World", "confidence": 0.9, "context": {}}
```

We define `check_string` function, that takes the `context` parameter (unused here)
test the string against the regular expresion, and if the search is
successful returns a text `Hello World`, with a confidence of `0.9`, and we
don't change context, so it returns `{}`

And tat is it.

Now you can add the skill to the list to load on `process.py`, `self.processor_list` list
and
