import os
import shutil

from _ import extract_title, markdown_to_html_node
from textnode import *


def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for name in os.listdir(src):
        src_path, dst_path = os.path.join(src, name), os.path.join(dst, name)
        if os.path.isfile(src_path):
            print(f"copy {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            copy_directory(src_path, dst_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    page = template.replace("{{ Title }}", extract_title(markdown)).replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for name in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, name)
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, os.path.join(dest_dir_path, name))
        elif name.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, name[:-3] + ".html")
            generate_page(src_path, template_path, dest_path)


def main():
    copy_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    obj = TextNode("This is some anchor text", TextType.PLAIN, "https://www.boot.dev")

    print(obj.__repr__())

main()