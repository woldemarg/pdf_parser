import pandas as pd
import numpy as np

import camelot
import pdftotext
# import re

# %%
NEW_PDF = "task_description/examples/GFS 5760519.pdf"
# NEW_PDF = "task_description/examples/sysco PO#_077-2706434.pdf"

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

ptt_df.drop(ptt_df[ptt_df[0].str.len() == 1].index, inplace=True)

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
filled_lines_mask = ptt_df[0].apply(lambda s: s == len(s) * s[0])
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
    tbl_hdr_last_idx = ln_above_tbl_idx - 1

tbl_hdr_frst_idx = prev_sep_idx + 1
tbl_hdr_idx = ptt_df.index[tbl_hdr_frst_idx : tbl_hdr_last_idx]

print(ptt_df.loc[tbl_hdr_idx])

# %%
# import cv2
# import matplotlib.pyplot as plt
# image = cv2.imread('scripts/notebooks/gfs_5760519_page_1.png')
# texted_image =cv2.putText(img=np.copy(image), text=["hello\n", "world"], org=(25,25),fontFace=1, fontScale=1, color=(0,0,255), thickness=5)
# plt.imshow(texted_image)
# plt.show()

# img = np.zeros((500,500,3), dtype='uint8')
# print(img.shape)

# position = (500, 100)
# font_scale = 0.75
# color = (255, 255, 255)
# thickness = 3
# font = cv2.FONT_HERSHEY_SIMPLEX
# line_type = cv2.LINE_AA

# text_size = cv2.getTextSize(splitted[0], font, font_scale, thickness)[0]

# line_height = text_size[1] + 3

# x, y0 = position
# for i in range(len(splitted)):
#     line = splitted[i].rstrip()
#     cv2.putText(image,
#                 line,
#                 (x, y),
#                 font,
#                 font_scale,
#                 color,
#                 thickness,
#                 line_type)


# cv2.imshow("Result Image", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# # %%
# import numpy as np
# import cv2
# import textwrap

# img = np.zeros((500,500,3), dtype='uint8')
# print(img.shape)

# height, width, channel = img.shape

# text_img = np.ones((height, width))
# print(text_img.shape)
# font = cv2.FONT_HERSHEY_SIMPLEX

# text = "type: car, color: white, number: 123456"
# #to automatically wrap text => wrapped_text = textwrap.wrap(text, width=10)
# wrapped_text = ['Type: car','Color: white','Number: 123456']
# x, y = 10, 40
# font_size = 0.5
# font_thickness = 1

# i = 0
# for line in wrapped_text:
#     textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]

#     gap = textsize[1] + 5

#     y = int((img.shape[0] + textsize[1]) / 2) + i * gap
#     x = 10#for center alignment => int((img.shape[1] - textsize[0]) / 2)

#     cv2.putText(image, line, (x, y), font,
#                 font_size,
#                 (255,255,255),
#                 font_thickness,
#                 lineType = cv2.LINE_AA)
#     i +=1

# cv2.imshow("Result Image", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

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
