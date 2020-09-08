import numpy as np
import pandas as pd

from itertools import chain, combinations

from scripts.v_02.pdf_parser_class import PDFparser
import scripts.v_02.get_table_utils as tbu

# %%
PDF = "task_description/examples/GFS 5760519.pdf"

# %%
my_parser = PDFparser()
df = my_parser.get_rows_marked(PDF)

# %%
table_strings = df.loc[df["mark"] == "tbl_row", 0]

odd_strings = table_strings.iloc[::2]
evn_strings = table_strings.iloc[1::2] # "висячие" строки

odd_df = tbu.get_table(odd_strings)

# %%
def get_cell_text_start_positions(row_orig, row_cell):
    pos_list = []
    start_pos = 0
    for cell_text in row_cell:
        row_orig_cutted = row_orig[start_pos:]
        cur_pos = row_orig_cutted.find(cell_text)
        pos_list.append(cur_pos + start_pos)
        start_pos += cur_pos + len(cell_text)
    return pos_list

# %%
cell_text_positions = []
for g, odd_s in enumerate(odd_strings):
    (cell_text_positions
    .append(get_cell_text_start_positions(odd_s,
                                          odd_df.iloc[g])))

# %%
def add_postfix(in_list):
    out_list = []
    i = 0
    while i < len(in_list) - 1:
        if in_list[i] != in_list[i + 1]:
            out_list.append(str(in_list[i]))
            i += 1
        j = 1
        while i + j < len(in_list):
            if in_list[i] == in_list[i + j]:
                out_list.append("{}_{}".format(in_list[i - 1], j))
                j += 1
            else:
                out_list.append(str(in_list[j]))
                break
        i += j
    out_list.append(str(in_list[-1]))
    return out_list

# %%
evn_cells_positions = []
for k, r in enumerate(evn_strings):
    row_mod = r.replace("|", " ").strip()
    row_spl = row_mod.split()
    text_pos = get_cell_text_start_positions(r, row_spl)
    col_idx = np.searchsorted(cell_text_positions[k], text_pos)
    col_idx_renamed = add_postfix(col_idx)

    one_row_df = pd.DataFrame(data=dict(zip(col_idx_renamed, row_spl)),
                     index=[odd_strings.index[k]])
    evn_cells_positions.append(one_row_df)

evn_df = pd.concat(evn_cells_positions)

# %%
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

combos = []
for t in powerset(evn_df.columns):
    if len(t) > 1 and all(elem[0] == t[0][0] for elem in t):
        combos.append(list(t))

for combo in combos:
    evn_df[combo[0]] = evn_df[combo[0]].str.cat(evn_df[combo[1:]], sep=" ")
    evn_df.drop(combo[1:],
                axis=1,
                inplace=True)

# %%
full_table = pd.concat([odd_df, evn_df], axis=1, sort=True)

full_table.columns = full_table.columns.astype(str)
full_table.sort_index(axis=1, inplace=True)
full_table.columns = list(range(full_table.shape[1]))

full_table = full_table.reset_index(drop=True)

