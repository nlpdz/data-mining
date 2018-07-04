#!/usr/bin/python
# coding=utf-8
# 采用TextRank方法提取文本关键词
import sys
import pandas as pd
import jieba.analyse
import jieba
"""
       TextRank权重：

            1、将待抽取关键词的文本进行分词、去停用词、筛选词性
            2、以固定窗口大小(默认为5，通过span属性调整)，词之间的共现关系，构建图
            3、计算图中节点的PageRank，注意是无向带权图
"""

# 处理标题和摘要，提取关键词
# def getKeywords_textrank(data,topK):
#     idList,titleList,abstractList = data['id'],data['title'],data['abstract']
#     ids, titles, keys = [], [], []
#     for index in range(len(idList)):
#         text = '%s。%s' % (titleList[index], abstractList[index]) # 拼接标题和摘要
#         jieba.analyse.set_stop_words("data/stopWord.txt") # 加载自定义停用词表
#         print "\"",titleList[index],"\"" , " 10 Keywords - TextRank :"
#         keywords = jieba.analyse.textrank(text, topK=topK, allowPOS=('n','nz','v','vd','vn','l','a','d'))  # TextRank关键词提取，词性筛选
#         word_split = " ".join(keywords)
#         print word_split
#         keys.append(word_split.encode("utf-8"))
#         ids.append(idList[index])
#         titles.append(titleList[index])
#
#     result = pd.DataFrame({"id": ids, "title": titles, "key": keys}, columns=['id', 'title', 'key'])
#     return result

def main():
    dataFile = 'data_valid1.txt'
    stop_words = []
    with open("stopWord.txt", 'r', encoding='utf-8') as fff:
        for line in fff:
            stop_words.append(line.strip())
    with open(dataFile, 'r', encoding='utf-8') as f:
        for line in f:
            text = line.split(":")[1]
            text = text.replace('\n', '')

            print(text)
            # jieba.analyse.set_stop_words("stopWord.txt")
            keywords = jieba.cut(text, cut_all=False)

            tokens=" ".join(keyword for keyword in keywords if keyword not in stop_words)
            print(tokens)

            with open('input1.txt', 'a', encoding='utf-8') as ff:
                ff.write(tokens + '\n')

if __name__ == '__main__':
    main()


