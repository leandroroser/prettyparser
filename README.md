
![icon](https://user-images.githubusercontent.com/10769732/140849995-fba5d146-9317-4324-b200-b6a3f6b0a07a.png)
===========


prettyparser is a library for parsing PDF/TXT and Python objects with text (str, list) using regular expressions. In case of PDF files, the package reads the content using pdfplumber and then performs a series of
data manipulations to generate better output. The package allows to customize the data processing steps.


## Installation

Clone this repository:
    $ git clone https://github.com/leandroroser/prettyparser
    $ pip install -r requirements.txt


## Example: processing PDF files

```Python
import regex as re
from prettyparser import PrettyParser

directory = "./BOOKS/PDF"
output = "./BOOKS/TXT"
parser = PrettyParser(directory, output, args=[[r"(\n\s*\d+\s*\n)|(\n\s*\d+\s*$)", r'\n\n'],
                                                [r"\n\s*-\d-\s*\n", r'\n\n'], 
                                                [r"\n\s*(\* *)+\s*\n", r'\n\n'],
                                                [r"__some_header_text", r'\n\n', re.IGNORECASE],
                                                remove_whitelines = True,
                                                paragraphs_spacing = 1,
                                                join_broken_words = True,
                                                mode = 'pdf')
parser.run()
```


```Python
import regex as re
from prettyparser import PrettyParser


txt = """
header to remove

This is a text with multiple problems. For exam-
ple the latter word can be joined. 
The portions of this line can be
joined
in a single line.
HERE ALSO IS SOME
TEXT IN UPPERCASE
TO JOIN
Some Other Ugly Stuff To Remove IGNORING Case. 

Remove the line below:

* * * 

Remove empty lines and finally separate each line with a blank line


Below is the page number.
99
"""
parser = PrettyParser(txt, mode = "pyobj", args=[[r"\s*header to remove\s*\n",r""],
                                                [r"(\n\s*\d+\s*\n)", '\n\n'],
                                                [r"\n\s*(\* *)+\s*\n", '\n\n'],
                                                [r"\n.*some other ugly stuff.*", '\n\n', re.IGNORECASE]],
                                                remove_whitelines = True,
                                                paragraphs_spacing = 1,
                                                join_broken_words = True)
output = parser.run()
print(output[0])
```

```
This is a text with multiple problems. For example the latter word can be joined.

The portions of this line can be joined in a single line.

HERE ALSO IS SOME TEXT IN UPPERCASE TO JOIN

Remove the line below: 

Remove empty lines and finally separate each line with a blank line Below is the page number.
```

Arguments
---------
- files (list or str): Path to parse for pdf/txt operations. If a string is passed, it will be treated as a directory when mode is 'pdf' or 'txt'. If a str or list is passed when mode is 'pyobj', it will be treated as a str/list of text files already loaded in memory in the corresponding object
- output (str): output directory.
- args (list): list of tuples of the form (regex, replacement, flags)
- mode (str): 'pdf', 'txt' or 'pyobj' (the latter for Python lists and strings)
- default (bool): if True, perform several default cleanup operations (default)
- remove_whitelines (bool): if True, remove whitespaces
- paragraphs_spacing (int): number of newlines between paragraphs
- page_spacing (str): string to insert between pages
- join_broken_words (bool): if True, join broken words
 
License
-------
© Leandro Roser, 2021. Licensed under an [Apache-2](https://github.com/leandroroser/prettyparser/blob/main/LICENSE) license.


