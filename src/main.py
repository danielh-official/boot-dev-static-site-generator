import os
import shutil

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

def main():
    copy_directory("static", "public")
    obj = TextNode("This is some anchor text", TextType.PLAIN, "https://www.boot.dev")

    print(obj.__repr__())

main()