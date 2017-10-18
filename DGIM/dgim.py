#!/usr/bin/python3
from bucket import Bucket
import copy


def read_stream_data(file):
        for line in file:
            data = line.strip().split(' ')
            stream = iter(data)
            for i in range(len(data)):
                yield next(stream)


def decimal_to_binary(decimal):
    decimal = int(decimal)
    if decimal not in range(1024):
        return None
    binary = [0] * 10
    for i in range(10):
        binary[i] = decimal % 2
        decimal = decimal // 2
    return binary


def update_bit_stream_and_bucket(data, bit_stream, bit_bucket):
    binary = decimal_to_binary(int(data))
    for i in range(len(binary)):
        bit_stream[i].insert(0, binary[i])
        bit_bucket[i].add_bucket(binary[i])
    if len(bit_stream[0]) > 100:
        for i in range(len(bit_stream)):
            bit_stream[i].pop()  # remove the last element


def get_single_bit_stream_sum(single_bit_stream):
    return sum(int(one) for one in single_bit_stream)


def get_separation_list(ith_bit_stream, ith_bit_bucket):
    # storage
    bucket_timestamp_list = []
    bucket_separation_list = []

    # extract the timestamp
    ith_bucket_timestamp_from_dict = list(ith_bit_bucket.get_bucket().values())
    for temp_timestamp in ith_bucket_timestamp_from_dict:
        bucket_timestamp_list.extend(temp_timestamp)

    # subtract from the timestamp
    base = int(ith_bit_bucket.get_timestamp())
    length_of_timestamp = len(bucket_timestamp_list)
    for j in range(length_of_timestamp):
        bucket_timestamp_list[j] = base - bucket_timestamp_list[j]
    # print(bucket_timestamp_list)

    # separate the stream
    if len(bucket_timestamp_list) > 0:
        # first
        start = bucket_timestamp_list[0] + 1
        bucket_separation_list.append(ith_bit_stream[0:start])
        # intermediate
        for j in range(length_of_timestamp - 1):
            start = bucket_timestamp_list[j] + 1
            end = bucket_timestamp_list[j + 1] + 1
            bucket_separation_list.append(ith_bit_stream[start:end])
        # the last one
        end = bucket_timestamp_list[-1] + 1
        if len(ith_bit_stream[end:]) > 0:  # skip with bucket with full area
            bucket_separation_list.append(tuple(ith_bit_stream[end:]))  # extend, not induce error but empty
        # print(bucket_separation_list)
    else:  # skip with empty
        bucket_separation_list = ith_bit_stream

    # # if the last step is append
    # temp = []
    # for i in range(len(bucket_separation_list)):
    #     temp.extend(bucket_separation_list[i])
    # print(temp == ith_bit_stream)

    return bucket_separation_list


def get_normalized_timestamp(ith_bit_bucket):
    timestamp = ith_bit_bucket.get_timestamp()
    bucket = copy.deepcopy(ith_bit_bucket.get_bucket())  # copy
    key = ith_bit_bucket.get_key()
    for i in range(len(bucket)):
        timestamp_list = bucket[key[i]]
        for j in range(len(timestamp_list)):
            timestamp_list[j] = timestamp - timestamp_list[j] + 1
    return bucket


def output_bit_stream_and_bucket(bit_stream, bit_bucket):
    print('\nThe left most bit is the coming one.\n')
    for i in range(len(bit_stream)):
        ith_bit_stream = bit_stream[i]
        ith_bit_bucket = bit_bucket[i]
        separation_of_stream = get_separation_list(ith_bit_stream, ith_bit_bucket)
        normalized_timestamp_list = get_normalized_timestamp(ith_bit_bucket)
        # output
        print('stream %d:' % i)
        print(bit_stream[i])
        print(separation_of_stream)
        # print(ith_bit_bucket.get_timestamp())
        # print(ith_bit_bucket.get_bucket())
        print(normalized_timestamp_list)
        print('true_sum = %d, estimate_sum = %d\n' %
              (get_single_bit_stream_sum(bit_stream[i]), bit_bucket[i].estimate_sum()))


def estimate_sum_of_last_hundred(bit_stream, bit_bucket):
    summation = 0
    weight = 1
    for i in range(len(bit_stream)):
        summation = summation + bit_bucket[i].estimate_sum() * weight
        weight = weight * 2
    return summation


def main():
    # bit stream: raw data
    bit_stream = []
    bit_bucket = []
    for i in range(10):
        bit_stream.append([])
        bit_bucket.append(Bucket())

    count = 0
    number_stream = []

    with open('cmsc5741_stream_data.txt', 'r') as file_read:
        integer_stream = read_stream_data(file_read)
        for data in integer_stream:
            update_bit_stream_and_bucket(data, bit_stream, bit_bucket)  # function convert data into int
            # estimation
            estimation_sum = estimate_sum_of_last_hundred(bit_stream, bit_bucket)
            # real
            number_stream.insert(0, data)
            if len(number_stream) > 100:
                number_stream.pop()
            true_sum = sum(int(num) for num in number_stream)
            # output
            count = count + 1
            print('%d true_sum = %d, estimate_sum = %d, error = %.3f%%' %
                  (count, true_sum, estimation_sum, (estimation_sum-true_sum)/true_sum*100))
        # whenever output is needed
        output_bit_stream_and_bucket(bit_stream, bit_bucket)


if __name__ == '__main__':
    main()
