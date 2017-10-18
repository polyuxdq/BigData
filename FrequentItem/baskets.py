#!/usr/bin/python3
class Baskets:

    def __init__(self):
        self.baskets = [[]]
        for b in self.range_with_end(1, 1000):
            temp_basket = []
            for i in self.range_with_end(1, 1000):
                if b % i == 0:
                    temp_basket.append(i)
            self.baskets.append(temp_basket)

    @staticmethod
    def range_with_end(start, end):
        return range(start, end + 1)

    def get_basket(self, num):
        if num in self.range_with_end(1, 1000):
            return self.baskets[num]
        else:
            return None


if __name__ == "__main__":
    baskets = Baskets()
    for index in Baskets.range_with_end(1, 1000):
        print(index, baskets.get_basket(index))
