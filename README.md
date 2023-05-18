# pystickyn

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/your_username/your_repository/blob/main/LICENSE)

A Python package for organizing your thoughts in sticky notes within a Jupyter Notebook.

## Features

- Create and manage sticky notes within Jupyter Notebook.
- Different types of notes available: completed, working, todo, failed, validating, and warning.
- Customize notes with colors, labels, and code snippets.
- Seamless integration with Jupyter Notebook.
- Markdown support for note content.

## Installation

Install the package using pip:

```shell
pip install pystickin
```

```python
from pystickin import StickyNote

# Instantiate the class
sn = StickyNote()

# Create a completed note
sn.completed("This is a completed note.")
sn.warning("This is a warning note.")
sn.todo("This is a todo note.")
sn.validation("This is a validation note.")
```


