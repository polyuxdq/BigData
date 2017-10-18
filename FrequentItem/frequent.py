#!/usr/bin/python3
from baskets import Baskets
from itertools import combinations
import numpy as np

NUM_RANGE = Baskets.range_with_end(1, 1000)
baskets = Baskets()


def search_individual(threshold):
    # storage for each individual item
    item_list = np.zeros(1001, dtype=np.int)

    # count the support of item
    for i in NUM_RANGE:
        ith_basket = baskets.get_basket(i)
        for j in range(len(ith_basket)):
            item_num = ith_basket[j]
            item_list[item_num] = item_list[item_num] + 1

    # find the frequent item
    frequent = []
    for i in NUM_RANGE:
        if item_list[i] >= threshold:
            frequent.append([[i], item_list[i]])  # add list for each
    return frequent


def search_pair(individual, threshold):
    # storage for each individual item
    single_item_num = len(individual)
    pair_name_list = []
    pair_count_list = []
    for i in range(single_item_num-1):
        for j in range(i+1, single_item_num):
            temp_pair_to_append = list(set(individual[i][0] + individual[j][0]))  # not sorted!!
            temp_pair_to_append.sort()
            pair_name_list.append(temp_pair_to_append)
            pair_count_list.append(0)
    pair_name_list.sort()

    # count the support of item
    for i in NUM_RANGE:
        ith_basket = baskets.get_basket(i)
        for j in range(len(ith_basket)-1):
            for k in range(j+1, len(ith_basket)):  # old method
                temp_pair = [ith_basket[j], ith_basket[k]]
                if temp_pair in pair_name_list:
                    index_of_pair = pair_name_list.index(temp_pair)
                    pair_count_list[index_of_pair] = pair_count_list[index_of_pair] + 1

    # find the frequent item
    frequent = []
    for i in range(len(pair_name_list)):
        if pair_count_list[i] >= threshold:
            frequent.append([pair_name_list[i], pair_count_list[i]])
    return frequent


def search_frequent_from_itemset_size_n(itemset, threshold):
    # storage for each itemset
    original_itemset_length = len(itemset)
    if original_itemset_length <= 1:
        return None
    original_itemset_size = len(itemset[0][0])
    next_itemset_name_list = []
    next_itemset_count_list = []
    original_itemset_unit = []
    next_itemset_count_list_use_tuple = []
    for i in range(original_itemset_length):
        original_itemset_unit.append(itemset[i][0])
    # print('original_itemset_unit:', original_itemset_unit)
    combinations_of_item_list = list(combinations(original_itemset_unit, 2))
    # print('combinations', len(combinations_of_item_list), combinations_of_item_list)
    for i in range(len(combinations_of_item_list)):
        temp_itemset = list(set(combinations_of_item_list[i][0] + combinations_of_item_list[i][1]))
        temp_itemset.sort()  # remember to sort
        next_itemset_count_list_use_tuple.append(tuple(temp_itemset))
    next_itemset_count_list_use_tuple = list(set(next_itemset_count_list_use_tuple))
    # remove same element with set

    for i in range(len(next_itemset_count_list_use_tuple)):
        temp_itemset = list(next_itemset_count_list_use_tuple[i])
        if len(temp_itemset) == original_itemset_size+1:
            next_itemset_name_list.append(temp_itemset)
            next_itemset_count_list.append(0)
    next_itemset_name_list.sort()
    print('next_itemset_name_list', len(next_itemset_name_list), next_itemset_name_list, '\n')

    # count the support of itemset
    '''improvement credit to Ms Huang'''
    previous_frequent_itemset = []
    for i in range(len(itemset)):
        previous_frequent_itemset.extend(itemset[i][0])
    previous_frequent_itemset = set(previous_frequent_itemset)
    # print(previous_frequent_itemset)

    for i in NUM_RANGE:
        ith_basket = baskets.get_basket(i)
        ith_basket = previous_frequent_itemset.intersection(set(ith_basket))  # set form
        '''Another improvement with removal of short basket'''
        if len(ith_basket) < original_itemset_size+1:
            continue
        # get the intersection -> subset
        for j in range(len(next_itemset_count_list)):
            if set(next_itemset_name_list[j]).issubset(ith_basket):
                next_itemset_count_list[j] = next_itemset_count_list[j] + 1

    # find the frequent item
    frequent = []
    for i in range(len(next_itemset_name_list)):
        if next_itemset_count_list[i] >= threshold:
            frequent.append([next_itemset_name_list[i], next_itemset_count_list[i]])
    return frequent


def main():
    individual = search_individual(20)
    print('frequent itemset with size 1:', len(individual),
          individual, '\n\n', str('-'*120), '\n')
    itemset_pair = search_pair(individual, 20)
    itemset_iter = search_frequent_from_itemset_size_n(individual, 20)
    # itemset_pair = itemset_iter  # simple loop is very slow

    with open('B.txt', 'w') as output:
        output.write('Support Threshold 20, frequent items:\n')
        for i in range(len(individual)):
            output.write(str(individual[i][0]))
            if i is not len(individual)-1:
                output.write(', ')
        output.write('\nSupport Threshold 20, frequent item pairs:\n')
        for i in range(len(itemset_pair)):
            output.write(str(itemset_pair[i][0]))
            if i is not len(itemset_pair)-1:
                output.write(', ')

        itemset_size = 2
        last_itemset_iter = itemset_iter
        if itemset_iter == itemset_pair:
            while itemset_iter is not None:
                print('frequent itemset with size ' + str(itemset_size) + ':',
                      len(itemset_iter), itemset_iter, '\n\n', str('-'*120), '\n')
                last_itemset_iter = itemset_iter
                itemset_iter = search_frequent_from_itemset_size_n(last_itemset_iter, 20)
                itemset_size = itemset_size + 1
            output.write('\nSupport Threshold 20, maximal frequent itemsets:\n')
            for i in range(len(last_itemset_iter)):
                output.write(str(last_itemset_iter[i][0]))
                if i is not len(last_itemset_iter)-1:
                    output.write(', ')
            output.write('\n')


if __name__ == '__main__':
    main()
