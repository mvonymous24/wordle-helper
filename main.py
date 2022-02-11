import collections
import os
import re
import sys
import json


weight = (7, 3)  # 字母频率与词汇频率占权重比值


def analysis_merge(a, b):
    c = b.copy()
    for i in a:
        if i in c:
            c[i] += a[i]
        else:
            c[i] = a[i]
    return c


def analysis_sum(a):
    sum = 0
    for i in a.keys():
        sum += a[i]
    return sum


def progress(name, now, all):
    #  os.system('clear')
    sys.stdout.flush()
    sys.stdout.write(
        '%s %s%s %s \n' % (name, '#' * int(now / all * 10), '.' * int(10 * (1 - now / all)), int(now / all * 100)))


def get_dataset():
    # data is from https://figshare.com/articles/dataset/txtlab_Novel450/2062002/1 and is under the licence CC-BY 4.0
    # this function will get all the texts in the folder dataset, analyse them and sum up the dictionary result.
    datasetFolder = os.listdir('dataset')
    dictResult = []
    counter = 0
    for i in datasetFolder:
        progress('getDataset.read', counter, len(datasetFolder))
        counter += 1
        dictResult.append(analyse_word_frequency(read('dataset/' + i)))
    dict = {}
    counter = 0
    for i in dictResult:
        progress('getDataset.merge', counter, len(dictResult))
        counter += 1
        dict = analysis_merge(dict, i)
    return dict


def read(path, type='text'):
    if type == 'text':
        with open(path, encoding='utf-8') as q:
            return q.read()
    else:
        with open(path, 'w') as file:
            return json.load(fp=file)


def analyse_word_frequency(text):
    split = re.split(r'\W\s*\.*', text.lower())  # 此处进行了全小写转换
    analysisResult = collections.Counter(split)
    analysisResult.pop('')
    analysisResultRemoval = analysisResult.copy()  # 字典深复制和浅复制
    for i in analysisResult:
        if re.fullmatch(r'[a-z]{5}', i) is None:  # or i.isalpha() is False :
            analysisResultRemoval.pop(i)
    return analysisResultRemoval


def initialization(reload=False):
    rereload = False
    # readCsv = pd.read_csv('analysis.csv', encoding='utf-8', index_col=0)
    if os.path.isfile('analysis.json'):
        with open('analysis.json', 'r') as file:
            readCsv = json.load(fp=file)
    else:
        rereload = True
    if reload or rereload:
        dataset = get_dataset()
        # print(dataset['happy'])
        # datasetpd = pd.DataFrame(dataset, index=[0])
        # datasetpd.to_csv('analysis.csv', encoding='utf-8')
        with open('analysis.json', 'w') as file:
            json.dump(dataset, file)
        return initialization()
    else:
        return readCsv


def analyse_letter_frequency(wordFrequencyDataset):
    keys = wordFrequencyDataset.keys()
    dict1, dict2, dict3, dict4, dict5 = {}, {}, {}, {}, {}
    for i in keys:
        if len(i) != 5:
            continue
        # print(i)
        l1, l2, l3, l4, l5 = (j for j in i)
        dict1 = analysis_merge(dict1, {l1: 1})
        dict2 = analysis_merge(dict2, {l2: 1})
        dict3 = analysis_merge(dict3, {l3: 1})
        dict4 = analysis_merge(dict4, {l4: 1})
        dict5 = analysis_merge(dict5, {l5: 1})
    return dict1, dict2, dict3, dict4, dict5  # 每个dict都是每个字母位置上的字母频次


def generate_base(letterFrequency, wordFrequencyDataset):
    # 计算sum of every letter
    letterSum = {}
    for i in range(5):
        letterSum[i] = analysis_sum(letterFrequency[i])
    letterFrequencyBase = {i: letterFrequency[i] for i in range(5)}  # 元组不可变
    for i in letterFrequencyBase:
        for j in letterFrequencyBase[i]:
            letterFrequencyBase[i][j] *= 10000
            letterFrequencyBase[i][j] /= letterSum[i]
            letterFrequencyBase[i][j] = int(letterFrequencyBase[i][j])

    # 评估词汇权重
    base = wordFrequencyDataset.copy()
    for i in wordFrequencyDataset.keys():
        if len(i) != 5:
            continue
        # print(i)
        # letterList = (j for j in i)
        sumWeight = 0
        for j in range(5):
            sumWeight += letterFrequencyBase[j][i[j]]
        base[i] = sumWeight

    # 叠加日常词频
    wordFrequencyBase = wordFrequencyDataset.copy()
    wordFrequencysum = analysis_sum(wordFrequencyBase)
    for i in base.keys():
        if i in wordFrequencyBase.keys():
            wordFrequencyBase[i] = wordFrequencyBase[i] * 10000 / wordFrequencysum
        else:
            wordFrequencyBase[i] = 0
        base[i] = base[i] * weight[0] / sum(weight) + wordFrequencyBase[i] * weight[1] / sum(weight)

    return base


