import numpy as np
import cv2
from scripts.pdf_parser_class import PDFparser
from pathlib import Path

# %%
pdf_pths = [str(pth) for pth
            in Path("task_description/examples/").iterdir()
            if pth.suffix == ".pdf"]

# %%
my_parser = PDFparser(parse_method="camelot")
df_marked_2 = my_parser.get_rows_marked(pdf_pths[0])

# %%
longest_str = df_marked.loc[df_marked[0].str.len().idxmax()][0]
mrgn = 50
font_scale = .35
color = (255, 255, 255)
thickness = 1
font = cv2.FONT_HERSHEY_SIMPLEX
line_type = cv2.LINE_AA

(w, h), baseline = cv2.getTextSize(longest_str,
                                   font,
                                   font_scale,
                                   thickness)

line_height = h + baseline

image = np.zeros((len(df_marked) * line_height + mrgn * 2,
                  w + mrgn * 2,
                  3), dtype="uint8")

x, y0 = (int(mrgn/2), mrgn)
for i in range(len(df_marked)):
    line = df_marked.loc[i, "mark"] + "    " + df_marked.loc[i, 0]
    y = y0 + i * line_height
    cv2.putText(image,
                line,
                (x, y),
                font,
                font_scale,
                color,
                thickness,
                line_type)

# plt.imshow(image)
cv2.imshow("Result Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
