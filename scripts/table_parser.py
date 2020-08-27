import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import camelot
import cv2

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
ptt_df[0] = ptt_df[0].str.strip()

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
filled_lines_mask = (ptt_df[0]
                     .apply(lambda s:
                            False if not s else s == len(s) * s[0]))
filled_lines_lens = ptt_df.loc[filled_lines_mask][0].str.len()
str_len_max = filled_lines_lens.max()

sep_idx = filled_lines_lens.index[filled_lines_lens > str_len_max * 0.9]

# table indicies
# get all rows starts with numbers, preserving original index
d_rows = (ptt_df[(ptt_df[0].str.contains(r"^\d")) & # starts with digit
                 ((ptt_df[0].str.len() -
                   ptt_df[0].str.count(" ")) /
                  str_len_max > 0.3)][0] # and filled for more than 30%
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

print(ptt_df.loc[tbl_hdr_idx])

# %%
class pdf_parser():

    def __init__(self,
                 doc_df=None,
                 drop_empty_rows=True,
                 file_path=None,
                 parse_method="pdftotext"
                 ):
        self.doc_df = doc_df
        self.drop_empty_rows=drop_empty_rows
        self.file_path = file_path
        self.parse_method = parse_method


    def get_rows(self, file_path):
        self.file_path = file_path
        if self.parse_method == "pdftotext":

            with open(self.file_path, "rb") as file:
                text_pages = pdftotext.PDF(file)

            parsed = ("\n\n".join(text_pages)
                      .splitlines())

            doc_df = pd.DataFrame(parsed)

            doc_df[0] = doc_df[0].str.strip()

            if self.drop_empty_rows:
                doc_df[0].replace("", np.nan, inplace=True)
                doc_df.dropna(inplace=True)

                (doc_df
                 .drop(doc_df[doc_df[0].str.len() == 1].index,
                       inplace=True))

                doc_df = doc_df.reset_index(drop=True)

        elif self.parse_method == "camelot":
            parsed = camelot.read_pdf(file_path,
                                      flavor="stream",
                                      split_text=True,
                                      suppress_stdout=True,
                                      pages="all")

            df_list = []

            for df in parsed:
                df_list.append(df.df)

            doc_df = pd.concat(df_list, ignore_index=True)

            if self.drop_empty_rows:
                (doc_df
                 .drop(doc_df[doc_df[0].str.len() == 1].index,
                       inplace=True))

                doc_df = doc_df.reset_index(drop=True)

        self.doc_df = doc_df
        return doc_df

# %%

my_parser = pdf_parser(parse_method="camelot")
f = my_parser.get_rows(file_path=NEW_PDF)
g = my_parser.get_rows(file_path=NEW_PDF)

my_parser.file_path
my_parser.doc_df

# %%
image = cv2.imread('scripts/notebooks/gfs_5760519_page_1_resized.png')
position = (5, 10)
font_scale = 0.3
color = (255, 0, 0)
thickness = 1
font = cv2.FONT_HERSHEY_PLAIN
line_type = cv2.LINE_AA

text_size = cv2.getTextSize(splitted[0], font, font_scale, thickness)[0]
line_height = text_size[1] + 3
x, y0 = position
for i in range(len(splitted[:50])):
    line = "l1"
    y = y0 + i * line_height
    cv2.putText(image,
                line,
                (x, y),
                font,
                font_scale,
                color,
                thickness,
                line_type)
plt.imshow(image)
# cv2.imshow("Result Image", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# %%
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
