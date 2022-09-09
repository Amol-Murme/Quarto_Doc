from docx import Document
import lxml

def set_updatefields_true(docx_path):
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    doc = Document(docx_path)
    # add child to doc.settings element
    element_updatefields = lxml.etree.SubElement(
        doc.settings.element, f"{namespace}updateFields"
    )
    element_updatefields.set(f"{namespace}val", "true")
    doc.save(docx_path)## Heading ##

# set_updatefields_true("test.docx") 
set_updatefields_true("/home/oem/Documents/quarto/Quarto_Doc/test.docx") 

print("Finished")