from os import rename
import subprocess
import shutil
import os
from bs4 import BeautifulSoup
import re
import yaml

def build_doc():
    base = os.path.dirname(os.path.abspath(__file__))
    qmd_template = os.path.join(base, "Base_Template.qmd")
    html_output_path = os.path.join(base, "../output/html/")
    docx_output_path = os.path.join(base, "../output/docx/")
    pdf_output_path = os.path.join(base, "../output/pdf/")

    html_output = subprocess.call(
                                 ["quarto", "render", qmd_template,"--to", "html",
                                  "--output-dir", html_output_path], 
                                 universal_newlines=True)

    docx_output = subprocess.call(
                                 ["quarto", "render", qmd_template,"--to", "docx",
                                  "--output-dir", docx_output_path], 
                                 universal_newlines=True)

    pdf_output = subprocess.call(
                                 ["quarto", "render", qmd_template,"--to", "pdf",
                                  "--output-dir", pdf_output_path], 
                                 universal_newlines=True)

def rename_img_paths():
    base = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base, "../output/html/Base_Template.html")
    with open(file_path,"r") as f:
        text= f.read()

    # print(text)   

    text = text.replace("../input/", "../../input/") 
    #special_char = u"\u00a0"
    #text = text.replace([\x08-\x14\x20]+ ," ") 
    # text = text.replace(" ", " ") 

    with open(file_path,"w") as f:
        f.write(text)

def copy_files():
    base = os.path.dirname(os.path.abspath(__file__))
    img_source =  os.path.join(base, "../input/")
    img_dest = os.path.join(base, "../app/static/doc_images")

    files_source = os.path.join(base, "../output/html/")
    files_dest = os.path.join(base, "../app/static/doc_statics")

    html_file = os.path.join(base,"../app/static/doc_statics/Base_Template.html")
    html_dest = os.path.join(base, "../app/templates/")
    html_dest_file = os.path.join(base, "../app/templates/Base_Template.html")

    if os.path.exists(img_dest):
        shutil.rmtree(img_dest)
    img_res = shutil.copytree(img_source, img_dest)

    if os.path.exists(files_dest):
        shutil.rmtree(files_dest)    
    file_res = shutil.copytree(files_source, files_dest)

    if os.path.exists(html_dest_file):
        os.remove(html_dest_file)
    html_res = shutil.move(html_file, html_dest)    
    
def rename_app_paths():
    base = os.path.dirname(os.path.abspath(__file__))
    html = open(os.path.join(base, '../app/templates/Base_Template.html'))
    bs = BeautifulSoup(html, 'html.parser')

    images = bs.find_all('img')
    for img in images:
        if img.has_attr('src'):
            text = img['src']
            text_out = text.replace('../../input/','/doc_images/')
            path = r"{{ url_for('static', path='" + text_out + r"') }}"
            # print(path)
            img['src'] = path

    scripts = bs.find_all('script')
    for script in scripts:
        if script.has_attr('src'):
            text = script['src']
            text_out = text.replace('Base_Template_files/','/doc_statics/Base_Template_files/')
            path = r"{{ url_for('static', path='" + text_out + r"') }}"
            # print(path)
            script['src'] = path

    links = bs.find_all('link')
    for link in links:
        if link.has_attr('href'):
            text = link['href']
            text_out = text.replace('Base_Template_files/','/doc_statics/Base_Template_files/')
            path = r"{{ url_for('static', path='" + text_out + r"') }}"
            link['href'] = path

    base = os.path.dirname(os.path.abspath(__file__))
    path_loc = os.path.join(base, '../app/templates/Base_Template.html')
    with open(path_loc, 'wb') as f:
        f.write(bs.prettify("utf-8"))

def make_content_editable():
    base = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base, "../app/templates/Base_Template.html")
    html_contents = open(file_path, "r")

    soup = BeautifulSoup(html_contents, 'html.parser')
    # print(html_contents)


    #read .yml variables
    path_loc = os.path.join(base, '_variables.yml')
    with open(path_loc) as file:
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
                    tag["id"] = "editable_" + str(k)

    script = soup.new_tag('script')
    # script['selected'] = r"{{ url_for('static', path='/js/index.js') }}"
    script['src'] = r"{{ url_for('static', path='/js/index.js') }}"

    body = soup.find('body')
    body.append(script)

    button = soup.new_tag('button')
    button['type'] = "button"
    button['class'] = "btn btn-primary btn-lg btn-block"
    button['onclick'] = "save_edited()"
    button.append("Save Edited Document")

    main = soup.find('main')
    main.insert_after(button)

    base = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base, '../app/templates/new_Base_Template.html')

    with open(file_path, 'wb') as f:
            f.write(soup.prettify("utf-8"))

if __name__ == "__main__":
    build_doc()
    rename_img_paths()
    copy_files()
    rename_app_paths()
    make_content_editable()