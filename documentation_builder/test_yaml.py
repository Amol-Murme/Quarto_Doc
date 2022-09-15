import yaml
from bs4 import BeautifulSoup
import re
import os

with open("../output/html/Base_Template.html","r") as f:
        text= f.read()

# print(text)   
if "../../input/" not in text:
    text = text.replace("../input/", "../../input/") 



