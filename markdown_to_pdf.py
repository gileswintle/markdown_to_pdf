from markdown import markdown
from weasyprint import HTML, CSS
import os
from weasyprint.fonts import FontConfiguration
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import subprocess
import os
from processing import process_html

root = tk.Tk()
root.withdraw()

content_file = filedialog.askopenfilename()
# content_file = input('file name: ')

cf_all = content_file
cf_directory, cf_file = os.path.split(cf_all)

# print('dir:',cf_directory, 'file:',cf_file)

# cur_dir = os.getcwd()


# css_file = pathlib.Path.cwd().parent / "reporting" / "reporting.css"
css_file = "/Users/gileswintle/Library/Application Support/MacDown/Styles/Cassian_report_3.css"
# out_file = 'report.pdf'
out_file = f'{content_file[:-2]}pdf'
# os.popen(f"open {out_file}")

# print(os.getcwd())

with open(content_file, "r", encoding="utf-8") as input_file:
    text = input_file.read()
content_html = markdown(text, extensions=['footnotes', 'tables', 'attr_list'])
content_html = content_html.replace('images/', f'{cf_directory}/images/' )

content_html = process_html(content_html)

# print(content_html)
# os.chdir(cf_directory)
HTML(string=content_html, base_url=__file__).write_pdf(out_file, stylesheets=[css_file])

# os.chdir(cur_dir)

subprocess.run(['open', out_file], check=True)


