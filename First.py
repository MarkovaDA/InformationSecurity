import math
import matplotlib.pyplot as plot


class Tests(object):
    default_expected_value = 0.5
    default_variance = 1.0 / 12

    def __init__(self, counts, length, random_list):
        self.k = counts
        self.n = length
        self.values = random_list

    # 1
    def first_test(self):
        expected_value = 0
        variance = 0
        for number in self.values:
            expected_value += number
        expected_value /= float(self.n)

        for number in self.values:
            variance += (number - expected_value) ** 2
        variance /= float(self.n)
        print "default expected value = %s, we have - %s" % (str(self.default_expected_value), str(expected_value))
        print "default variance = %s, we have - %s" % (str(self.default_variance), str(variance))

    # 2
    def typical_task(self):
        count_events = 0
        for index in range(1, self.n/2):
            # sum = (self.values[index-1]**2 + self.values[index]**2) ** 0.5
            sum = (self.values[2*(index-1)]**2 + self.values[2*index]**2) ** 0.5
            if sum < 1:
                count_events += 1
        round_pi = 8 * count_events / float(self.n)
        print "default pi = %s, we have - %s" % (str(math.pi), str(round_pi))

    # 3
    def hi(self, dict):
        p = 1.0 / self.k
        hi = 0
        for key in dict:
             hi += (dict[key] - p * self.n) ** 2
        hi /= (p * self.n)
        print "We have %s squared-hi" % (str(hi))

    # 4
    def histogram(self):
        _min = min(self.values)
        interval = (max(self.values) - _min) / float(self.k)
        hist_dict = {}
        for i in range(1, 11):
            hist_dict[i] = 0
        hist_list = []
        for number in self.values:
            for i in range(1, 11):
                if (number >= (_min + (i-1)*interval)) and (number <= (_min + i*interval)):
                    hist_list.append(i)
                    hist_dict[i] += 1
                    break
        print hist_dict.items()
        self.hi(hist_dict)
        plot.hist(hist_list, self.k)
        plot.show()

    # 5
    def digital_dimension(self):
        hist_list = []
        for number in self.values:
            for i in range(1, 11):
                after_dot = math.trunc(10 * number)
                if after_dot == i:
                    hist_list.append(i)
                    break
        plot.hist(hist_list, self.k)
        plot.show()


class Random(object):
    pi = math.pi
    default_n = 20000

    def frac(self, number):
        return number - int(number)

    def random(self, r):
        r = round(r, 4)
        result = []
        i = 1
        while r not in result and len(result) < self.default_n:
            print i
            i += 1
            result.append(r)
            r = self.frac(11*r + self.pi)
        self.length = len(result)
        return result

    def __init__(self, r0):
        self.numbers = self.random(r0)

    def print_list(self):
        for element in self.numbers:
            print element,


'''r1 = 0.5
r2 = 0.002
k = 10
random = Random(r1)
n = random.length
tests = Tests(k, n, random.numbers)
tests.first_test()
tests.typical_task()
tests.histogram()
tests.digital_dimension()'''
