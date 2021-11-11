#!/usr/bin/env python

import pdfplumber
import regex as re
import time
from tqdm import tqdm
from typing import (Union,
                    Optional,
                    Callable,
                    List)
import os

class PrettyParser:
    """Parse pdf/txt files or python strings/lists and perfom cleanup operations to enhance the text quality

    Args:
        files (list or str): Path to parse for pdf/txt operations
        If a string is passed, it will be treated as a directory when mode is 'pdf' or 'txt'
        If a str or list is passed when mode is 'pyobj', 
        it will be treated as a str/list of text files already loaded in memory in the corresponding object
        output (str): output directory
        args (list): list of tuples of the form (regex, replacement, flags). The flag can be absent.
        mode (str): 'pdf', 'txt' or 'list'
        default (bool): if True, perform several default cleanup operations
        remove_whitelines (bool): if True, remove whitespaces
        paragraphs_spacing (int): number of newlines between paragraphs
        page_spacing (str): string to insert between pages
        remove_hyphen_eol (bool): if True, if True, remove end of line hyphens and merge subwords
        custom_pdf_fun (Callable): custom function to parse pdf files
        It must accept a pdfplumber page as argument and return a text to be joined with previous pages

    Returns:
        list or str: list of parsed files or string when output = None
    """
    def __init__(self, files:Union[str, List[str]], output:str = None, args:list = None, mode:str = "path", 
                 default:bool = True, remove_whitelines:bool = False, paragraphs_spacing:int = 0,
                 page_spacing:str = "\n\n", remove_hyphen_eol:bool = False, custom_pdf_fun = None):
        
        self.files = files
        self.output = output
        if args:
            if not isinstance(args, list):
                raise TypeError("args must be a list or a string")
            flags = [x[2] if len(x) == 3 else 0 for x in args]
            replace = [x[1] for x in args]
            patterns = [x[0] for x in args]
            self.args = [[re.compile(arg, flags = flag), rep] for arg,flag,rep in zip(patterns,flags,replace)]
        else:
            self.args = None
        if not mode in ["pdf", "txt", 'pyobj']:
            raise ValueError("mode must be 'pdf', 'txt' or 'pyobj'")
        self.mode = mode
        self.default = default
        self.remove_whitelines = remove_whitelines
        self.paragraphs_spacing = "\n" * (paragraphs_spacing + 1) if paragraphs_spacing else None
        self.page_spacing = page_spacing
        self.remove_hyphen_eol = remove_hyphen_eol
        self.custom_pdf_fun = custom_pdf_fun

        upper = "A-ZÀÂÄÁÈÊËÉÎÏÍÔÖÓÙÛÜÚÑßŸÇÕ"
        lower = "a-zàâäáèéêëíîïôöóùûüúñßÿçõ"
        chars = ",\(\[{;\'\"—"
        self.p1 = re.compile(fr"([{lower}0-9]+[ \t]*[,;:\]*[0-9]*)([{chars}]?[ \t]*)(\n+)")
        self.p2 = re.compile(fr"([{upper}]+[ \t]*[,;:\-]*[0-9]*)([{chars}]?[ \t]*?)(?:\n+)([{upper}]+[ \t])")
        self.p3 = re.compile(fr"(([n|N]°)|•)([ \t]*\n[ \t]*)+")
        self.p4 = re.compile(r"[ \t]+")
        self.p5 = re.compile(r"(?<=\n)[ \t]+")
        #self.p6 = re.compile(fr"(?<=[.])(\n+?)([{lower}.]+)")
        self.p7 = re.compile(r"(?<=[.]\n)(\s[ \t]*?)([\w\—\-]+?)")
        self.p8 = re.compile(r"([.\?!\w])([ \t]*?\n)")
        self.p9 = re.compile(r"(^\s+)|\s+$")
        self.p10 = re.compile(r"\n+")
        self.p11 = re.compile(fr"(-)(?:[ \t]*?[\d]*?\n+[ \t]*?)([{lower}{upper}])")
        #self.p7 = re.compile(r"([.,;])(\w)", flags= re.UNICODE)
        #self.pend = re.compile(r"( *\n *)+")
        if output:
            if not os.path.exists(output):
                os.makedirs(output)
    
    def cleanup(self, x:str)->str:
        """
        Args:
            x (str): string to clean up
        Returns:
            str: cleaned up string
        """
        if self.args:
            for arg,rep in self.args:
                x = arg.sub(rep, x)
        if self.default:
            x = self.p1.sub(r"\1\2 ", x)
            for _ in range(2):
                x = self.p2.sub(r"\1\2 \3", x)
            x = self.p3.sub(r"\1 ", x)
            x = self.p4.sub(" " , x)
            x = self.p5.sub("" , x) 
            #x = self.p6.sub(lambda y: y.group(2).title() if not y.group(2).startswith('.') else y.group(2), x)
            if self.remove_whitelines:
                x = self.p7.sub(r"\2", x)
            if self.remove_hyphen_eol:
                x = self.p11.sub(r"\2", x)
            if self.paragraphs_spacing:
                x = self.p8.sub(fr"\1{self.paragraphs_spacing}", x)
        #x = self.p7.sub(lambda y: y.group(1) + " " + y.group(2).upper(), x)
        return x


    def pretty_parser_pdf(self, directory:str, filename:str, i:int)->str:
        """
        Args:
            directory (str): directory of the pdf file
            filename (str): name of the pdf file
            i (int): page index of the pdf file
        Returns:
            str: cleaned up string
        """
        fullpath = os.path.join(directory, filename)
        print("Parsing... " + fullpath)
        all_text = ''
        with pdfplumber.open(fullpath) as pdf:
            for pdf_page in tqdm(pdf.pages, total = len(pdf.pages)):
                if self.custom_pdf_fun:
                    single_page_text = self.custom_pdf_fun(pdf_page)
                    if not single_page_text:
                        continue
                    else:
                        all_text += single_page_text
                else:
                    single_page_text = pdf_page.extract_text()
                    if not single_page_text:
                        continue
                    all_text = all_text + (self.page_spacing if i!=1 else "") + single_page_text
        return all_text
    

    def pretty_parser_txt(self, directory:str, filename:str)->str:
        """
        Args:
            directory (str): directory of the txt file
            filename (str): name of the txt file
        Returns:
            str: cleaned up string
        """
        fullpath = os.path.join(directory, filename)
        print("Parsing... " + fullpath)
        with  open(fullpath, 'r') as f:
            all_text = f.read()
        return all_text

    def pretty_parser_list(self, textlist:list)->Union[str, List[str]]:
        """
        Args:
            textlist (list): list of strings
        Returns:
            str: cleaned up string
        """
        number_files = len(textlist) if isinstance(textlist, list) else 1
        out = []
        time_average = 0
        textlist = textlist if isinstance(textlist, list) else [textlist]
        for i,filename in enumerate(textlist):
            try:
                start = time.time()
                cl = self.cleanup(filename)
                if self.default:
                    cl = self.p9.sub("" , cl)
                if self.paragraphs_spacing:
                    cl = self.p10.sub(self.paragraphs_spacing, cl)
                out.append(cl)
                end = time.time()
                time_average = time_average + (end - start)
                print(f"\033[92m * Time average: {time_average/(i+1):.2f} seconds/file \033[0m")
                print(f"\033[92m * Done: { 100 *(i+1)/(number_files):.1f} % \033[0m")
            except Exception as e:
                print(f"\033[91m + Error: {e} \033[0m")
        return out

    
    def parse_files(self, datatype:str)->Callable[[str, str], Optional[List[str]]]:
        """
        Args:
            datatype (str): type of the data to parse
        Returns:
            list: list of cleaned up strings
        """
        def wrapper(directory, output):
            total_files = os.listdir(directory)
            number_files = len(total_files)
            out = {}
            time_elapsed = 0

            for i,filename in enumerate(total_files):
                try:
                    if filename.endswith(datatype):
                        start = time.time()
                        if datatype == 'pdf':
                            all_text = self.pretty_parser_pdf(directory, filename, i)
                        elif datatype == 'txt':
                            all_text = self.pretty_parser_txt(directory, filename)
                        else:
                            raise TypeError("datatype must be 'pdf' or 'txt'")

                        all_text = self.cleanup(all_text)
                        all_text = self.p9.sub("" , all_text)
                        if self.paragraphs_spacing:
                            all_text = self.p10.sub(self.paragraphs_spacing, all_text)
                        if output:
                            outpath = f'{output}/{re.sub(".pdf", ".txt", filename)}'
                            with open(outpath, 'w') as f:
                                f.write(all_text) 
                                f.close()
                            print(f"\033[92m * Written to: {outpath} \033[0m")
                        else:
                            out[filename] = all_text
                        end = time.time()
                        time_elapsed += (end - start)
                        print(f"\033[92m * Time average: {time_elapsed/(i+1):.2f} seconds/book \033[0m")
                        print(f"\033[92m * Time elapsed: {time_elapsed/60:.2f} minutes \033[0m")
                        print(f"\033[92m * Processed files: { 100 *(i+1)/(number_files):.1f} % \033[0m")
                except Exception as e:
                    print(f"\033[91m + Error: {e} \033[0m")
                if not output:
                    return out
        return wrapper
    
    def run(self)->Optional[Union[str, List[str]]]:
        """
        Returns:
            list: list of cleaned up strings
        """
        if (self.mode == "pdf") or (self.mode == "txt"):
            if not os.path.exists(self.files):
                raise FileNotFoundError(f"{self.files} not found")
            parser = self.parse_files(self.mode)
            out = parser(self.files, self.output)
            if not self.output:
                return out
        else:
            if not isinstance(self.files, (list, str)):
                raise TypeError("files must be a list or str")
            out = self.pretty_parser_list(self.files)
            return out



