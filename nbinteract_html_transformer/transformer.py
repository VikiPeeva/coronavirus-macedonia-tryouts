import sys, getopt, codecs
import xml.sax

from html.parser import HTMLParser
from bs4 import BeautifulSoup


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('transformer.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('transformer.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    input_html = codecs.open(input_file)
    input_tree = BeautifulSoup(input_html, 'html.parser')
    divs = input_tree.body.findAll('div', {'class': 'cell border-box-sizing code_cell rendered'})

    template_html = codecs.open("template.html", "r", "utf-8")
    template_tree = BeautifulSoup(template_html, 'html.parser')
    container_div = template_tree.body.find('div', {'class': 'container'})

    i = 0
    for div in divs:
        div['class'].append('nbinteract-hide_in')
        container_div.insert(i, div)
        i = i + 1

    with open(output_file, "w") as file:
        file.write(template_tree.prettify())


if __name__ == "__main__":
    main(sys.argv[1:])
