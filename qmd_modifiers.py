def add_heading(heading):
    text = "\n"
    text += "## " + str(heading) + "\n"
    # text +="\n\n\n"

    return text

def add_text_content(text_content):
    text = "\n"
    text += str(text_content) + "\n"
    # text +="\n\n\n"

    return text    

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