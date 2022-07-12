from framework.ui import *
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--title",help="Quizz title")
    parser.add_argument("-d","--descrip",help="Quizz description")

    parser.add_argument("-T","--txt-dir",help="txt files directory")
    parser.add_argument("-P","--pcap-dir",help="pcap files directory")

    parser.add_argument("template", nargs=argparse.REMAINDER, default="", help="Template a parsear")
    args = parser.parse_args()
    
    title =  input("Quiz Name: ") if not hasattr(args,"title") else args.title
    descripcion = input("Descripción: ") if not hasattr(args,"descrip") else args.descrip
    
    a = MainInterface(title, descripcion)
    a.txt_dir = args.txt_dir
    a.pcap_dir = args.pcap_dir

    if len(args.template) != 0:
        pass
    
    a.run()
