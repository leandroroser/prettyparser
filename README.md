![icon](https://user-images.githubusercontent.com/10769732/140849397-d0cf1c44-2d57-4318-80f4-3530ac0df98f.png)
===========


prettyparser is a library for parsing PDF/TXT and Python objects with text (str, list) using regex expressions. The package allows to read PDF files using pdfplumber and then performs a series of
data manipulations to generate better output. The package allows to customize the data processing steps.


- Processing PDF files

```Python
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
 
License
-------
© Contributors, 2021. Licensed under an [Apache-2](https://github.com/dmlc/xgboost/blob/master/LICENSE) license.


