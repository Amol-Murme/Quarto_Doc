from tabulate import tabulate
import pandas as pd


text = ""
with open('template.qmd') as file:
    text = file.readlines()

print(text)
#Add regex for searching - complexity increases to O(n^2)
title_index = text.index('title: ""\n')
print(title_index)  

toc_index = text.index('toc: true\n')
print(toc_index)

# text.insert(search_index + 1, org_table)

# # print(text)

# with open('auto_hello.qmd', 'w') as file:
#     file.writelines(text)
    
