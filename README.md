
![icon](https://user-images.githubusercontent.com/10769732/140857203-e0580717-52c3-4cdd-affc-00ad5bf0a526.png)
===========


prettyparser is a library for parsing PDF/TXT and Python objects with text (str, list) using regular expressions. 
In case of PDF files, the package reads the content using pdfplumber and then performs a series of
data manipulations to generate a higher quality output, removing the boilerplate code needed to read/write the content. A custom processing function using pdfplumber that takes a page and return a processed text is also allowed. Additional data processing steps can be customized with custom regular expressions.


## Installation

```
Clone this repository:
    $ git clone https://github.com/leandroroser/prettyparser
    $ cd prettyparser
    $ pip install -e .
```

<span style="color:orange;">Word up</span>

## Example: processing a folder with multiple PDF files

```Python
import regex as re
from prettyparser import PrettyParser

directory = "./BOOKS/PDF"
output = "./BOOKS/TXT"
parser = PrettyParser(directory, output, mode = 'pdf' 
                      args = [[r"(\n\s*\d+\s*\n)|(\n\s*\d+\s*$)", r'\n\n'],
                            [r"\n\s*-\d-\s*\n", r'\n\n'], 
                            [r"\n\s*(\* *)+\s*\n", r'\n\n'],
                            [r"__some_header_text", r'\n\n', re.IGNORECASE]],
                            remove_whitelines = True,
                            paragraphs_spacing = 1,
                            join_broken_words = True)
parser.run()
```

## Example: processing a Python str

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

Remove empty lines and finally separate each line with a blank line.


Below is the page number.
99
"""
parser = PrettyParser(txt, mode = "pyobj", args = [[r"\s*header to remove\s*\n",r""],
                                                    [r"(\n\s*\d+\s*\n)", r'\n\n'],
                                                    [r"\n\s*(\* *)+\s*\n", r'\n\n'],
                                                    [r"\n.*some other ugly stuff.*", 
                                                    r'\n\n', re.IGNORECASE]],
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

Remove empty lines and finally separate each line with a blank line.

Below is the page number.
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
- custom_pdf_fun (Callable): custom function to parse pdf files.
  It must accept a pdfplumber page as argument and return a text to be joined with previous pages.

Current languages support for the default parser
------------------------------------------------
English, Spanish, German, French 

License
-------
© Leandro Roser, 2021. Licensed under an [Apache-2](https://github.com/leandroroser/prettyparser/blob/main/LICENSE) license.


