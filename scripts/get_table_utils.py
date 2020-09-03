import re
import numpy as np
import pandas as pd

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
def readjust_cols(original_col):
    splitted_cols = (original_col.str.split(expand=True)
                     .fillna(""))

    if splitted_cols.shape[1] == 1:
        return pd.DataFrame(original_col)

    is_digit = (splitted_cols
                .apply(lambda col:
                       all(str(elem).isdigit() for elem in col),
                       axis=0))

    rsnd_series = []

    idx = 0
    while idx < len(is_digit):
        cur_col = splitted_cols[idx]
        if is_digit[idx]:
            idx += 1
        else:
            j = 1
            while idx + j < len(is_digit):
                if ~is_digit[idx + j]:
                    cur_col += " " + splitted_cols[idx + j]
                    j += 1
                else:
                    break
            idx += j
        rsnd_series.append(cur_col.str.strip())
    rsnd_cols = pd.DataFrame(rsnd_series).transpose()

    return rsnd_cols

# %%
def get_table(tbl_rows):
    splitted_rows = []
    for rw in tbl_rows:
        rw = rw.replace("|", "")
        splitted_rows.append(split_to_cols(rw))

    rows_len = list(map(len, splitted_rows))
    len_mode = max(rows_len, key=rows_len.count)

    for i, rw in enumerate(splitted_rows):
        if len(rw) != len_mode:
            splitted_rows[i] = [np.nan] * len_mode

    init_df = pd.DataFrame(splitted_rows)

    i, offset = 0, 0
    while i < init_df.shape[1]:
        new_cols = readjust_cols(init_df[i])
        init_df = pd.concat([init_df.iloc[:, :i],
                             new_cols,
                             init_df.iloc[:, i + 1:]],
                            axis=1)
        init_df.columns = range(init_df.shape[1])
        offset = new_cols.shape[1] - 1
        i += 1 + offset

    return init_df
