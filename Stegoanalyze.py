import sys
import random as rnd
import cv2
import binascii
import matplotlib.pyplot as plt
import numpy as np
from math import log10
import collections
# from tabulate import tabulate


def process_all_images():
    names_parrot_bmp = ["0001.jpg", "0002.jpg"]
    names_yacht_bmp = ["0003.jpg", "0004.jpg"]
    names_city_bmp = ["0005.bmp", "0006.bmp"]
    names_lenag_bmp = ["0007.bmp", "0008.bmp"]
    names_lily_bmp = ["0009.bmp", "0010.bmp"]
    names_forest_jpg = ["image_002.jpg", "image_003.jpg", "image_004.jpg", "image_005.jpg", "image_006.jpg","image_007.jpg"]
    names_lenac_bmp = ["Lena_1.jpg", "Lena_2.jpg"]
    names_sailboard_bmp = ["sailboat_at_anchor_1.jpg", "sailboat_at_anchor_2.jpg"]
    names = {1: names_parrot_bmp, 2: names_yacht_bmp, 3: names_city_bmp, 4: names_lenag_bmp, 5: names_lily_bmp} #,
             # 6: names_forest_jpg, 7: names_lenac_bmp, 8: names_sailboard_bmp}
    analyze(names)
    print "\nend"


def analyze(names):
    # imgs = []
    # for name in names_bmp:
    # 	imgs.append(cv2.imread(name))

    # results = []
    # for img in imgs:
    # 	results.append(analize_seq3_repeating(img))
    # add_hist(results)
    # plt.show()

    for item in names.keys():
        results = {}
        for name in names[item]:
            img = cv2.imread(name)
            results[name] = analyze_seq3_repeating(img)
        # imgs.append(cv2.imread(name))

        # for img in imgs:
        # 	results.append(analize_seq3_repeating(img))results.keys()
        if len(results) < 4:
            add_hist(results, item)
        else:
            add_plot(results, item)
    plt.show()


def analyze_jpeg(names_jpeg):
    results = {}
    for name in names_jpeg:
        img = cv2.imread(name, 0)
    # cv2.imshow("img",img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# For BMP files
def analyze_seq3_repeating(img):
    print "-----IMG-----"
    y = 0
    res = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0, "111": 0}
    height, width, depth = img.shape
    while y < height:
        x = 0
        while x < width:
            # r = img[y][x][0]
            # g = img[y][x][1]
            b = bin(img[y][x][2])[2:].zfill(8)
            res[b[5:]] += 1
            # print b[5:], int(b, 2)
            x += 1
        y += 1
    print(res)
    return res


def add_hist(results, item):
    my_colors = 'bcmyckrg'
    # for (i,res) in enumerate(results):
    # 	# print res.keys
    # 	indexes = np.arange(0,len(res),1)
    # 	width = 0.3
    # 	step = 0.05
    # 	plt.figure(1)
    # 	plt.title('Hist of bits sequences')
    # 	plt.xticks(indexes+i*(width+step/2), res.keys())
    # 	# col = rnd.randint(0,len(my_colors)-1)
    # 	plt.legend((rects1[0], rects2[0]), (, 'Theoretical') )
    # 	plt.bar(indexes+i*(width+step), res.values(), width, color=my_colors[i])
    rects = []
    for (i, key) in enumerate(results.keys()):
        # print res.keys
        res = results[key]
        indexes = np.arange(0, len(res), 1)
        step = 0.05
        width = float(1) / len(results) - step
        print width, 1 % len(results), 1 / len(results), float(20) / 3

        plt.figure(item)
        plt.subplot(111)
        plt.title('Hist of bits sequences')
        plt.xticks(indexes + i * (width + step / 2), res.keys())
        # col = rnd.randint(0,len(my_colors)-1)
        rect = plt.bar(indexes + i * (width + step), res.values(), width, color=my_colors[i % len(my_colors)])
        rects.append(rect)

    plt.legend((rects), (results.keys()), loc='center left', bbox_to_anchor=(1, 0.5))


def add_plot(results, item):
    rects = []
    for (i, key) in enumerate(results.keys()):
        # print res.keys
        res = results[key]
        indexes = np.arange(0, len(res), 1)
        step = 0.05
        width = float(1) / len(results) - step
        # print width, 1%len(results),1/len(results), float(20)/3

        plt.figure(item)
        plt.subplot(111)
        # plt.title('Hist of bits sequences')
        plt.xticks(indexes, res.keys())
        # # col = rnd.randint(0,len(my_colors)-1)
        # rect = plt.bar(indexes+i*(width+step), res.values(), width, color=my_colors[i%len(my_colors)])
        plt.plot(indexes, res.values(), label=key)
        # rects.append(rect)

        # plt.legend((rects), (results.keys()),loc='center left', bbox_to_anchor=(1, 0.5))
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


process_all_images()
# imgs = []
# imgs.append(cv2.imread(names_bmp[0]))
# imgs.append(cv2.imread(names_bmp[1]))
# heights = []
# widths = []
# depth = []
# height[0], width[0], depth[0] = imgs[0].shape
# height[1], width[1], depth[1] = imgs[1].shape
# analyze(names_jpeg)
# analyze_jpeg(["0001.jpg", "0002.jpg"])
