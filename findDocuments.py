# coding=utf8

import json
# import deepcut
import time
from heapq import nlargest
from sqlitedict import SqliteDict
from pythainlp.corpus import wordnet , stopwords
from usage import alarm , rreplace

# initial databased
start = time.time()
dict = SqliteDict('E:\CPE#Y4\databaseTF\lastest_db\doc_add_missing.sqlite', autocommit=True)
dict = dict['doc']
end = time.time()
print("Time to initial db", end - start)
# initial data and test set
q = open("test_set\\new_sample_questions_tokenize.json", mode='r', encoding="utf-8-sig")
n_q = open("no_stop_words_questions_.json", mode='r', encoding="utf-8-sig")
data = json.load(q)
validate = json.load(open("test_set\\new_sample_questions_answer.json", mode='r', encoding="utf-8-sig"))

doc = 0
data = data[doc:]
print(data.__len__())
save = 0
string = ''
question_words = stopwords.words('thai')
question_words.append('กี่')
question_words.append('ใด')

for s in data:
    start = time.time()
    string += "question " + str(doc)
    print("question", doc, s, validate[doc])

    # segment until no space and do rule-based
    r = []
    for i in s:
        if ' ' in i:
            for j in i.split():
                s.append(j)
        elif i.endswith('คือ'):
            r.append(i)
            s.append(rreplace(i,'คือ','',1))
    for i in r:
        s.remove(i)

    ########################################################################################

    s.sort()
    s = list(set(s))
    search = []
    cantfind = []

    # # find by sqlitedict

    for f in range(s.__len__()):
        if (s[f].isspace()) or (s[f] in question_words):
            continue
        if (s[f][0] == ' ') or (s[f][-1] == ' '):
            s[f] = s[f].strip()

        try:
            tmp = dict[s[f][0]][s[f]]
            search.append((s[f], tmp))

        except KeyError:  # # if no index find by synonyms
            cantfind.append(s[f])
            synonyms = []
            for syn in wordnet.synsets(s[f]):
                for i in syn.lemma_names('tha'):
                    synonyms.append(i)

            # if synonyms.__len__() == 0 :
            #     synonyms = deepcut.tokenize(s[f])
            if s[f] in synonyms :
                synonyms.remove(s[f])
            for i in synonyms:
                try:
                    tmp = dict[i[0]][i]
                    search.append((i, tmp))
                    break
                except KeyError:
                    cantfind.append(i)

    ########################################################################################

    # remove least mean tf-idf
    word = []
    pool = []
    search.sort(key=lambda s: s[1][0][0], reverse=True)
    for i in range(0):
        if (search.__len__() > 2):
            search.pop()
        else:
            break

    search.sort(key=lambda s: len(s[1]))
    for i in range(search.__len__()):
        try:
            word.append(search[i][0])
            pool.append(search[i][1][1:])
        except IndexError:
            break
    # weight shortest in case shortest + best tf-idf
    # for i in range(pool[0].__len__()):
    #     pool[0][i][1] *= 3

    ########################################################################################

    answer_index = []
    count = []

    # rank answer in answer pool
    c = {}
    weight = [5,1]
    for i in range(pool.__len__()):
        for k, v in pool[i]:
            try:
                if i < weight.__len__():
                    c[k] += v*weight[i]
                else:
                    c[k] += v
            except KeyError:
                if i < weight.__len__():
                    c[k] = v*weight[i]


    for key, value in c.items():
        answer_index.append(key)
        count.append(value)

    ########################################################################################
    answer_n = nlargest(count.__len__(), count)
    answer = []
    for i in answer_n:
        index = count.index(i)
        answer.append(answer_index[index])
        answer_index.pop(index)
        count.pop(index)

    print(answer.__len__(), answer[:6])

    # write in text file
    answer = list(answer)
    ans_int = ''
    find = []
    for i in range(pool.__len__()):
        find.append([])
        for j in pool[i]:
            find[-1].append(j[0])
        try:
            find[i].index(str(validate[doc]))
        except ValueError:
            ans_int += ' c[' + str(i) + '] '

    ########################################################################################

    try:
        if answer.index(str(validate[doc])) < 6:
            string += ': 1'
        else:
            string += ': 0'
        string += " rank" + str(answer.index(str(validate[doc])))
    except ValueError:
        string += ": 0 cdoc"

    string += ' || [' + str(word) + ']' + ans_int
    for i in range(find.__len__()):
        string += str(find[i].__len__()) + ' '
    string += str(cantfind)

    end = time.time()
    print(end - start, 'secs')
    string += ' ' + str(end - start) + 'secs \n'
    doc += 1
    save += 1
    if save == 100 or doc == 4000:
        with open("result/result_q_weight5_cut_suffix.txt", "a", encoding="utf-8") as text_file:
            text_file.write(string)
        save = 0
        string = ''
    if doc == 4000:
        break
alarm()
# os.system("shutdown /s /t 30")
