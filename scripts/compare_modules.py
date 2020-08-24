from py4j.java_gateway import JavaGateway

import tabula
import camelot
import pdftotext

# %%
PDF_1 = "task_description/examples/GFS 5760519.pdf"
PDF_2 = "task_description/examples/sysco PO#_077-2706434.pdf"

# %%
# tabula-py 1.4.1
df_1 = tabula.read_pdf(PDF_1, stream=True, pages="all")
df_1.head()

# %%
df_2 = tabula.read_pdf(PDF_2, stream=True, pages="all")
df_2.head()

# %%
# camelot-py 0.8.2
tables_1 = camelot.read_pdf(PDF_1,
                            flavor="stream",
                            split_text=True,
                            suppress_stdout=True,
                            pages="all")
print(tables_1[0].df.head(25))

# %%
tables_2 = camelot.read_pdf(PDF_2,
                            flavor="stream",
                            split_text=True,
                            suppress_stdout=True,
                            pages="all")
print(tables_2[0].df.head(25))

# %%
# PDFLayoutTextStripper 2.2.3
# https://stackoverflow.com/questions/51334387/unable-to-launch-gateway-from-python-in-py4j
# https://stackoverflow.com/questions/42826221/py4j-how-to-launch-the-java-gateway-from-python
# https://www.py4j.org/py4j_java_gateway.html#examples

gg = (JavaGateway
      .launch_gateway(
          classpath="pdf_layout_text_stripper/python-gateway.jar",
          die_on_exit=True))

pdf_stripper = gg.jvm.io.github.jonathanlink.PythonGateway()

# %%
res_1 = pdf_stripper.strip(PDF_1)
str_1 = res_1["payload"].splitlines()
for i in range(30):
    print(str_1[i])

# %%
res_2 = pdf_stripper.strip(PDF_2)
print(res_2)

# %%
gg.close()

# %%
# pdftotext 2.1.5
# https://stackoverflow.com/questions/14372706/visual-studio-cant-build-due-to-rc-exe
with open(PDF_1, "rb") as f1:
    pdf_1 = pdftotext.PDF(f1)

txt_1 = ("\n\n".join(pdf_1) # append all pages
         .splitlines())

for i in range(35):
    print(txt_1[i])

# %%
with open(PDF_2, "rb") as f2:
    pdf_2 = pdftotext.PDF(f2)

txt_2 = ("\n\n".join(pdf_2)
         .splitlines())

for i in range(25):
    print(txt_2[i])
