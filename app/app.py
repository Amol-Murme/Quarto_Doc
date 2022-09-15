from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import subprocess
import yaml
from qmd_modifiers import *
from pydantic import BaseModel, Json
from typing import Dict

# import sys
# sys.path.append('../documentation_builder/')
from build_doc import *

class VariablesJson(BaseModel):
    data: Dict



api = FastAPI()

api.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# @api.get("/", response_class=HTMLResponse)
# async def read_item(request:Request):
#     return templates.TemplateResponse("index.html",{'request':request})

@api.get("/", response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("new_Base_Template.html",{'request':request})    

@api.post("/recompute")
async def recompute(variablesJson : VariablesJson):
    data = variablesJson.data

    with open('../documentation_builder/_variables.yml', 'w') as file:
        documents = yaml.dump(data, file)

    build_doc()
    rename_img_paths()
    copy_files()
    rename_app_paths()
    make_content_editable()

    return  variablesJson     

@api.get("/api/render_html")
def calculate():
    html_output = subprocess.call(["quarto", "render", "hello.qmd"], universal_newlines=True)

    result = {
        'Success' : "Finished Rendering HTML",
        'html_output' : html_output,
    }
    return result

@api.get("/api/render_docx")
def calculate():
    # subprocess.call(["quarto", "preview", "hello.qmd", "--to", "docx", "--no-browser", "--no-watch-inputs"])
    docx_output = subprocess.call(["quarto", "render", "hello.qmd", "--to", "docx"], universal_newlines=True)
    result = {
        'Success' : "Finished Rendering DOCX",
        'docx_output' : docx_output,
    }
    return result  

@api.get("/api/render_pdf")
def calculate():
    pdf_output = subprocess.call(["quarto", "render", "hello.qmd", "--to", "pdf"], universal_newlines=True)
    result = {
        'Success' : "Finished Rendering DOCX",
        'pdf_output' : pdf_output,
    }
    return result  

@api.post("/generate_doc/")
async def login(request:Request,
                companyName: str = Form(),
                toc_check: bool = Form(False),
                heading: str = Form(), 
                text_content: str = Form() ):

    #read from template
    with open('template.qmd') as file:
        text = file.readlines()    

    title_index = text.index('title: ""\n')
    toc_index = text.index('toc: true\n')  

    text[title_index] = f'title: "{str(companyName).upper()}"\n'  
    text[toc_index] = f'toc: {str(toc_check).lower()}\n'
    text.append(add_heading(heading))
    text.append(add_text_content(text_content))


    filename = companyName + ".qmd"
    with open(filename, 'w') as file:
        file.writelines(text)

    docx_output = subprocess.call(["quarto", "render", filename, "--to", "docx"], universal_newlines=True)
    
    # result = {"companyName": companyName,
    #          "toc_check":toc_check,
    #          "heading": heading,
    #          "text_content": text_content,
    #          "filename" : filename} 

    # return  result
    html_file = companyName + ".html"
    html_output = subprocess.call(["quarto", "render", filename], universal_newlines=True)

    cp_out = subprocess.call(["cp", html_file, "templates/"], universal_newlines=True)

    return templates.TemplateResponse(html_file, {'request':request})



if __name__ == "__main__":
    uvicorn.run(api, port=8000)    