import csv
import matplotlib.pyplot as plt
name1 = 'out_0001.csv'
name2 = 'out_0002.csv'
name3 = 'out_0003.csv'
name4 = 'out_0004.csv'
csv_iter = csv.reader(file(name1))
next(csv_iter)

csv_iter2 = csv.reader(file(name2))
next(csv_iter2)

csv_iter3 = csv.reader(file(name3))
next(csv_iter3)

csv_iter4 = csv.reader(file(name4))
next(csv_iter4)

result = []

for row in csv_iter:
    # print len(row)
    for i in range(len(row)):
        if int(row[i]) != 0 and int(row[i]) != 1:
            result.append(int(row[i]))

print len(result)

result2 = []

for row in csv_iter2:
    # print len(row)
    for i in range(len(row)):
        if int(row[i]) != 0 and int(row[i]) != 1:
            result2.append(int(row[i]))


result3 = []

for row in csv_iter3:
    # print len(row)
    for i in range(len(row)):
        if int(row[i]) != 0 and int(row[i]) != 1:
            result3.append(int(row[i]))

print len(result)

result4 = []

for row in csv_iter4:
    # print len(row)
    for i in range(len(row)):
        if int(row[i]) != 0 and int(row[i]) != 1:
            result4.append(int(row[i]))


def histogram(name, result):
    _min = min(result)
    _max = max(result)

    k = 0
    items = []
    for item in result:
        if item not in items:
            items.append(item)
    print items
    k = len(items)

    interval = (_max - _min) / k
    hist_dict = {}
    for i in range(_min, _max+ interval, interval):
        hist_dict[i] = 0
    hist_list = []
    for number in result:
        for i in range(_min, _max+ interval, interval):
            if (number >= (_min + (i - 1) * interval)) and (number <= (_min + i * interval)):
                hist_list.append(i)
                hist_dict[i] += 1
                break
    print hist_dict.items()
    plt.figure(name)
    plt.hist(hist_list, k)
    # plt.show()


histogram(name1, result)
histogram(name2, result2)
histogram(name3, result3)
histogram(name4, result4)
# plt.figure("First")
# plt.plot(1, result)
#
#
# plt.figure("Second")
# plt.plot(1, result2)

plt.show()

