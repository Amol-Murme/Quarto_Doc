from tabulate import tabulate
import pandas as pd

def align_table(tabulated ,align):

    if align == "right":
        if "-|" in tabulated:
            new_text = tabulated.replace("-|", ":|")
    elif align == "left":
        if "|-" in tabulated:
            new_text = tabulated.replace("|-", "|:") 
    else:
        new_text = tabulated.replace("|-", "|:")
        new_text = new_text.replace("-|", ":|")

    # print(new_text)
    return new_text


text = ""
with open('hello.qmd') as file:
    text = file.readlines()

print(text)
#Add regex for searching - complexity increases to O(n^2)
search_index = text.index('Methodology Overview Table:\n')
print(search_index)  

df = pd.read_csv('Data source/test.csv')

headers = df.columns.tolist()
table = df.values.tolist()


org_table = "\n\n"
org_table += align_table(tabulate(table, headers = headers, tablefmt="github"), "center")
org_table += "\n\n"
org_table += r': {tbl-colwidths="[34,33,33]"}'
org_table += "\n\n\n" 
print(org_table)

text.insert(search_index + 1, org_table)

# print(text)

with open('auto_hello.qmd', 'w') as file:
    file.writelines(text)
    
