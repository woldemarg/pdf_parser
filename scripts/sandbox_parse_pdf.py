import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import camelot
import cv2

import pdftotext
# import re

# %%
NEW_PDF = "task_description/examples/GFS 5760519.pdf"
# NEW_PDF = "task_description/examples/sysco PO#_077-2706434.pdf"
# NEW_PDF = "task_description/examples/Sysco PO#_338-4243823.pdf"
# NEW_PDF = "task_description/examples/GFS PO3430811.pdf"

# %%
with open(NEW_PDF, "rb") as file:
    text_pages = pdftotext.PDF(file)

splitted = ("\n\n".join(text_pages)
            .splitlines())

ptt_df = pd.DataFrame(splitted)
# ptt_df[0] = ptt_df[0].str.strip()

ptt_df[0].replace("", np.nan, inplace=True)
ptt_df.dropna(inplace=True)
(ptt_df
  .drop(ptt_df[ptt_df[0].str.len() == 1].index,
        inplace=True))
ptt_df = ptt_df.reset_index(drop=True)

# %%
parsed = camelot.read_pdf(NEW_PDF,
                          flavor="stream",
                          split_text=True,
                          suppress_stdout=True,
                          pages="all")

df_list = []

for df in parsed:
    df_list.append(df.df)

cam_df = pd.concat(df_list, ignore_index=True)

cam_df.drop(cam_df[cam_df[0].str.len() == 1].index, inplace=True)
cam_df = cam_df.reset_index(drop=True)

# %%
# print(ptt_df.equals(cam_df))

# %%
# unequal_mask = (ptt_df[0] != cam_df[0])

# compare_df = pd.concat([ptt_df[unequal_mask],
#                         cam_df[unequal_mask]],
#                        axis=1)

# compare_df.columns = ["ptt", "cam"]

# %%
# print(compare_df.loc[22, "ptt"])
# print(compare_df.loc[22, "cam"])

# %%
# separators
# ptt_df = cam_df
filled_lines_mask = (ptt_df[0]
                     .apply(lambda s:
                            False if not s else s == len(s) * s[0]))
filled_lines_lens = ptt_df.loc[filled_lines_mask][0].str.len()
# str_len_max = filled_lines_lens.max()
str_len_max = ptt_df[0].str.len().max()

sep_idx = filled_lines_lens.index[filled_lines_lens >= str_len_max * 0.5]

# table indicies
# get all rows starts with numbers, preserving original index
d_rows = (ptt_df[(ptt_df[0].str.contains(r"^\s*\d+\s+")) & # starts with digit
                 ((ptt_df[0].str.len() -
                   ptt_df[0].str.count(" ")) /
                  ptt_df[0].str.len().mean() >= 0.5)][0] # and filled for more than 30%
          .str.extract(pat=r"^\s*(\d+)\s*\D") # get number from str beginning
          .astype(np.int64))[0]

tbl_frst_row_idx = d_rows[d_rows == 1].index.min()

# relative index of row stars with 1 in series above
one_idx = (d_rows
           .index
           .get_loc(tbl_frst_row_idx))

# get sequence of numbers, each next bigger than previous by 1
CNT = 1
while ((d_rows.iloc[one_idx + CNT] -
        d_rows.iloc[one_idx + CNT - 1] == 1) and
       (one_idx + CNT <= len(d_rows) - 2)):
    CNT += 1

tbl_last_row_idx = d_rows.index[CNT]
tbl_idx_ext = ptt_df.index[tbl_frst_row_idx : tbl_last_row_idx + 1]

# in-between table rows there could be some data
if tbl_idx_ext[1] not in d_rows.index:
    tbl_idx_ext = ptt_df.index[tbl_frst_row_idx : tbl_last_row_idx + 2]

# drop header lines
tbl_lines = (ptt_df.loc[tbl_idx_ext][0]
             .str.replace(" ", "")
             .str[:-1]) # to match PAGE-1 with PAGE-2

top_lines = (ptt_df.loc[:tbl_frst_row_idx - 1][0]
             .str.replace(" ", "")
             .str[:-1])

tbl_idx_cln = tbl_lines.index[~tbl_lines.isin(top_lines)]

