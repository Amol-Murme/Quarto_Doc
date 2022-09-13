import yaml
from bs4 import BeautifulSoup
import re
import os


html_contents = open("../app/templates/Base_Template.html", "r")

soup = BeautifulSoup(html_contents, 'html.parser')
# print(html_contents)


#read .yml variables
with open('_variables.yml') as file:
    var_list = yaml.load(file, Loader=yaml.FullLoader)

# print(var_list)

#list of probable elements to search
elements = ['p', 'h2', 'h3', 'strong']

for k,v in var_list.items():
    # print(k)
    for ele in elements:
        matched_tags = soup.find_all(lambda tag: (len(tag.find_all()) == 0 )
                                                  and(str(tag.text).strip() == str(v).strip())
                                                  and (ele in tag.name)
                                                  and ( "figcaption" not in tag.name )
                                    )

        if matched_tags != []:
            for tag in matched_tags:
                tag["contenteditable"] = "true"
                tag["style"] = "background-color:powderblue;"
                tag["id"] = str(k)


with open('../app/templates/new_Base_Template.html', 'wb') as f:
        f.write(soup.prettify("utf-8"))
