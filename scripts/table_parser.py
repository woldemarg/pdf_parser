import pdftotext
import camelot
import pandas as pd
import numpy as np

# %%
NEW_PDF = "task_description/examples/sysco PO#_077-2706434.pdf"

# %%
with open(NEW_PDF, "rb") as file:
    text_pages = pdftotext.PDF(file)

# %%
doc = ("\n\n".join(text_pages)
       .splitlines())

doc_df[0].replace("", np.nan, inplace=True)
doc_df.dropna(inplace=True)
doc_df[0] = doc_df[0].str.strip()

# %%
import camelot

# %%
parsed = camelot.read_pdf(NEW_PDF,
                            flavor="stream",
                            split_text=True,
                            suppress_stdout=True,
                            pages="all")

d_list = []

for d in parsed._tables:
    d_list.append(d.df)

all_df = pd.concat(d_list,ignore_index=True)

