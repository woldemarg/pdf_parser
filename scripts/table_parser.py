import pandas as pd
import numpy as np

import camelot
import pdftotext

# import re

# %%
# NEW_PDF = "task_description/examples/GFS 5760519.pdf"
NEW_PDF = "task_description/examples/sysco PO#_077-2706434.pdf"

# %%
with open(NEW_PDF, "rb") as file:
    text_pages = pdftotext.PDF(file)

splitted = ("\n\n".join(text_pages)
            .splitlines())

ptt_df = pd.DataFrame(splitted)
ptt_df[0].replace("", np.nan, inplace=True)
ptt_df = (ptt_df
          .dropna()
          .reset_index(drop=True))

ptt_df[0] = ptt_df[0].str.strip()

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

# %%
print(ptt_df.equals(cam_df))

# %%
unequal_mask = (ptt_df[0] != cam_df[0])

compare_df = pd.concat([ptt_df[unequal_mask],
                        cam_df[unequal_mask]],
                       axis=1)

compare_df.columns = ["ptt", "cam"]

# %%
print(compare_df.loc[22, "ptt"])
print(compare_df.loc[22, "cam"])

# %%
is_separator_mask = ptt_df[0].apply(lambda s: s == len(s) * s[0])
max_str_length = ptt_df.loc[is_separator_mask, 0].str.len().max()

# get all rows starts with numbers, preserving original index
d_rows = (ptt_df[(ptt_df[0].str.contains(r"^\d")) & # starts with digit
                 ((ptt_df[0].str.len() -
                   ptt_df[0].str.count(" ")) /
                  max_str_length > 0.3)][0] # and filled for more than 30%
          .str.extract(pat=r"^(\d+)\s*\D") # get number from str beginning
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

tbl_last_row_idx = d_rows.index[one_idx + CNT]

g = ptt_df.iloc[tbl_frst_row_idx:tbl_last_row_idx + 1]



# f_elem = d_rows[0].str[0]
# d = d_rows.diff()
# start_idx = d[(d != 1) & (~d.isna())].idxmin()
# d_rows[start_idx]
# for i in range(d.index.get_loc(start_idx) + 1, len(d)):
#     if d.iloc[i] =! 1:
#         start_ind =
#         end_idx = d.index[i]
#     end_idx = d.index[len(d) - 1]


# d[d == d.iloc[1].index
# d.index.get_loc(22)
# start_idx = digit_rows.index[i + 1]
#     end_idx = digit_rows.index[i]

# digit_rows.iloc[1, 0][0]

# s = compare_df.iloc[1, 0]

# tokens = re.findall('\s+', s)

# for i in range(0, len(tokens)):
#     print(len(tokens[i]))

# d.iloc[0]
# # %%
# s = compare_df.iloc[1, 1]

# tokens = re.findall('\s+', s)

# for i in range(0, len(tokens)):
#     print(len(tokens[i]))

# # compare_df.loc[22, "cam"]
# # s
# len(tokens[1])

# ptt_df[ptt_df[0].str.startswith("1")]
