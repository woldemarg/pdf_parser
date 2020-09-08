from io import StringIO

import pandas as pd
import numpy as np

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# %%
class PDFparser():

    def __init__(self,
                 sep_min_width=0.5,
                 tbl_row_min_fill=0.5
                 ):
        self.doc_df = None
        self.doc_df_m = None
        self.file_path = None
        self.sep_idx = None
        self.sep_min_width = sep_min_width
        self.str_len_max = None
        self.tbl_hdr_idx = None
        self.tbl_idx = None
        self.tbl_row_min_fill = tbl_row_min_fill

    def get_rows(self, file_path):
        output_string = StringIO()

        with open(file_path, "rb") as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr,
                                   output_string,
                                   laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        doc_df = pd.DataFrame(output_string.getvalue()
                              .splitlines())

        doc_df[0].replace("", np.nan, inplace=True)
        doc_df.dropna(inplace=True)

        (doc_df
         .drop(doc_df[doc_df[0].str.len() == 1].index,
               inplace=True))

        doc_df = doc_df.reset_index(drop=True)

        self.file_path = file_path
        self.doc_df = doc_df
        return doc_df

    def __get_sep_idx(self):
        filled_lines_mask = (self.doc_df[0]
                             .apply(lambda s:
                                    False if not s else s == len(s) * s[0]))
        filled_lines_lens = self.doc_df.loc[filled_lines_mask][0].str.len()

        str_len_max = self.doc_df[0].str.len().max()

        sep_idx = (filled_lines_lens
                   .index[filled_lines_lens >= str_len_max *
                          self.sep_min_width])

        self.sep_idx = sep_idx
        self.str_len_max = str_len_max
        return sep_idx

    def __get_tbl_idx(self):
        d_rows = (self.doc_df[(self.doc_df[0].str.contains(r"^\s*\d+\s+")) &
                              ((self.doc_df[0].str.len() -
                                self.doc_df[0].str.count(" ")) /
                               self.doc_df[0].str.len().mean() >=
                               self.tbl_row_min_fill)][0]
                  .str.extract(pat=r"^\s*(\d+)\s*\D")
                  .astype(np.int64))[0]

        tbl_frst_row_idx = d_rows.index[0]
        tbl_last_row_idx = d_rows.index[-1]

        tbl_idx_ext = (self.doc_df
                       .index[tbl_frst_row_idx:tbl_last_row_idx + 1])

        if tbl_idx_ext[1] not in d_rows.index:
            tbl_idx_ext = (self.doc_df
                           .index[tbl_frst_row_idx:tbl_last_row_idx + 2])

        tbl_lines = (self.doc_df.loc[tbl_idx_ext][0]
                     .str.replace(" ", "")
                     .str[:-1])

        top_lines = (self.doc_df.loc[:tbl_frst_row_idx - 1][0]
                     .str.replace(" ", "")
                     .str[:-1])

        tbl_idx_cln = tbl_lines.index[~tbl_lines.isin(top_lines)]

        self.tbl_idx = tbl_idx_cln
        return tbl_idx_cln

    def __get_tbl_hdr_idx(self):
        ln_above_tbl_idx = self.tbl_idx[0] - 1

        if ln_above_tbl_idx in self.sep_idx:
            prev_sep_idx = self.sep_idx[self.sep_idx
                                        .get_loc(ln_above_tbl_idx) - 1]
            tbl_hdr_last_idx = ln_above_tbl_idx
        else:
            prev_sep_idx = self.sep_idx[self.sep_idx < ln_above_tbl_idx][0]
            tbl_hdr_last_idx = ln_above_tbl_idx + 1

        tbl_hdr_frst_idx = prev_sep_idx + 1

        tbl_hdr_idx = self.doc_df.index[tbl_hdr_frst_idx:tbl_hdr_last_idx]

        self.tbl_hdr_idx = tbl_hdr_idx
        return tbl_hdr_idx

    def get_rows_marked(self, file_path):
        doc_df_m = self.get_rows(file_path).copy()
        doc_df_m["mark"] = np.nan

        self.__get_sep_idx()

        tbl_idx = self.__get_tbl_idx()
        doc_df_m.loc[tbl_idx, "mark"] = "tbl_row"

        tbl_hdr_idx = self.__get_tbl_hdr_idx()
        doc_df_m.loc[tbl_hdr_idx, "mark"] = "tbl_hdr"

        doc_df_m["mark"].fillna("doc_txt", inplace=True)

        self.doc_df_m = doc_df_m
        return doc_df_m
