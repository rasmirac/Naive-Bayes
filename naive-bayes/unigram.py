#!/usr/bin/python

import argparse
import os
import collections
import csv
from operator import itemgetter


# Stop word list
stopWords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also',
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
             'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us',
             've', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
             'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet',
             'you', 'your']


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
    myFileList = os.listdir(directory)
    files = []
    for myFile in myFileList:
        if myFile.endswith('.txt'):
            files.append(myFile)
    return files


def ridCharsWords(myList):
    """
    input: list of text
    removes non alpha chars
    and stopwords
    returns: edited list
    """
    myEditedList = []
    for x in myList:
        if x.isalpha() is False or x in stopWords:
            continue
        myEditedList.append(x)
    return myEditedList


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
    flattenedText = []
    for i in range(len(text)):
        for item in text[i]:
            flattenedText.append(item)
    return flattenedText


def countWords(textList):
    """
    input: list of [text]
    creates dict of the form
    word: number of occurrences
    returns: dict
    """
    count = collections.Counter()
    for word in textList:
        count[word] += 1
    return count


def createList(wordsDict):
    """
    input: dictionary
    crates list in form
    [class, word, count, probability]
    sorts the list by probability
    returns: list
    """
    probList = [['class', 'word', 'count', 'probability']]
    for key in wordsDict.keys():
        mySum = sum(wordsDict[key].values())
        for word in wordsDict[key].keys():
            probList.append([key, word, wordsDict[key][word], float(wordsDict[key][word])/mySum])
    probList = sorted(probList, key=itemgetter(3), reverse=True)
    return probList


def writeOutput(myList):
    """
    input: list
    writes csv file
    returns: nothing
    """
    with open('movie_unigram.csv', 'wb') as test_file:
        file_writer = csv.writer(test_file)
        for line in myList:
            file_writer.writerow(line)


def main():
    """
    input: none
    loops through 'pos' and
    'neg' directory to create
    dict with word count for each
    word in corresponding text
    calls function to write .csv
    returns: nothing
    """
    args = parseArgument()
    directory = args['d'][0]
    words_dic = {}
    for myClass in ('pos', 'neg'):
        files = getFileList(myClass)
        myText = []
        for myFile in files:
            myText.append(parseFile(directory+myClass+'/'+myFile))
        myText = flattenText(myText)
        words_dic[myClass] = countWords(myText)
    myList = createList(words_dic)
    writeOutput(myList)

main()