def sort(dict_of_words):
    return sorted(dict_of_words.items(), key=lambda x: x[1], reverse=True)  # 返回一个list


def funnel(input_word, words_to_check, color):
    # gray, yellow, green = 1 2 3
    # green
    green = {}
    for i in range(5):
        if color[i] == '3':
            green[i] = input_word[i]
    # print('green = ', green)
    words_to_check_green = funnel_green(green, words_to_check)

    # gray
    gray = {}
    for i in range(5):
        if color[i] == '1':
            gray[i] = input_word[i]
    # print('gray = ', gray)

    # yellow
    yellow = {}
    for i in range(5):
        if color[i] == '2':
            yellow[i] = input_word[i]
    # print('yellow = ', yellow)

    words_to_check_green_gray = funnel_gray(gray, green, yellow, words_to_check_green)
    words_to_check_green_gray_yellow = funnel_yellow(yellow, green, words_to_check_green_gray)
    return words_to_check_green_gray_yellow


def funnel_yellow(yellow, green, words):
    if yellow:
        yellow_reverse = {}
        for i in yellow:
            if yellow[i] in yellow_reverse:
                yellow_reverse[yellow[i]].append(i)
            else:
                yellow_reverse[yellow[i]] = [i]
        # print('yellow_reverse = ', yellow_reverse)
        exception = yellow_reverse.copy()
        for i in green:
            if green[i] in exception:
                exception[green[i]].append(i)
            else:
                exception[green[i]] = [i]
        # print('exception = ', exception)
        words_output = {}  # 只有满足条件（黄色字母在非绿非自身位置(exception外的位置)出现指定次数(yellow_reverse中的次数)）才会被加入这个字典

        for word_checking in words:
            standard_met = True
            for i in yellow_reverse:
                appear_times = len(yellow_reverse[i])
                counter = 0
                for j in range(5):
                    if word_checking[j] == i and (j not in exception[i]):
                        counter += 1
                # print(i, ' ', appear_times, ' ', counter)
                if counter != appear_times:
                    standard_met = False
                    break
            if standard_met:
                words_output[word_checking] = words[word_checking]

        return words_output
    else:
        return words


def get_yellow_reverse(yellow):
    yellow_reverse = {}
    for i in yellow.keys():
        if yellow[i] in yellow_reverse:
            yellow_reverse[yellow[i]].append(i)
        else:
            yellow_reverse[yellow[i]] = [i]
    return yellow_reverse


def funnel_gray(gray, green, yellow, words):
    if gray:
        # 倒置灰黄色块数据储存方式
        gray_reverse = {}
        for i in gray.keys():
            if gray[i] in gray_reverse:
                gray_reverse[gray[i]].append(i)
            else:
                gray_reverse[gray[i]] = [i]
        yellow_reverse = {}
        for i in yellow.keys():
            if yellow[i] in yellow_reverse:
                yellow_reverse[yellow[i]].append(i)
            else:
                yellow_reverse[yellow[i]] = [i]

        # 遍历单词
        words_output = {}
        for enumerated_word in words.keys():
            repulsion_requirements = True
            yellow_num_requirements = True
            for gray_position in gray:
                yellow_reverse = get_yellow_reverse(yellow)
                if gray[gray_position] in yellow_reverse:
                    check_repulsion_list = yellow_reverse[gray[gray_position]]
                else:
                    check_repulsion_list = []
                if gray[gray_position] in yellow_reverse:
                    yellow_num = len(yellow_reverse[gray[gray_position]])
                    check_existence_place = []
                    for i in range(5):
                        if i not in green and i not in yellow_reverse[gray[gray_position]] and i != gray_position:
                            check_existence_place.append(i)
                        for gray_letter_place in gray_reverse[gray[gray_position]]:
                            if gray_letter_place not in check_repulsion_list:
                                check_repulsion_list.append(gray_letter_place)
                else:
                    yellow_num = 0
                    check_existence_place = []
                    for i in range(5):
                        if i not in green and i != gray_position:
                            check_existence_place.append(i)
                        # check_repulsion_list = yellow_reverse[gray[gray_position]]
                        for gray_letter_place in gray_reverse[gray[gray_position]]:
                            if gray_letter_place not in check_repulsion_list:
                                check_repulsion_list.append(gray_letter_place)
                # 计数：非绿非自身灰块非黄同字母区域的该字母个数是否等于黄色色块个数
                # if enumerated_word == 'ceres':
                    # print(yellow_reverse)
                    # print('letter is ', gray[gray_position],', ceres yellow num = ', yellow_num, ' and repulsion is ', check_repulsion_list, ' exsitence check is ', check_existence_place)
                for checking_place in check_existence_place:
                    if enumerated_word[checking_place] is gray[gray_position]:
                        yellow_num -= 1
                for repulsion_place in check_repulsion_list:
                    if enumerated_word[repulsion_place] is gray[gray_position]:
                        repulsion_requirements = False
                if yellow_num != 0:
                    yellow_num_requirements = False
            if yellow_num_requirements and repulsion_requirements:
                words_output[enumerated_word] = words[enumerated_word]

        return words_output
    else:
        return words


