# Copyright (c) 2005-2012 Stephen John Machin, Lingfo Pty Ltd
# This module is part of the xlrd package, which is released under a
# BSD-style licence.
import os
import pprint
import sys
import zipfile
from library.xlwt import * 
from library.xlwt.Style import default_style

from . import timemachine
from .biffh import (
    XL_CELL_BLANK, XL_CELL_BOOLEAN, XL_CELL_DATE, XL_CELL_EMPTY, XL_CELL_ERROR,
    XL_CELL_NUMBER, XL_CELL_TEXT, XLRDError, biff_text_from_num,
    error_text_from_code,
)
from .book import Book, colname, open_workbook_xls
from .compdoc import SIGNATURE as XLS_SIGNATURE
from .formula import *  # is constrained by __all__
from .info import __VERSION__, __version__
from .sheet import empty_cell
from .xldate import XLDateError, xldate_as_datetime, xldate_as_tuple


#: descriptions of the file types :mod:`xlrd` can :func:`inspect <inspect_format>`.
FILE_FORMAT_DESCRIPTIONS = {
    'xls': 'Excel xls',
    'xlsb': 'Excel 2007 xlsb file',
    'xlsx': 'Excel xlsx file',
    'ods': 'Openoffice.org ODS file',
    'zip': 'Unknown ZIP file',
    None: 'Unknown file type',
}

ZIP_SIGNATURE = b"PK\x03\x04"

PEEK_SIZE = max(len(XLS_SIGNATURE), len(ZIP_SIGNATURE))


def inspect_format(path=None, content=None):
    """
    Inspect the content at the supplied path or the :class:`bytes` content provided
    and return the file's type as a :class:`str`, or ``None`` if it cannot
    be determined.

    :param path:
      A :class:`string <str>` path containing the content to inspect.
      ``~`` will be expanded.

    :param content:
      The :class:`bytes` content to inspect.

    :returns:
       A :class:`str`, or ``None`` if the format cannot be determined.
       The return value can always be looked up in :data:`FILE_FORMAT_DESCRIPTIONS`
       to return a human-readable description of the format found.
    """
    if content:
        peek = content[:PEEK_SIZE]
    else:
        path = os.path.expanduser(path)
        with open(path, "rb") as f:
            peek = f.read(PEEK_SIZE)

    if peek.startswith(XLS_SIGNATURE):
        return 'xls'

    if peek.startswith(ZIP_SIGNATURE):
        zf = zipfile.ZipFile(timemachine.BYTES_IO(content) if content else path)

        # Workaround for some third party files that use forward slashes and
        # lower case names. We map the expected name in lowercase to the
        # actual filename in the zip container.
        component_names = {}
        for name in zf.namelist():
            component_names[name.replace('\\', '/').lower()] = name

        if 'xl/workbook.xml' in component_names:
            return 'xlsx'
        if 'xl/workbook.bin' in component_names:
            return 'xlsb'
        if 'content.xml' in component_names:
            return 'ods'
        return 'zip'


