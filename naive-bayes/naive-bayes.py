__author__ = 'RachelSmith'

#!/usr/bin/python

import argparse
import os
import collections
import math
import random


ITERATIONS = 30
LENTESTSET = .3333
stop_words = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also',
             'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be',
             'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear',
             'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for',
             'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers',
             'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is',
             'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may',
             'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor',
             'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our',
             'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since',
             'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then',
             'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas',
             'us', 've', 'wants', 'was', 'we', 'were', 'what', 'when', 'where',
             'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would',
             'yet', 'you', 'your']


def parseArgument():
    """
    Code for parsing arguments
    """
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('-d', nargs=1, required=True)
    args = vars(parser.parse_args())
    return args


def getFileList(directory):
    """
    input: directory
    creates list of files
    that are in the directory
    returns: list of files
    """
    file_list = os.listdir(directory)
    files = []
    for part in file_list:
        if part.endswith('.txt'):
            files.append(part)
    return files


def ridCharsWords(my_list):
    """
    input: list of text
    removes non alpha chars
    and stopwords
    returns: edited list
    """
    edited_list = []
    for part in my_list:
        if part.isalpha() is False or part in stop_words:
            continue
        edited_list.append(part)
    return edited_list


def parseFile(filename):
    """
    input: filename
    retrieve file content
    and put into list
    calls function ridCharsWords()
    returns: list of contents
    """
    input_file = open(filename, 'r')
    text = input_file.read().split(' ')
    input_file.close()
    text = ridCharsWords(text)
    return text


def flattenText(text):
    """
    input: nested list
    flattens text list
    returns: un-nested list
    """
    flat_text = []
    for i in range(len(text)):
        for item in text[i]:
            flat_text.append(item)
    return flat_text


def countWords(text_list):
    """
    input: list of [text]
    creates dict of the form
    word: number of occurrences
    returns: dict
    """
    count = collections.Counter()
    for word in text_list:
        count[word] += 1
    return count


def createTrainTestSets(text_list, len_test):
    """
    input: text list and desired length of test set
    creates random sample from text set
    for the test set
    then uses that set to create training set
    return: test set, training set (in this order)
    """
    test_set = random.sample(text_list, len_test)
    training_set = []
    for text in text_list:
        if text not in test_set:
            training_set.append(text)
    return test_set, training_set


def calcDenominators(text_list, text_list_other):
    """
    input: text_list, other text_list
    calculates denominator for prob dict
    for class of first text list
    returns: denominator
    """
    vocab = countWords(flattenText(text_list+text_list_other))
    word_dict = countWords(flattenText(text_list))
    return sum(word_dict.values()) + len(vocab) + 1


def computeProbsDict(pos_train, neg_train):
    """
    input: positive and negative training sets
    computes prob for each word in training set
    returns: word: prob dict
    """
    pos_dict, neg_dict = countWords(flattenText(pos_train)), \
        countWords(flattenText(neg_train))
    pos_den, neg_den = calcDenominators(pos_train, neg_train), \
        calcDenominators(neg_train, pos_train)
    pos_unk, neg_unk = math.log(float(1)/pos_den), math.log(float(1)/neg_den)
    prob_pos, prob_neg = {'unk': pos_unk}, {'unk': neg_unk}
    for word in pos_dict:
        prob_pos[word] = math.log(float(pos_dict[word] + 1)/pos_den)
    for word in neg_dict:
        prob_neg[word] = math.log(float(neg_dict[word] + 1)/neg_den)
    return prob_pos, prob_neg


def replaceWithFreq(my_dict, text_count):
    """
    input: text list, dict of word probs, dict of word count
    Note: I take out multiplying by the count of the word
    here and just calculate the sum based on presence
    this increases my accuracy by about a percentage point
    returns: list with words replaced with frequencies
    """
    new_text = []
    for word in text_count:
        if word not in my_dict:
            new_text.append(my_dict['unk'])
        else:
            new_text.append(my_dict[word])
    return new_text


def computeProbClass(testing_set, pos_prob, neg_prob, probPos, probNeg):
    """
    input: testing set, pos prob dict, neg prob dict
    sums up probs for each class
    predicts if pos or negative
    returns: list of predicted review classes
    """
    predictions = []
    for text in testing_set:
        textCount = countWords(text)
        sum_pos, sum_neg = math.log(probPos), math.log(probNeg)
        sum_pos += sum(replaceWithFreq(pos_prob, textCount))
        sum_neg += sum(replaceWithFreq(neg_prob, textCount))
        if sum_neg > sum_pos:
            predictions.append('neg')
        else:
            predictions.append('pos')
    return predictions


def printList(my_list):
    """
    input: list
    prints list in specified format
    returns: nothing
    """
    print '\t'+'num_pos_test_docs: '+str(my_list[0])
    print '\t'+'num_pos_training_docs: '+str(my_list[1])
    print '\t'+'num_pos_correct_docs: '+str(my_list[2])
    print '\t'+'num_neg_test_docs: '+str(my_list[3])
    print '\t'+'num_neg_training_docs: '+str(my_list[4])
    print '\t'+'num_neg_correct_docs: '+str(my_list[5])
    accuracy = 100*(my_list[5]+my_list[2])/(my_list[3]+my_list[0])
    print '\t'+'accuracy: '+str(round(accuracy))+'%'


def mainLoop(my_text):
    """
    input: list of text
    creates training set
    runs through steps for predicting
    probabilities
    computes accuracy
    returns: accuracy for loop
    """
    my_train, my_test = {}, {}
    for my_class in ('pos', 'neg'):
        my_test[my_class], my_train[my_class] = createTrainTestSets(
            my_text[my_class], int(LENTESTSET*len(my_text[my_class])))
    pos_prob, neg_prob = computeProbsDict(my_train['pos'], my_train['neg'])
    testing_set = my_test['pos'] + my_test['neg']
    testing_set = random.sample(testing_set, len(testing_set))
    probOfPos, probOfNeg = len(my_test['pos'])/float(len(testing_set)),\
        len(my_test['neg'])/float(len(testing_set))
    predicts = computeProbClass(testing_set, pos_prob, neg_prob, probOfPos, probOfNeg)
    right_pos, right_neg = 0, 0
    for i in range(len(predicts)):
        if predicts[i] == 'pos' and testing_set[i] in my_test['pos']:
            right_pos += 1
        elif predicts[i] == 'neg' and testing_set[i] in my_test['neg']:
            right_neg += 1
    info_list = [len(my_test['pos']), len(my_train['pos']), right_pos,
                 len(my_test['neg']), len(my_train['neg']), right_neg]
    printList(info_list)
    return 100*(right_neg+right_pos)/len(predicts)


def main():
    """
    input: none
    calls functions to parse text
    runs through loop to classify docs
    prints final avg accuracy
    returns: nothing
    """
    args = parseArgument()
    directory = args['d'][0]
    my_text = {}
    for my_class in ('pos', 'neg'):
        new_dir = os.path.join(directory, my_class)
        files, text = getFileList(new_dir), []
        for my_file in files:
            text.append(parseFile(new_dir+'/'+my_file))
        my_text[my_class] = text
    accuracies = []
    for i in range(ITERATIONS):
        print 'Iteration: '+str(i+1)
        accuracies.append(mainLoop(my_text))
    average = float(sum(accuracies))/len(accuracies)
    print '\n'+'\t'+'avg_accuracy: '+str(round(average, 1))+'%'

main()
