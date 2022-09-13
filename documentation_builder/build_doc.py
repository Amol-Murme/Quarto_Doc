from os import rename
import subprocess
import shutil

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

    text = text.replace("../input/", "../../input/") 

    with open("../output/html/Base_Template.html","w") as f:
        f.write(text)

def copy_files():
    img_source =  "../input/"
    img_dest = "../app/static/assets/images"

    files_source = "../output/html/"
    files_dest = "../app/static/"

    img_res = shutil.copyfile(img_source, img_dest)
    file_res = shutil.copyfile(files_source, files_dest)

    



if __name__ == "__main__":
    build_doc()
    rename_img_paths()