def open_workbook(filename=None,
                  logfile=sys.stdout,
                  verbosity=0,
                  use_mmap=True,
                  file_contents=None,
                  encoding_override=None,
                  formatting_info=False,
                  on_demand=False,
                  ragged_rows=False,
                  ignore_workbook_corruption=False
                  ):
    """
    Open a spreadsheet file for data extraction.

    :param filename: The path to the spreadsheet file to be opened.

    :param logfile: An open file to which messages and diagnostics are written.

    :param verbosity: Increases the volume of trace material written to the
                      logfile.

    :param use_mmap:

      Whether to use the mmap module is determined heuristically.
      Use this arg to override the result.

      Current heuristic: mmap is used if it exists.

    :param file_contents:

      A string or an :class:`mmap.mmap` object or some other behave-alike
      object. If ``file_contents`` is supplied, ``filename`` will not be used,
      except (possibly) in messages.

    :param encoding_override:

      Used to overcome missing or bad codepage information
      in older-version files. See :doc:`unicode`.

    :param formatting_info:

      The default is ``False``, which saves memory.
      In this case, "Blank" cells, which are those with their own formatting
      information but no data, are treated as empty by ignoring the file's
      ``BLANK`` and ``MULBLANK`` records.
      This cuts off any bottom or right "margin" of rows of empty or blank
      cells.
      Only :meth:`~xlrd.sheet.Sheet.cell_value` and
      :meth:`~xlrd.sheet.Sheet.cell_type` are available.

      When ``True``, formatting information will be read from the spreadsheet
      file. This provides all cells, including empty and blank cells.
      Formatting information is available for each cell.

      Note that this will raise a NotImplementedError when used with an
      xlsx file.

    :param on_demand:

      Governs whether sheets are all loaded initially or when demanded
      by the caller. See :doc:`on_demand`.

    :param ragged_rows:

      The default of ``False`` means all rows are padded out with empty cells so
      that all rows have the same size as found in
      :attr:`~xlrd.sheet.Sheet.ncols`.

      ``True`` means that there are no empty cells at the ends of rows.
      This can result in substantial memory savings if rows are of widely
      varying sizes. See also the :meth:`~xlrd.sheet.Sheet.row_len` method.


    :param ignore_workbook_corruption:

      This option allows to read corrupted workbooks.
      When ``False`` you may face CompDocError: Workbook corruption.
      When ``True`` that exception will be ignored.

    :returns: An instance of the :class:`~xlrd.book.Book` class.
    """

    file_format = inspect_format(filename, file_contents)
    # We have to let unknown file formats pass through here, as some ancient
    # files that xlrd can parse don't start with the expected signature.
    if file_format and file_format != 'xls':
        raise XLRDError(FILE_FORMAT_DESCRIPTIONS[file_format]+'; not supported')

    bk = open_workbook_xls(
        filename=filename,
        logfile=logfile,
        verbosity=verbosity,
        use_mmap=use_mmap,
        file_contents=file_contents,
        encoding_override=encoding_override,
        formatting_info=formatting_info,
        on_demand=on_demand,
        ragged_rows=ragged_rows,
        ignore_workbook_corruption=ignore_workbook_corruption,
    )

    return bk


def dump(filename, outfile=sys.stdout, unnumbered=False):
    """
    For debugging: dump an XLS file's BIFF records in char & hex.

    :param filename: The path to the file to be dumped.
    :param outfile: An open file, to which the dump is written.
    :param unnumbered: If true, omit offsets (for meaningful diffs).
    """
    from .biffh import biff_dump
    bk = Book()
    bk.biff2_8_load(filename=filename, logfile=outfile, )
    biff_dump(bk.mem, bk.base, bk.stream_len, 0, outfile, unnumbered)


def count_records(filename, outfile=sys.stdout):
    """
    For debugging and analysis: summarise the file's BIFF records.
    ie: produce a sorted file of ``(record_name, count)``.

    :param filename: The path to the file to be summarised.
    :param outfile: An open file, to which the summary is written.
    """
    from .biffh import biff_count_records
    bk = Book()
    bk.biff2_8_load(filename=filename, logfile=outfile, )
    biff_count_records(bk.mem, bk.base, bk.stream_len, outfile)


def copy(wb):
    """
    Copy an :class:`xlrd.Book` into an :class:`xlwt.Workbook` preserving as much
    information from the source object as possible.

    See the :doc:`copy` documentation for an example.
    """
    w = XLWTWriter()
    process(
        XLRDReader(wb,'unknown.xls'),
        w
        )
    return w.output[0][1]


def process(reader, *chain):
    """
    The driver function for the :mod:`xlutils.filter` module.

    It takes a chain of one :ref:`reader <reader>`, followed by zero or more
    :ref:`filters <filter>` and ending with one :ref:`writer <writer>`.

    All the components are chained together by the :func:`process` function
    setting their ``next`` attributes appropriately. The
    :ref:`reader <reader>` is then called with the first
    :ref:`filter <filter>` in the chain.
    """
    for i in range(len(chain)-1):
        chain[i].next = chain[i+1]
    reader(chain[0])


