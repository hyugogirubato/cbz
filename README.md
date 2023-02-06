# pydvdfab
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Release](https://img.shields.io/github/release-date/hyugogirubato/pycbzhelper?style=plastic)](https://github.com/hyugogirubato/pycbzhelper/releases)
![Total Downloads](https://img.shields.io/github/downloads/hyugogirubato/pycbzhelper/total.svg?style=plastic)

Python library to create a cbz file with metadata.

# Usage

### Basic Usage

```python
>>> import os
>>> from pycbzhelper import Helper
>>> metadata = {
>>>     "Title": "T1 - Arrête de me chauffer, Nagatoro",
>>>     "Series": "Arrête de me chauffer, Nagatoro",
>>>     "Number": "1",
>>>     "Count": 8,
>>>     "Volume": 1
>>>     ...
>>> }
>>> ...
>>> helper = Helper(metadata)
>>> helper.save_cbz(
...     path=os.path.join("eBooks", "Arrête de me chauffer, Nagatoro"),
...     file="T1 - Arrête de me chauffer, Nagatoro",
...     clear=False,
...     replace=True
... )
```

# Installation

To install, you can either clone the repository and run `python setup.py install`

## About
- Graphical metadata editing software [here](https://github.com/comictagger/comictagger)
- Standard ComicInfo file structure information [here](https://github.com/Kussie/ComicInfoStandard)
- New version of ComicInfo file structure [here](https://github.com/anansi-project/comicinfo)