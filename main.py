
import click
from prettyparser import PrettyParser
import multiprocessing

@click.command()
@click.option('--files', type=click.Path(exists=True), multiple=True, default=None,
              help='Path with files to parse for pdf/txt operations or list with text.')
@click.option('--directories', type=click.Path(exists=True), multiple=True, default=None,
              help='Paths with folders to parse for pdf/txt operations. '
                   'If a string is passed, it will be treated as a directory when mode is "pdf" or "txt". '
                   'If a str or list is passed when mode is "pyobj", '
                   'it will be treated as a str/list of text files already loaded in memory in the corresponding object.')
@click.option('--output', type=click.Path(), default=None, help='Output directory.')
@click.option('--args', type=(str, str, int), multiple=True, default=None, help='List of tuples of the form (regex, replacement, flags). The flag can be absent.')
@click.option('--mode', type=click.Choice(['pdf', 'txt', 'list']), default="pdf", help='"pdf", "txt" or "list".')
@click.option('--default', type=click.BOOL,default=True,  help='If True, perform several default cleanup operations.')
@click.option('--remove_whitelines', type=click.BOOL,default=False, help='If True, remove whitespaces.')
@click.option('--paragraphs_spacing', type=click.INT,default=0, help='Number of newlines between paragraphs.')
@click.option('--page_spacing', type=click.STRING, default="\n\n",help='String to insert between pages.')
@click.option('--remove_hyphen_eol', type=click.BOOL, default=False, help='If True, if True, remove end of line hyphens and merge subwords.')
@click.option('--custom_pdf_fun', type=click.STRING, default=None, help='Custom lambda function to parse pdf files. Parse the function as a string.'
                                                                             'It must accept a pdfplumber page as argument and return a text to be joined with previous pages.')
@click.option('--overwrite', type=click.BOOL, default=False, help='Overwrite file if exists. Default: False.')
@click.option('--n_jobs', type=click.INT, default= multiprocessing.cpu_count() - 2, help='Number of jobs. Default: number of cores -2.')
def main(files, directories, output, args, mode, default, remove_whitelines, paragraphs_spacing, page_spacing, remove_hyphen_eol, custom_pdf_fun, overwrite, n_jobs):
    if custom_pdf_fun is not None:
        custom_pdf_fun = eval(custom_pdf_fun)
    files = list(files)
    directories = list(directories)
    if len(files) == 0:
        files = None
    if len(directories) == 0:
        directories = None
    parser = PrettyParser(files = files, directories = directories, 
                output = output, mode = mode, 
                default = default, remove_whitelines = remove_whitelines, 
                paragraphs_spacing =  paragraphs_spacing,
                page_spacing =page_spacing, remove_hyphen_eol = remove_hyphen_eol, 
                custom_pdf_fun = custom_pdf_fun,
                overwrite = overwrite,
                n_jobs = n_jobs)
    parser.run()


if __name__ == '__main__':
    main()