def funnel_green(green, words):
    if green:
        words_output = words.copy()
        for i in words.keys():
            for j in green.keys():
                if i[j] != green[j]:
                    words_output.pop(i)
                    break
        return words_output
    else:
        return words


def color_translator(text):
    color_elements = ['1', '2', '3']  # 灰 黄 绿
    need_translator = False
    if os.path.isfile('color_code_override.txt'):
        with open('color_code_override.txt', 'r') as file:
            color_code_override = file.read()
        need_translator = True
        color_elements = [color_code_override[0], color_code_override[1], color_code_override[2]]
    for letter in text:
        if letter not in color_elements:
            print('Color code error: the input contains letters that cannot be identified.')
            return 'error'
    if need_translator:
        text = text.replace(color_elements[0], '1')
        text = text.replace(color_elements[1], '2')
        text = text.replace(color_elements[2], '3')
    return text


def getInput(tip, type):
    input_text = input(tip)
    if type == 'inputword':
        if input_text == '':
            return '1'
        return input_text
    elif type == 'color':
        if len(input_text) == 5:
            color_get = color_translator(input_text)
            if color_get != 'error':
                return color_get
            else:
                getInput(tip, type)
        else:
            if input_text == 'x':
                return 'go_back'
            else:
                print('Wrong input format. The default format is a 5-letter string consists of \'1\', \'2\' and \'3\'.'
                      '\'1\' stands for gray, \'2\' stands for yellow, and \'3\' stands for green.')
                return getInput(tip, type)


def topN(sorted_list, n=5):
    if len(sorted_list) > n:
        listN = sorted_list[:n]
    else:
        listN = sorted_list
    text = ''
    listNum = 0
    for listWord in listN:
        listNum += 1
        text = text + str(listNum) + '. ' + listWord[0] + '\n'

    return listN, text


# 下一步是统计所有单词，根据其单词中的字母搜索字母频次获得每个单词的权重，生成base权重字典

# 字母颜色硬筛选，按字母出现频次+词汇整体语境出现频次（标准化后以较小的权重）叠加形成base排序建议


if os.path.isfile('dataset_override'):
    os.remove('dataset_override')
    wordFrequencyDataset = initialization(True)
else:
    wordFrequencyDataset = initialization()  # json，里面是按纯按日用词频的统计数据
base = generate_base(letterFrequency=analyse_letter_frequency(wordFrequencyDataset)
                     , wordFrequencyDataset=wordFrequencyDataset)

# gray, yellow, green = 1 2 3
unsortedList = base
sortList = sort(base)
topList, topTipText = topN(sortList)
times = 0
while True:
    print('There are ', len(sortList), ' word(s) left in the dictionary. Here are the most recommended ',
          len(topList), ' word(s). Choose one and input it into Wordle: \n', topTipText, sep='')
    if len(sortList) == 1:
        print('Only one word left. Please input it into Wordle.')
    if len(sortList) == 0:
        print('None of the words in the dictionary meets the requirements. Please try:'
              '\n1. restart the program to see if there\'s a wrong input.'
              '\n2. Customize the dictionary.')
        break
    numberOfWord = int(getInput('Select the word you have just input into Wordle. '
                                'If you select nothing, the first word will be chosen. '
                                '\n[Input]The number is: ', type='inputword'))
    color = getInput('input the word into Wordle, and tell me the colors. '
                     'If you chose a wrong word in the last step, just input \'x\' to go back.'
                     '\n[Input]The color is: ', type='color')
    if color == '33333':
        print('\nToday\'s Wordle completed. Congrats!')
        break
    if color == 'go_back' or color == 'x':
        continue
    if color is None:
        print('\nGetting color failed. Please try again.')
        continue
    unsortedList = funnel(topList[numberOfWord - 1][0], unsortedList, color)
    sortList = sort(unsortedList)
    topList, topTipText = topN(sortList)
    times += 1
    if times == 6:
        print('Today\'s Wordle is incomplete. Maybe you wanna see what\'s still in the dictionary:\n', topList)
        break

print('[press enter to exit]')
input('')