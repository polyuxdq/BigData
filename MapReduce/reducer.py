#!/usr/bin/python3
from itertools import groupby
from operator import itemgetter
import codecs
import os


def read_format_file(file, separator='\t'):
    for line in file:
        yield line.strip().split(separator)


def main(pair='sort.dblp.map.txt', separator='\t'):
    i = 0
    with codecs.open('dblp.reduce.txt', 'w', 'utf-8') as reduce_out:
        with codecs.open(pair, 'r', 'utf-8') as reduce_in:
            data_list_in_line = read_format_file(reduce_in, separator=separator)
            # "author1", "author2", 1
            for author_pair, group in groupby(data_list_in_line, itemgetter(0, 1)):
                total_count = sum(int(count) for author1, author2, count in group)
                reduce_out.write(author_pair[0] + separator)
                reduce_out.write(author_pair[1] + separator)
                reduce_out.write(str(total_count) + '\n')
                i = i + 1
                if i % 10000 == 0:
                    print('Writing', str(i), 'Author Pairs...')
    print('Total:', str(i), 'Author Pairs.')


def list_top_100(reduce_out='sort.dblp.reduce.txt', separator='\t'):
    i = 0
    with codecs.open('A.txt', 'w', 'utf-8') as output:
        with codecs.open(reduce_out, 'r', 'utf-8') as reduce:
            data_list_in_line = read_format_file(reduce, separator=separator)
            # "author1", "author2", 1
            for data_list in data_list_in_line:
                output.write(data_list[0] + ' ' + data_list[1] + ' ' + data_list[2] + '\n')
                i = i + 1
                if i >= 100:
                    break


if __name__ == "__main__":
    main()
    print('''sort -t $'\t' -k3rn -k1 -k2 dblp.reduce.txt -o sort.dblp.reduce.txt''')
    os.system('''sort -t $'\t' -k3rn -k1 -k2 dblp.reduce.txt -o sort.dblp.reduce.txt''')
    list_top_100()