class BaseWriter:
    """
    This is the base writer that copies all data and formatting from
    the specified sources.
    It is designed for sequential use so when, for example, writing
    two workbooks, the calls must be ordered as follows:
    
    - :meth:`workbook` call for first workbook
    - :meth:`sheet` call for first sheet
    - :meth:`row` call for first row
    - :meth:`cell` call for left-most cell of first row
    - :meth:`cell` call for second-left-most cell of first row
    - ...
    - :meth:`row` call for second row
    - ...
    - :meth:`sheet` call for second sheet
    - ...
    - :meth:`workbook` call for second workbook
    - ...
    - :meth:`finish` call

    Usually, only the :meth:`get_stream` method needs to be implemented in subclasses.
    """
    
    wtbook = None
    
    close_after_write = True

    def get_stream(self,filename):
        """
        This method is called once for each file written.
        The filename of the file to be created is passed and something with
        :meth:`~file.write` and :meth:`~file.close`
        methods that behave like a :class:`file` object's must be returned.
        """
        raise NotImplementedError

    def start(self):
        """
        This method should be called before processing of a batch of input.
        This allows the filter to initialise any required data
        structures and dispose of any existing state from previous
        batches. 
        """
        self.wtbook = None
        
    def close(self):
        if self.wtbook is not None:
            stream = self.get_stream(self.wtname)
            self.wtbook.save(stream)
            if self.close_after_write:
                stream.close()
            del self.wtbook
            del self.rdbook
            del self.rdsheet
            del self.wtsheet
            del self.style_list

    def workbook(self,rdbook,wtbook_name):
        """
        This method should be called every time processing of a new
        workbook starts.

        :param rdbook: the :class:`~xlrd.Book` object from which the new workbook
                 will be created.

        :param wtbook_name: the name of the workbook into which content
                      will be written.
        """
        self.close()        
        self.rdbook = rdbook
        self.wtbook = Workbook(style_compression=2)
        self.wtbook.dates_1904 = rdbook.datemode
        self.wtname = wtbook_name
        self.style_list = []
        self.wtsheet_names = set()
        # the index of the current wtsheet being written
        self.wtsheet_index = 0
        # have we set a visible sheet already?
        self.sheet_visible = False
        if not rdbook.formatting_info:
            return
        for rdxf in rdbook.xf_list:
            wtxf = Style.XFStyle()
            #
            # number format
            #
            wtxf.num_format_str = rdbook.format_map[rdxf.format_key].format_str
            #
            # font
            #
            wtf = wtxf.font
            rdf = rdbook.font_list[rdxf.font_index]
            wtf.height = rdf.height
            wtf.italic = rdf.italic
            wtf.struck_out = rdf.struck_out
            wtf.outline = rdf.outline
            wtf.shadow = rdf.outline
            wtf.colour_index = rdf.colour_index
            wtf.bold = rdf.bold #### This attribute is redundant, should be driven by weight
            wtf._weight = rdf.weight #### Why "private"?
            wtf.escapement = rdf.escapement
            wtf.underline = rdf.underline_type #### 
            # wtf.???? = rdf.underline #### redundant attribute, set on the fly when writing
            wtf.family = rdf.family
            wtf.charset = rdf.character_set
            wtf.name = rdf.name
            # 
            # protection
            #
            wtp = wtxf.protection
            rdp = rdxf.protection
            wtp.cell_locked = rdp.cell_locked
            wtp.formula_hidden = rdp.formula_hidden
            #
            # border(s) (rename ????)
            #
            wtb = wtxf.borders
            rdb = rdxf.border
            wtb.left   = rdb.left_line_style
            wtb.right  = rdb.right_line_style
            wtb.top    = rdb.top_line_style
            wtb.bottom = rdb.bottom_line_style 
            wtb.diag   = rdb.diag_line_style
            wtb.left_colour   = rdb.left_colour_index 
            wtb.right_colour  = rdb.right_colour_index 
            wtb.top_colour    = rdb.top_colour_index
            wtb.bottom_colour = rdb.bottom_colour_index 
            wtb.diag_colour   = rdb.diag_colour_index 
            wtb.need_diag1 = rdb.diag_down
            wtb.need_diag2 = rdb.diag_up
            #
            # background / pattern (rename???)
            #
            wtpat = wtxf.pattern
            rdbg = rdxf.background
            wtpat.pattern = rdbg.fill_pattern
            wtpat.pattern_fore_colour = rdbg.pattern_colour_index
            wtpat.pattern_back_colour = rdbg.background_colour_index
            #
            # alignment
            #
            wta = wtxf.alignment
            rda = rdxf.alignment
            wta.horz = rda.hor_align
            wta.vert = rda.vert_align
            wta.dire = rda.text_direction
            # wta.orie # orientation doesn't occur in BIFF8! Superceded by rotation ("rota").
            wta.rota = rda.rotation
            wta.wrap = rda.text_wrapped
            wta.shri = rda.shrink_to_fit
            wta.inde = rda.indent_level
            # wta.merg = ????
            #
            self.style_list.append(wtxf)
   
    def sheet(self,rdsheet,wtsheet_name):
        """
        This method should be called every time processing of a new
        sheet in the current workbook starts.

        :param rdsheet: the :class:`~xlrd.sheet.Sheet` object from which the new
                  sheet will be created.

        :param wtsheet_name: the name of the sheet into which content
                       will be written.
        """
        
        # these checks should really be done by xlwt!
        if not wtsheet_name:
            raise ValueError('Empty sheet name will result in invalid Excel file!')
        l_wtsheet_name = wtsheet_name.lower()
        if l_wtsheet_name in self.wtsheet_names:
            raise ValueError('A sheet named %r has already been added!'%l_wtsheet_name)
        self.wtsheet_names.add(l_wtsheet_name)
        l_wtsheet_name = len(wtsheet_name)
        if len(wtsheet_name)>31:
            raise ValueError('Sheet name cannot be more than 31 characters long, '
                             'supplied name was %i characters long!'%l_wtsheet_name)
        
        self.rdsheet = rdsheet
        self.wtsheet_name=wtsheet_name
        self.wtsheet = wtsheet = self.wtbook.add_sheet(wtsheet_name,cell_overwrite_ok=True)
        self.wtcols = set() # keep track of which columns have had their attributes set up
        #
        # MERGEDCELLS
        # 
        mc_map = {}
        mc_nfa = set()
        for crange in rdsheet.merged_cells:
            rlo, rhi, clo, chi = crange
            mc_map[(rlo, clo)] = crange
            for rowx in xrange(rlo, rhi):
                for colx in xrange(clo, chi):
                    mc_nfa.add((rowx, colx))
        self.merged_cell_top_left_map = mc_map
        self.merged_cell_already_set = mc_nfa
        if not rdsheet.formatting_info:
            return
        #
        # default column width: STANDARDWIDTH, DEFCOLWIDTH
        #
        if rdsheet.standardwidth is not None:
            # STANDARDWIDTH is expressed in units of 1/256 of a 
            # character-width, but DEFCOLWIDTH is expressed in units of
            # character-width; we lose precision by rounding to
            # the higher whole number of characters.
            #### XXXX TODO: implement STANDARDWIDTH record in xlwt.
            wtsheet.col_default_width = \
                (rdsheet.standardwidth + 255) // 256
        elif rdsheet.defcolwidth is not None:
            wtsheet.col_default_width = rdsheet.defcolwidth
        #
        # WINDOW2
        #
        wtsheet.show_formulas = rdsheet.show_formulas
        wtsheet.show_grid = rdsheet.show_grid_lines
        wtsheet.show_headers = rdsheet.show_sheet_headers
        wtsheet.panes_frozen = rdsheet.panes_are_frozen
        wtsheet.show_zero_values = rdsheet.show_zero_values
        wtsheet.auto_colour_grid = rdsheet.automatic_grid_line_colour
        wtsheet.cols_right_to_left = rdsheet.columns_from_right_to_left
        wtsheet.show_outline = rdsheet.show_outline_symbols
        wtsheet.remove_splits = rdsheet.remove_splits_if_pane_freeze_is_removed
        wtsheet.selected = rdsheet.sheet_selected
        # xlrd doesn't read WINDOW1 records, so we have to make a best
        # guess at which the active sheet should be:
        # (at a guess, only one sheet should be marked as visible)
        if not self.sheet_visible and rdsheet.sheet_visible:
            self.wtbook.active_sheet = self.wtsheet_index
            wtsheet.sheet_visible = 1
        self.wtsheet_index +=1
        
        wtsheet.page_preview = rdsheet.show_in_page_break_preview
        wtsheet.first_visible_row = rdsheet.first_visible_rowx
        wtsheet.first_visible_col = rdsheet.first_visible_colx
        wtsheet.grid_colour = rdsheet.gridline_colour_index
        wtsheet.preview_magn = rdsheet.cooked_page_break_preview_mag_factor
        wtsheet.normal_magn = rdsheet.cooked_normal_view_mag_factor
        #
        # DEFAULTROWHEIGHT
        #
        if rdsheet.default_row_height is not None:
            wtsheet.row_default_height =          rdsheet.default_row_height
        wtsheet.row_default_height_mismatch = rdsheet.default_row_height_mismatch
        wtsheet.row_default_hidden =          rdsheet.default_row_hidden
        wtsheet.row_default_space_above =     rdsheet.default_additional_space_above
        wtsheet.row_default_space_below =     rdsheet.default_additional_space_below
        #
        # BOUNDSHEET
        #
        wtsheet.visibility = rdsheet.visibility
       
        #
        # PANE
        #
        if rdsheet.has_pane_record:
            wtsheet.split_position_units_are_twips = True
            wtsheet.active_pane =              rdsheet.split_active_pane
            wtsheet.horz_split_pos =           rdsheet.horz_split_pos
            wtsheet.horz_split_first_visible = rdsheet.horz_split_first_visible
            wtsheet.vert_split_pos =           rdsheet.vert_split_pos
            wtsheet.vert_split_first_visible = rdsheet.vert_split_first_visible
            
    def set_rdsheet(self,rdsheet):
        """
        This should only ever called by a filter that
        wishes to change the source of cells mid-way through writing a
        sheet.

        :param rdsheet: the :class:`~xlrd.sheet.Sheet` object from which cells from
                  this point forward will be read.

        """
        self.rdsheet = rdsheet
        
    def row(self,rdrowx,wtrowx):
        """
        This should be called every time processing of a new
        row in the current sheet starts.

        :param rdrowx: the index of the row in the current sheet from which
                 information for the row to be written will be
                 copied.

        :param wtrowx: the index of the row in sheet to be written to which
                 information will be written for the row being read.
        """
        wtrow = self.wtsheet.row(wtrowx)
        # empty rows may not have a rowinfo record
        rdrow = self.rdsheet.rowinfo_map.get(rdrowx)
        if rdrow:
            wtrow.height = rdrow.height
            wtrow.has_default_height = rdrow.has_default_height
            wtrow.height_mismatch = rdrow.height_mismatch
            wtrow.level = rdrow.outline_level
            wtrow.collapse = rdrow.outline_group_starts_ends # No kiddin'
            wtrow.hidden = rdrow.hidden
            wtrow.space_above = rdrow.additional_space_above
            wtrow.space_below = rdrow.additional_space_below
            if rdrow.has_default_xf_index:
                wtrow.set_style(self.style_list[rdrow.xf_index])

    def cell(self,rdrowx,rdcolx,wtrowx,wtcolx):
        """
        This should be called for every cell in the sheet being processed.

        :param rdrowx: the index of the row to be read from in the current sheet. 
        :param rdcolx: the index of the column to be read from in the current sheet. 
        :param wtrowx: the index of the row to be written to in the current output sheet. 
        :param wtcolx: the index of the column to be written to in the current output sheet. 
        """
        cell = self.rdsheet.cell(rdrowx,rdcolx)
        # setup column attributes if not already set
        if wtcolx not in self.wtcols and rdcolx in self.rdsheet.colinfo_map:
            rdcol = self.rdsheet.colinfo_map[rdcolx]
            wtcol = self.wtsheet.col(wtcolx)
            wtcol.width = rdcol.width
            wtcol.set_style(self.style_list[rdcol.xf_index])
            wtcol.hidden = rdcol.hidden
            wtcol.level = rdcol.outline_level
            wtcol.collapsed = rdcol.collapsed
            self.wtcols.add(wtcolx)
        # copy cell
        cty = cell.ctype
        if cty == XL_CELL_EMPTY:
            return
        if cell.xf_index is not None:
            style = self.style_list[cell.xf_index]
        else:
            style = default_style
        rdcoords2d = (rdrowx, rdcolx)
        if rdcoords2d in self.merged_cell_top_left_map:
            # The cell is the governing cell of a group of 
            # merged cells.
            rlo, rhi, clo, chi = self.merged_cell_top_left_map[rdcoords2d]
            assert (rlo, clo) == rdcoords2d
            self.wtsheet.write_merge(
                wtrowx, wtrowx + rhi - rlo - 1,
                wtcolx, wtcolx + chi - clo - 1, 
                cell.value, style)
            return
        if rdcoords2d in self.merged_cell_already_set:
            # The cell is in a group of merged cells.
            # It has been handled by the write_merge() call above.
            # We avoid writing a record again because:
            # (1) It's a waste of CPU time and disk space.
            # (2) xlwt does not (as at 2007-01-12) ensure that only
            # the last record is written to the file.
            # (3) If you write a data record for a cell
            # followed by a blank record for the same cell,
            # Excel will display a blank but OOo Calc and
            # Gnumeric will display the data :-(
            return
        wtrow = self.wtsheet.row(wtrowx)
        if cty == XL_CELL_TEXT:
            wtrow.set_cell_text(wtcolx, cell.value, style)
        elif cty == XL_CELL_NUMBER or cty == XL_CELL_DATE:
            wtrow.set_cell_number(wtcolx, cell.value, style)
        elif cty == XL_CELL_BLANK:
            wtrow.set_cell_blank(wtcolx, style)
        elif cty == XL_CELL_BOOLEAN:
            wtrow.set_cell_boolean(wtcolx, cell.value, style)
        elif cty == XL_CELL_ERROR:
            wtrow.set_cell_error(wtcolx, cell.value, style)
        else:
            raise Exception(
                "Unknown xlrd cell type %r with value %r at (sheet=%r,rowx=%r,colx=%r)" \
                % (cty, cell.value, self.rdsheet.name, rdrowx, rdcolx)
                )

    def finish(self):
        """
        This method should be called once processing of all workbooks has
        been completed.
        """
        self.close()
        
  
