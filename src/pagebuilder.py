import os, shutil
from helpers import markdown_to_html_node

def copy_dir(source, destination):
    if not os.path.exists(source):
        raise ValueError(f"Source path does not exist: {source}")
    if not os.path.exists(destination):
        os.mkdir(destination)
    source_contents = os.listdir(source)
    for item in source_contents:
        fullpath_source = os.path.join(source, item)
        fullpath_dest = os.path.join(destination, item)
        if os.path.isfile(fullpath_source):
            shutil.copy(fullpath_source, fullpath_dest)
        else:
            copy_dir(fullpath_source, fullpath_dest)

def extract_title(markdown:str):
    if not markdown.startswith("# "):
        raise ValueError("Markdown lacks a top heading")
    lines = markdown.split("\n")
    return lines[0].lstrip("# ") # We already proved there's at least one line
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    incoming_markdown = open(from_path).read()
    template = open(template_path).read()
    html = markdown_to_html_node(incoming_markdown).to_html()
    title = extract_title(incoming_markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    open(dest_path, "w").write(template)