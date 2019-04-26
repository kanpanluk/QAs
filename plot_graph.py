import matplotlib.pyplot as plt
import os
from pprint import pprint
import json
import random
import numpy as np

def similar(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio()


def plotAccuracy(file, label):
    for f in file:

        data = open('result\\old_result\\' + f, 'r', encoding='utf-8-sig')

        a = []
        topN = []
        for i in data:
            i = i.replace('cant find in best tf-idf', 'ct')
            i = i.replace('cant find in shortest', 'cs')
            i = i.replace('Cant find doc', 'cd')
            a.append(i.split())

            try:
                topN.append(a[-1][3])
            except IndexError:
                print(a[-1])
                exit(0)
        if (topN.__len__() < 4000):
            continue
        for i in range(a.__len__()):
            try:
                topN[i] = int(topN[i].split('rank')[1])
            except IndexError:
                topN[i] = 1000000

        rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 50]
        acc = []
        for n in rank:
            acc.append(0)
            for i in topN:
                if i < n:
                    acc[-1] += 1
            acc[-1] = acc[-1] / topN.__len__()
            # print(n, acc[-1])

        plt.xlabel('Rank N', size=25)
        plt.ylabel('Accuracy', size=25)
        plt.title('Accuracy in N rank', size=25)

        plt.plot(rank, acc, marker='o', label=label)
        plt.legend(loc='upper right')

    plt.tick_params(axis='x', labelsize=20)
    plt.tick_params(axis='y', labelsize=20)
    plt.grid(axis='y', )


def plotAccuracy_withList(topN, label):
    rank = np.arange(12)
    acc = []
    for n in rank:
        acc.append(0)
        for i in topN:
            if i < n:
                acc[-1] += 1
        acc[-1] = acc[-1] / 4000
        # print(n, acc[-1])

    plt.xlabel('Rank N', size=25)
    plt.ylabel('Accuracy', size=25)
    plt.title('Accuracy in N rank', size=25)

    plt.plot(rank, acc, marker='o', label=label)
    plt.legend(loc='upper right')

    plt.tick_params(axis='x', labelsize=20)
    plt.tick_params(axis='y', labelsize=20)
    plt.grid(axis='y')
    plt.grid(axis='x')

def plot_histogram(file, n, color):
    data = open('result\\' + file, 'r', encoding='utf-8-sig')

    l = []
    for i in data:
        tmp = i.split(']]')[-1].split()
        print(tmp)
        for j in range(tmp.__len__()):
            if tmp[j].isnumeric():
                try:
                    l.append(int(tmp[j + n]))
                    break
                except ValueError:
                    l.append(0)
                    break

    plt.tick_params(axis='x', labelsize=20)
    plt.tick_params(axis='y', labelsize=20)
    plt.hist(l, 50, color=color)
    plt.grid(axis='y', )
    plt.xlabel('Length of list', size=25)
    plt.ylabel('Number of list', size=25)
    plt.title('Histogram of shortest list', size=25)
    plt.show()


def modify_data_for_histogram(data):
    for i in range(data.__len__()):
        if data[i]>=10000:
            data[i] = -5
        else:
            data[i] += 1
    return data

def plot_histogram_with_list(data, label):
    # This is  the colormap I'd like to use.
    cm = plt.cm.get_cmap('RdYlBu_r')
    data = modify_data_for_histogram(data)

    # Plot histogram.
    n, bins, patches = plt.hist(data, max(data),alpha=0.5,label=label)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    # scale values to interval [0,1]
    col = bin_centers - min(bin_centers)
    col /= max(col)

    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))

    # plt.hist(data, max(data), color=color, alpha=0.5, label=label)

    plt.legend(loc='upper right')
    plt.tick_params(axis='x', labelsize=10)
    plt.tick_params(axis='y', labelsize=10)
    plt.grid(axis='y', )
    plt.xlabel('Similarity Score', size=15)
    plt.ylabel('Number of Answer', size=15)
    plt.title('Histogram of Similarity', size=15)

    plt.show()


def accuracy_from_doc_candidate(doc, validate):
    acc = []
    out_of_range = 0
    for i in range(doc.__len__()):
        try:
            # print(i,test_output[i].index(str(validate[i])))
            acc.append(doc[i].index(str(validate[i])))
        except ValueError:
            # print(i,''.join(q[i]))
            out_of_range += 1
            # print(q[i])
    print("OUT:", out_of_range)
    return acc

def plot_doc_candidate():
    color = []
    r = lambda: random.randint(0, 255)
    color.append('#%02X%02X%02X' % (r(), r(), r()))

    validate = json.load(open("test_set\\new_sample_questions_answer.json", mode='r', encoding="utf-8-sig"))
    q = json.load(open('test_set\\new_sample_questions_tokenize.json', mode='r', encoding="utf-8-sig"))

    plotAccuracy(['result_q_weight5_fill_c[0](BEST).txt'], "old-db")  ###

    path = 'document_candidate\\'
    file = os.listdir(path)
    print(file)

    for f in file:
        test_output = json.load(open(path + f, 'r', encoding='utf-8'))
        acc = accuracy_from_doc_candidate(test_output, validate)
        plotAccuracy_withList(acc, f.replace('.json', ''))

    plt.grid(axis='y')
    plt.grid(axis='x')
    plt.show()

def sentence_acc(sentence_candidate, validate_sentences):
    for j in range(sentence_candidate.__len__()):
        for k in validate_sentences:
            if sentence_candidate[j][-1] == k:
                return j
    return 10000
def accuracy_from_sen_candidate(sentence_candidate,validate_sentences):
    acc = []
    for i in range(validate_sentences.__len__()):
        acc.append(sentence_acc(sentence_candidate[i], validate_sentences[i]))

    return acc

def plot_sen_candidate():
    validate = json.load(open("test_set\\validate_sentences.json", mode='r', encoding="utf-8-sig"))

    color = []
    r = lambda: random.randint(0, 255)
    color.append('#%02X%02X%02X' % (r(), r(), r()))

    path = 'sentence_candidate\\'
    file = os.listdir(path)
    print(file)

    for f in file:
        sentence_candidate = json.load(open(path + f, 'r', encoding='utf-8'))
        acc = accuracy_from_sen_candidate(sentence_candidate, validate)
        # plotAccuracy_withList(acc, f.replace('.json', ''))
        plot_histogram_with_list(acc, f.replace('.json', ''))
    plt.show()

# plot_doc_candidate()
plot_sen_candidate()