class XLWTWriter(BaseWriter):
    "A writer that writes to a sequence of in-memory :class:`xlwt.Workbook` objects."

    def __init__(self):
        self.output = []

    def close(self):
        if self.wtbook is not None:
            self.output.append((self.wtname,self.wtbook))
            del self.wtbook


class BaseReader:
    "A base reader good for subclassing."

    def get_filepaths(self):
        """
        This is the most common method to implement. It must return an
        interable sequence of paths to excel files.
        """
        raise NotImplementedError

    def get_workbooks(self):
        """
        If the data to be processed is not stored in files or if
        special parameters need to be passed to :func:`xlrd.open_workbook`
        then this method must be overriden.
        Any implementation must return an iterable sequence of tuples.
        The first element of which must be an :class:`xlrd.Book` object and the
        second must be the filename of the file from which the book
        object came.
        """
        for path in self.get_filepaths():
            yield (
                open_workbook(
                    path,
                    formatting_info=1,
                    on_demand=True,
                    ragged_rows=True),
                os.path.split(path)[1]
                )

    def __call__(self, filter):
        """
        Once instantiated, a reader will be called and have the first
        filter in the chain passed to its :meth:`__call__` method.
        The implementation of this method
        should call the appropriate methods on the filter based on the
        cells found in the :class:`~xlrd.Book` objects returned from the
        :meth:`get_workbooks` method.
        """
        filter.start()
        for workbook,filename in self.get_workbooks():
            filter.workbook(workbook,filename)
            for sheet_x in range(workbook.nsheets):
                sheet = workbook.sheet_by_index(sheet_x)
                filter.sheet(sheet,sheet.name)
                for row_x in xrange(sheet.nrows):
                    filter.row(row_x,row_x)
                    for col_x in xrange(sheet.row_len(row_x)):
                        filter.cell(row_x,col_x,row_x,col_x)
                if workbook.on_demand:
                    workbook.unload_sheet(sheet_x)
        filter.finish()


class XLRDReader(BaseReader):
    "A reader that uses an in-memory :class:`xlrd.Book` object as its source of events."

    def __init__(self,wb,filename):
        self.wb = wb
        self.filename = filename
        
    def get_workbooks(self):
        "Yield the workbook passed during instantiation."
        yield (self.wb,self.filename)