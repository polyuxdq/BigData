#!/usr/bin/python3
from lxml import etree
import codecs
import os


CATEGORY = {'article', 'inproceedings', 'proceedings', 'book', 'incollection',
            'phdthesis', 'mastersthesis', 'www', 'person', 'data'}


def output_author_pair(author, file_write, separator='\t'):
    if len(author) > 1:
        author.sort()
        for i in range(len(author)-1):
            for j in range(i+1, len(author)):
                file_write.write('\"' + author[i] + '\"' + separator)  # further
                file_write.write('\"' + author[j] + '\"' + separator)
                file_write.write(str(1) + '\n')


def find_all_from_tag(element, tag='author'):
    find = []
    for match in element.iterfind('.//%s' % tag):  # XPath: all sub-elements on all levels beneath current element
        find.append(match.text)
    return find


def main(xml='dblp.xml', separator='\t'):
    i = 0
    with codecs.open('dblp.map.txt', 'w', 'utf-8') as map_out:
        for event, element in etree.iterparse(xml, tag=CATEGORY, dtd_validation=True, load_dtd=True):
            author = find_all_from_tag(element, tag='author')
            output_author_pair(author, map_out, separator=separator)
            # print('%d %s' % (i, author))
            element.clear()  # very important!
            i = i + 1
            if i % 10000 == 0:
                print('Reading', str(i), 'Elements...')
    print('Total:', str(i), 'Elements.')


if __name__ == "__main__":
    main()
    print('''sort -t $'\t' -k1 -k2 dblp.map.txt -o sort.dblp.map.txt''')
    os.system('''sort -t $'\t' -k1 -k2 dblp.map.txt -o sort.dblp.map.txt''')
