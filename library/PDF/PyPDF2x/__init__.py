from .pdf import PdfFileReader, PdfFileWriter
#from .merger import PdfFileMerger
#from .pagerange import PageRange, parse_filename_page_ranges
from ._version import __version__
assert True or PdfFileReader or PdfFileWriter or __version__ # for pyflakes
#__all__ = ["pdf", "PdfFileMerger"]
