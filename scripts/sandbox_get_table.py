import re
import pandas as pd
import numpy as np
import camelot
import tabula
from fpdf import FPDF
from scripts.pdf_parser_class import PDFparser

# %%
# PDF = "task_description/examples/Sysco PO#_338-4243823.pdf"
PDF = "task_description/examples/GFS 5760519.pdf"

# %%
my_parser = PDFparser()
df = my_parser.get_rows_marked(PDF)

# %%
row = (df
       .loc[df["mark"] == "tbl_row", 0]
       .reset_index(drop=True)[7])

# %%
tokens = re.findall(r"\s+", row)

ws = []
for g, tk in enumerate(tokens):
    ws.append(len(tk))
ws.insert(0, 0)
ws.append(0)

# %%
row_splitted = re.split(r"\s+", row)

ROW_DEM = ""
for h, w in enumerate(row_splitted):
    ROW_DEM += " (" + str(ws[h]) + ") " + w
ROW_DEM += " (" + str(ws[-1]) + ") "

# %%
def split_to_cols(row_org):
    row_org = row_org.strip()

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

    init_df = pd.DataFrame(splitted_rows,
                           index=tbl_rows.index)

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

# %%
str_series = df.loc[df["mark"] == "tbl_row", 0]

uneven_rows = str_series.iloc[::2]

uneven_df = get_table(uneven_rows)

# %%
# pdf = FPDF()
# pdf.add_page(orientation="L")
# pdf.set_font("Courier", size = 8)
# for k, st in enumerate(str_series):
#     pdf.cell(w=0,
#              h=5,
#              border=0,
#              align="L",
#              ln=1,
#              txt=st)
# pdf.output("mygfg.pdf")

# %%
# df_1 = tabula.read_pdf("mygfg.pdf", stream=True, pages="all")
# df_1.head()

# %%
# tables_1 = camelot.read_pdf("mygfg.pdf",
#                             flavor="stream",
#                             split_text=True,
#                             suppress_stdout=True,
#                             pages="all")
# print(tables_1[0].df.head(25))

# %%
row = (df
       .loc[df["mark"] == "tbl_row", 0]
       .reset_index(drop=True))

splitted_rows = []
for rw in uneven_rows:
    rw = rw.replace("|", "")
    splitted_rows.append(split_to_cols(rw))

# h = row[7]
# h2 = split_to_cols2(row_mod)

# %%
def split_to_cols2(row_org):
    row_org = row_org.strip()
    tkns = re.findall(r"\s+", row_org)

    whsp = [] # num of spaces between words in a row
    for i, t in enumerate(tkns):
        whsp.append(len(t))
    whsp.insert(0, 0)
    whsp.append(0)

    row_mod = re.sub(r"(^[0-9]+)(\s{1})", r"\1  ", row_org)
    row_spl = re.split(r"\s+", row_mod)


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
for w in splitted_rows[0]:
    print ("{} starts at {}".format(w, row[0].find(w)))

row[1].find("182050")
