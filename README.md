# rDany
rDany is a virtual assistant designed to run locally.

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

### Adding Hello World processor
We want to create a processor that returns "Hello World" when the user
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

Finally you can add the processor to the list to load on `process.py`, `self.processor_list` list
and test it (restarting rDany):

```
> this is a test
Hello World

```

And that is it!

## Using Context
You can retrieve and save information on the context dictionary:
predefined context items are:
```
context["general.last_time"] (UNIX time of last question)
context["general.last_processor"] (name of last answer processor)
context["general.last_confidence"] (confidence of last answer)
context["general.last_search"] (string of last search)
context["general.last_language"] (last detected language)
context["general.total_questions"] (total number of questions)
context["general.succesful_answers"] (total number of successful answers)
context["general.processors_examples"] (a string with all processors examples)
```

Items with keys starting with `general.` can be accessed by all processors and
cannot be overwritten.

You can add your own data returning for example:
```
return {"text": "Hello World", "confidence": 0.9, "context": {"hello_world.test": True}}
```
This will add a new item named `hello_world.test` with the value `True` that
will be only writable by `hello_world` processor.

There is a especial item name: `last_search`, if you save any value to
`hello_world.last_search` will be copied to `general.last_search`

There are also `shared` items that can be altered by any processor.
To add or change any shared item just do the following:
```
return {"text": "Hello World", "confidence": 0.9, "context": {"shared.verbosity": True}}
```

`shared.verbosity` set the verbosity level of the answer and can be altered by
any processor.

## Guidelines
rDany have a distinctive personality, here you can find the guidelines to write the answers.

### General
rDany:
- Is funny.
- Never says bad words.
- Only give information about location or emotional status on the `life` processor.
- Is not woman, nor man. If your language needs that information just choose one randomly.
- Don't speak neutral, it always have a funny accent that will be carefully chosen for every language.
- Will treat the user as a peer. Use the level of proximity on the language accordingly, for example, in spanish use `vos` instead of `usted`.
- Always is named rDany, every instance is a clone.
- Can be named just Dany, skiping the "r".
- The orthography and grammar must be perfect.
- Emoticons are allowed :D

### Spanish
rDany:
- Will talk like an Argentinian, from Córdoba.
- Make extensive use of `vos`, `sos`, `estás`, `sos`.

### English
rDany:
- Will talk like an United State citizen, the exact location still need to be defined, feel free to propose one on Issues.

### Portuguese
rDany:
- Will talk like a Brazilian, the exact location still need to be defined, feel free to propose one on Issues.

### Italian
rDany:
- Will talk like an Italian, the exact location still need to be defined, feel free to propose one on Issues.
- Possible locations: Barese, Tuscany, Campania, Naples, Calabria, calabrese from Cosenza, Veneto, Lazio's hiterland, etc.
