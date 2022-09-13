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

#         # html_line["contenteditable"] = "true"

for k,v in var_list.items():
    print(k)
    # string_search = r"^"+str(v)+r"$"
    # print(string_search)
    # my_regex = re.compile(str(v))
    # print(my_regex)
    for ele in elements:
        matched_tags = soup.find_all(lambda tag: (len(tag.find_all()) == 0 )
                                                #  and (tag.find_all(ele,text=str(v)))
                                                #   and (str(v) in  tag.text)
                                                 and(str(tag.text).strip() == str(v).strip())
                                                  and (ele in tag.name)
                                                #   and (len(tag.attrs) <=2)
                                    )

        if matched_tags != []:
            print(ele)
            print(matched_tags)
            # print(type(matched_tags))
            # for i in matched_tags:
            #     print(str(i.text).strip() == str(v).strip())
        print("="*50)
# for matched_tag in matched_tags:
#     print("Matched:", matched_tag)


