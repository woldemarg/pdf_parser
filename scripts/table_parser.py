import re
import pandas as pd
import numpy as np
from scripts.pdf_parser_class import PDFparser

# %%
# PDF = "task_description/examples/Sysco PO#_338-4243823.pdf"
PDF = "task_description/examples/GFS 5760519.pdf"

# %%
my_parser = PDFparser(parse_method="camelot")
df = my_parser.get_rows_marked(PDF)

# %%
row = (df
       .loc[df["mark"] == "tbl_row", 0]
       .reset_index(drop=True)[7])

# %%
tokens = re.findall(r"\s+", row)

ws = []
for i, t in enumerate(tokens):
    ws.append(len(t))
ws.insert(0, 0)
ws.append(0)

# %%
row_spl = re.split(r"\s+", row)

ROW_DEM = ""
for i, w in enumerate(row_spl):
    ROW_DEM += " (" + str(ws[i]) + ") " + w
ROW_DEM += " (" + str(ws[-1]) + ") "

# %%
def split_to_cols(row_org):
    tkns = re.findall(r"\s+", row_org)

    whsp = [] # num of spaces between words in a row
    for i, t in enumerate(tkns):
        whsp.append(len(t))
    whsp.insert(0, 0)
    whsp.append(0)

    row_spl = re.split(r"\s+", row_org)

    cols = []
    cols.append(row_spl[0])

    i = 1
    while i < len(row_spl[:-1]):
        el = row_spl[i]
        if whsp[i + 1] != 1:
            i += 1
        else:
            j = 1
            while whsp[i + j] == 1:
                el += " " + row_spl[i + j]
                j += 1
            i = i + j
        cols.append(el.strip())
    cols.append(row_spl[-1])

    return cols

# %%
str_series = (df
              .loc[df["mark"] == "tbl_row", 0]
              .reset_index(drop=True))

tbl_rows = str_series.loc[range(0, len(str_series), 2)]


splitted_rows = []
for row in tbl_rows:
    splitted_rows.append(split_to_cols(row))

rows_len = list(map(len, splitted_rows))
len_mode = max(rows_len, key=rows_len.count)

for i, row in enumerate(splitted_rows):
    if len(row) != len_mode:
        splitted_rows[i] = [np.nan] * len_mode

init_df = pd.DataFrame(splitted_rows)

i, offset = 0, 0
while i < init_df.shape[1] + offset:
    splt_cols = (init_df[i].str.split(expand=True)
                 .fillna(""))
    if splt_cols.shape[1] != 1:
        is_digit = (splt_cols
                   .apply(lambda col:
                          all(str(elem).isdigit() for elem in col),
                          axis=0))

        redist_series = []

        idx = 0
        while idx < len(is_digit):
            cur_col = splt_cols[idx].copy()
            if is_digit[idx]:
                idx += 1
            else:
                j = 1
                while idx + j < len(is_digit):
                    if ~is_digit[idx + j]:
                        cur_col += " " + splt_cols[idx + j]
                        j += 1
                idx = idx + j
            redist_series.append(cur_col.str.strip())

        redist_cols = pd.DataFrame(redist_series).transpose()

        init_df = pd.concat([init_df.iloc[:, :i],
                             redist_cols,
                             init_df.iloc[:, i + 1:]],
                            axis=1)
        init_df.columns = range(init_df.shape[1])
        offset += redist_cols.shape[1]
    i += 1 + offset


~digit_types[1]
False and True
# %%
def reassign_cols(cols):

cols = (init_df[2].str.split(expand=True)
                 .fillna(""))

is_digit = (cols
            .apply(lambda col:
                   all(str(elem).isdigit() for elem in col),
                   axis=0))

rsnd_series = []

idx = 0
while idx < len(is_digit):
    cur_col = cols[idx].copy()
    if is_digit[idx]:
        # rsnd_series.append(cur_col.str.strip())
        idx += 1
    else:
        j = 1
        while idx + j < len(is_digit):
            if ~is_digit[idx + j]:
                cur_col += " " + cols[idx + j]
                j += 1
            else:
                # rsnd_series.append(cur_col.str.strip())
                break
        idx += j
        # if idx + j > 6:
    rsnd_series.append(cur_col.str.strip())
# if idx == len(is_digit):
    # rsnd_series.append(cur_col.str.strip())
        #     while ~is_digit[idx + j]:
        #         cur_col += " " + cols[idx + j]
        #         if idx + j >= len(is_digit) - 1:
        #             rsnd_series.append(cur_col.str.strip())
        #             break
        #         j += 1
        #     # idx += j
        #     # rsnd_series.append(cur_col.str.strip())
        # idx += j



    return pd.DataFrame(rsnd_series).transpose()

# %%

splt_cols = (init_df[2].str.split(expand=True)
                 .fillna(""))

g = reassign_cols(splt_cols)
