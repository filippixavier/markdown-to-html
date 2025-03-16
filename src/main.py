import os
import shutil
import sys

from convert import (markdown_to_html_node, extract_title)

def deep_copy(source, destination, sub_paths):
    source_path = os.path.join(source, sub_paths)
    for dir in os.listdir(source_path):
        next_subs = os.path.join(sub_paths, dir)
        full_source_path = os.path.join(source_path, dir)
        full_destination_path = os.path.join(destination, next_subs)
        if not os.path.isfile(full_source_path):
            os.mkdir(full_destination_path)
            deep_copy(source, destination, next_subs)
        else: 
            shutil.copy(full_source_path, full_destination_path)
            pass

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generate page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(from_path) as f:
        markdown = f.read()
        title = extract_title(markdown)
        content = markdown_to_html_node(markdown)
    with open(template_path) as f:
        html = f.read()
    html = html.replace("{{ Title }}", title).replace("{{ Content }}", content.to_html()).replace("href=\"/", "href=\"" + basepath).replace("src=\"/", "src=\"" + basepath)

    with open(dest_path, "x") as f:
        f.write(html)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for dir in os.listdir(dir_path_content):
        new_source = os.path.join(dir_path_content, dir)
        new_dest = os.path.join(dest_dir_path, dir)
        if os.path.isfile(new_source):
            generate_page(new_source, template_path, new_dest.replace(".md", ".html"), basepath)
        else:
            generate_page_recursive(new_source, template_path, new_dest, basepath)


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")
    os.mkdir("./docs")
    if os.path.exists("./static"):
        deep_copy("./static", "./docs", "")
    # generate_page("./content/index.md", "template.html", "./public/index.html")
    generate_page_recursive("./content", "template.html", "./docs", basepath)

if __name__ == "__main__":
    main()
