from textnode import *

def main():
    obj = TextNode("This is some anchor text", TextType.PLAIN, "https://www.boot.dev")

    print(obj.__repr__())

main()