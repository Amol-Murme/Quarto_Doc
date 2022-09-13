import re
from bs4 import BeautifulSoup
import os

# print(re.findall(r'(\/.*?\.[\w:]+)', "file path /log/file.txt some lines /log/var/file2.txt"))

# with open('Base_Template.html','r') as f:
#     text = f.read() 

# print(re.findall(r'(\/.*?\.[\w:]+)', text))

####################################################

base = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(base, 'Base_Template.html'))
bs = BeautifulSoup(html, 'html.parser')

images = bs.find_all('img')
for img in images:
    if img.has_attr('src'):
        print(img['src'])

scripts = bs.find_all('script')
for script in scripts:
    if script.has_attr('src'):
        print(script['src'])

links = bs.find_all('link')
for link in links:
    if link.has_attr('href'):
        print(link['href'])
