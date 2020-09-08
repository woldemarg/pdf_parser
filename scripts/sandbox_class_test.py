from scripts.v_01.pdf_parser_class import PDFparser

# %%
PDF_1 = "task_description/examples/Sysco PO#_338-4243823.pdf"
PDF_2 = "task_description/examples/GFS 5760519.pdf"

# %%
my_parser = PDFparser()

# %%
df_1 = my_parser.get_rows_marked(PDF_1)
df_2 = my_parser.get_rows_marked(PDF_2)

# %%
print(df_1.equals(df_2))