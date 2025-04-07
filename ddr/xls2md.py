#!/usr/bin/env python3

import pandas as pd
import sys
from tabulate import tabulate

workbook_filename = sys.argv[1]
workbook = pd.ExcelFile(workbook_filename)
for name in workbook.sheet_names:
   df = pd.read_excel(workbook, name)
   with open(f"{name}.md", 'w') as markdown_file:
       for line in tabulate(df, headers='keys', tablefmt='github').splitlines():
           print(line.replace('nan', '   '), file=markdown_file)