# pystickyn

A Python package for organizing your thoughts in sticky notes within a Jupyter Notebook.

## Features

- Create and manage sticky notes within Jupyter Notebook.
- Different types of notes available: completed, working, todo, failed, validating, and warning.
- Customize notes with colors, labels, and code snippets.
- Seamless integration with Jupyter Notebook.
- Markdown support for note content.

## Installation

Install the package using pip:

> NOTE: In this pre-release stage, you will have to install directly from the repository.

```shell
pip install git+https://github.com/samlexrod/pystickyn.git
```

```python
from pystickyn import StickyNote

# Instantiate the class
sn = StickyNote()

# Create a completed note
sn.completed("This is a completed note.")
sn.warning("This is a warning note.")
sn.todo("This is a todo note.")
sn.validation("This is a validation note.")
```


