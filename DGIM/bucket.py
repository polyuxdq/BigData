#!/usr/bin/python3
import math


class Bucket:

    def __init__(self):
        self.timestamp = 0
        self.bucket = {}  # dictionary
        self.key = []
        self.bucket_num_range = int((math.log(100, 2)))  # enough for holding 100 bit
        for i in range(self.bucket_num_range):
            self.key.append(int(math.pow(2, i)))
            self.bucket[self.key[i]] = []

    def get_bucket(self):
        return self.bucket

    def get_key(self):
        return self.key

    def get_timestamp(self):
        return self.timestamp

    def add_bucket(self, bit):
        self.timestamp = self.timestamp + 1
        if int(bit):
            self.bucket[self.key[0]].insert(0, self.timestamp)
            for i in range(self.bucket_num_range):
                current_bucket = self.bucket[self.key[i]]
                # update block, leave the last one
                if len(current_bucket) > 2 and i is not self.bucket_num_range - 1:
                    time = current_bucket.pop()
                    current_bucket.pop()
                    self.bucket[self.key[i + 1]].insert(0, time)
        # discard out-of-date data
        for i in range(self.bucket_num_range):
            current_bucket = self.bucket[self.key[i]]
            for j in range(len(current_bucket)):
                if self.timestamp - current_bucket[j] >= 100:  # 101 - 1 = 100
                    current_bucket.pop(j)
                    break  # only remove one element at a time, to be improved

    def estimate_sum(self):
        bucket_sum = 0
        weight = 1
        # count all with non-full window
        if self.timestamp <= 100:
            for i in range(self.bucket_num_range):
                bucket_sum = bucket_sum + len(self.bucket[self.key[i]]) * weight
                weight = weight * 2
        else:
            smallest_timestamp = self.timestamp  # for update
            for i in range(self.bucket_num_range):
                current_bucket = self.bucket[self.key[i]]
                bucket_sum = bucket_sum + len(current_bucket) * weight
                weight = weight * 2
                # find the oldest timestamp
                for j in range(len(current_bucket)):
                    if current_bucket[j] < smallest_timestamp:
                        smallest_timestamp = current_bucket[j]
            timestamp_gap = smallest_timestamp - (self.timestamp - 99)  # 33 - (101 - 99) = 31
            # print(timestamp_gap, end=')')
            bucket_sum = bucket_sum + timestamp_gap // 2  # half size of 1s
        return bucket_sum


if __name__ == '__main__':
    bucket = Bucket()
    # print(bucket.get_key())
    # print(0, bucket.get_bucket())
    for i in range(150):
        bucket.add_bucket('1')
        print(bucket.get_timestamp(), bucket.estimate_sum(), bucket.get_bucket())