# table headers
ln_above_tbl_idx = tbl_idx_cln[0] - 1

if ln_above_tbl_idx in sep_idx:
    prev_sep_idx = sep_idx[sep_idx.get_loc(ln_above_tbl_idx) - 1]
    tbl_hdr_last_idx = ln_above_tbl_idx
else:
    prev_sep_idx = sep_idx[sep_idx < ln_above_tbl_idx][0]
    tbl_hdr_last_idx = ln_above_tbl_idx + 1

tbl_hdr_frst_idx = prev_sep_idx + 1
tbl_hdr_idx = ptt_df.index[tbl_hdr_frst_idx : tbl_hdr_last_idx]

ptt_df["marks"] = np.nan
ptt_df.loc[sep_idx, "marks"] = "separator"
ptt_df.loc[tbl_idx_cln, "marks"] = "table_row"
ptt_df.loc[tbl_hdr_idx, "marks"] = "table_header"

# %%
str_series = ptt_df.loc[ptt_df["marks"] == "table_row", 0]

uneven_rows = str_series.iloc[::2]
even_rows = str_series.iloc[1::2]

uneven_df = get_table(uneven_rows)

# %%

def get_cell_text_start_positions(row_orig, row_cell):
    pos_list = []
    start_pos = 0
    for i, cell_text in enumerate(row_cell):
        row_orig_cutted = row_orig[start_pos:]
        cur_pos = row_orig_cutted.find(cell_text)
        pos_list.append(cur_pos + start_pos)
        start_pos += cur_pos + len(cell_text)
    return pos_list



pos = []
for i in range(len(uneven_rows)):
    pos.append(get_cell_text_start_positions(uneven_rows.iloc[i],
                                              uneven_df.iloc[i]))

    # pos_in_row = []
    # start_pos = 0
    # for j in range(uneven_df.shape[1]):
    #     cell = uneven_df.loc[i, j]
    #     str_to_seek_in = uneven_rows.iloc[i][start_pos:]
    #     cur_pos = str_to_seek_in.find(cell)
    #     pos_in_row.append(cur_pos + start_pos)
    #     start_pos += cur_pos + len(cell)
    pos.append(pos_in_row)

def rename_elements_in_list(ls_in):
    ls_out = []
    i = 0
    while i < len(ls_in) - 1:
        if ls_in[i] != ls_in[i + 1]:
            ls_out.append(str(ls_in[i]))
            i += 1
        j = 1
        while i + j < len(ls_in):
            if ls_in[i] == ls_in[i + j]:
                ls_out.append("{}_{}".format(ls_in[i - 1], j))
                j += 1
            else:
                ls_out.append(str(ls_in[j]))
                break
        i += j
    ls_out.append(str(ls_in[-1]))

    return ls_out






# r = even_rows.iloc[9]
even_ls = []
for i, r in enumerate(even_rows):
    row_mod = r.replace("|", " ").strip()
    # row_spl = re.split(r"\s+", row_mod)
    row_spl = row_mod.split()
    w_pos = get_cell_text_start_positions(r, row_spl)
    df_pos = np.searchsorted(pos[i], w_pos)
    df_pos = rename_elements_in_list(df_pos)

    s = pd.DataFrame(data=dict(zip(df_pos, row_spl)),
                     index=[uneven_rows.index[i]])
    even_ls.append(s)


# g = pd.concat(even_ls, axis=1, verify_integrity=True)
g3 = pd.concat(even_ls, sort=True) #, ignore_index=False, sort=False)
# g2 = pd.append(even_ls)
# , axis=1, verify_integrity=True)
g4 = pd.concat([uneven_df, g3], axis=1, sort=True)
g4 = g4.reindex(sorted(g4.columns.astype("str")), axis=1)
g4.columns = g4.columns.astype("str")
g5 = g4.sort_index(axis=1)
even_rows.index[0]
len(uneven_rows.iloc[0])


    print ("{} starts at {}".format(w, row[0].find(w)))

list(enumerate(uneven_df.loc[0]))

np.searchsorted([1,2,3,4,5], [2, 2], side="right")
sorted(g4.columns.astype("str"))
