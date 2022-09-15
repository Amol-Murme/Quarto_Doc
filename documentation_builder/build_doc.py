from os import rename
import subprocess
import shutil
import os
from bs4 import BeautifulSoup
import re
import yaml

def build_doc():

    qmd_template = "Base_Template.qmd"
    html_output_path = "../output/html/"
    docx_output_path = "../output/docx/"
    pdf_output_path = "../output/pdf/"

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
    with open("../output/html/Base_Template.html","r") as f:
        text= f.read()

    # print(text)   
    if "../../input/" not in text:
        text = text.replace("../input/", "../../input/") 


    with open("../output/html/Base_Template.html","w") as f:
        f.write(text)

def copy_files():
    img_source =  "../input/"
    img_dest = "../app/static/doc_images"

    files_source = "../output/html/"
    files_dest = "../app/static/doc_statics"

    html_file = "../app/static/doc_statics/Base_Template.html"
    html_dest = "../app/templates/"
    html_dest_file = "../app/templates/Base_Template.html"

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

    with open('../app/templates/Base_Template.html', 'wb') as f:
        f.write(bs.prettify("utf-8"))

def add_button_n_modal():
    html_contents = open("../app/templates/Base_Template.html", "r")

    soup = BeautifulSoup(html_contents, 'html.parser')
    # print(html_contents)

    # add jquery script
    script = soup.new_tag('script')
    script['src'] = r"{{ url_for('static', path='/js/jquery.js') }}"

    body = soup.find('body')
    body.append(script)

    #add custom script
    script2 = soup.new_tag('script')
    script2['src'] = r"{{ url_for('static', path='/js/index.js') }}"
    body.append(script2)

    #add button
    button = soup.new_tag('button')
    button['type'] = "button"
    button['class'] = "btn btn-primary btn-lg btn-block"
    button['onclick'] = "save_edited()"
    button.append("Save Edited Document")

    main = soup.find('main')
    main.insert_after(button)

    #add modal
    '''
    <div class="modal" tabindex="-1" role="dialog">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
        <div class="modal-body">
            <p>Modal body text goes here.</p>
        </div>
        </div>
    </div>
    </div>
    '''

    modal = soup.new_tag('div')
    modal['class'] = "modal"
    modal['id'] = "loader"
    modal['tabindex'] = "-1"
    modal['role'] = "dialog"
    modal['data-backdrop'] = "static"
    modal['data-keyboard'] = "false"
    modal['aria-hidden'] = "true"

    modal_dialog = soup.new_tag('div')
    modal_dialog['class'] = "modal-dialog"
    modal_dialog['role'] = "document"

    modal_content = soup.new_tag('div')
    modal_content['class'] = "modal-content"

    modal_body = soup.new_tag('div')
    modal_body['class'] = "modal-body"

    #  <center><img src="https://miro.medium.com/max/500/1*em5HcTFZIQw90qIgdbYjVg.gif"></center>

    center = soup.new_tag('center')
    img = soup.new_tag('img')
    img['src'] = "https://miro.medium.com/max/500/1*em5HcTFZIQw90qIgdbYjVg.gif"
    center.append(img)

    modal_body.append(center)
    modal_content.append(modal_body)
    modal_dialog.append(modal_content)
    modal.append(modal_dialog)

    main = soup.find('main')
    main.insert_after(modal)
    main.insert_after(button)


    with open('../app/templates/new_Base_Template.html', 'wb') as f:
            f.write(soup.prettify("utf-8"))

if __name__ == "__main__":
    build_doc()
    rename_img_paths()
    copy_files()
    rename_app_paths()
    add_button_n_modal()