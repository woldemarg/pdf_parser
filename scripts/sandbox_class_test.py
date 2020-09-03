import re
import pandas as pd
import numpy as np
import camelot
import tabula
from fpdf import FPDF
from scripts.pdf_parser_class import PDFparser

# %%
PDF_1 = "task_description/examples/Sysco PO#_338-4243823.pdf"
PDF_2 = "task_description/examples/GFS 5760519.pdf"

# %%
my_parser = PDFparser()

# %%
df_1 = my_parser.get_rows_marked(PDF_1)
df_2 = my_parser.get_rows_marked(PDF_2)
