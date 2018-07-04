# encoding:utf-8
import jieba
import logging
import codecs
import traceback
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from collections import Counter


class TextCluster(object):
    # 初始化函数,重写父类函数
    def __init__(self):
        pass
    def seg_words(self, sentence):
        seg_list = jieba.cut(sentence)  # 默认是精确模式
        return " ".join(seg_list)       # 分词，然后将结果列表形式转换为字符串
    # 加载用户词典
    def load_userdictfile(self, dict_file):
        jieba.load_userdict(dict_file)
    def load_processfile(self, process_file):
        corpus_list = []
        try:
            fp = open(process_file, "r", encoding="utf-8")
            for line in fp:
                conline = line.strip()
                corpus_list.append(conline)
            return True, corpus_list
        except:
            logging.error(traceback.format_exc())
            return False, "get process file fail"
    def output_file(self, out_file, item):
        try:
            fw = open(out_file, "a")
            fw.write('%s' % (item.encode("utf-8")))
            fw.close()
        except:
            logging.error(traceback.format_exc())
            return False, "out file fail"
    # 释放内存资源
    def __del__(self):
        pass
    def process(self, process_file, tf_ResFileName, tfidf_ResFileName, num_clusters):
        try:
            flag, lines = self.load_processfile(process_file)  # 读文件
            if flag == False:
                logging.error("load error")
                return False, "load error"
            tf_vectorizer = CountVectorizer(min_df=1, max_df=1.0, token_pattern='\\b\\w+\\b')
            # fit_transform是将文本转为词频矩阵
            tf_matrix = tf_vectorizer.fit_transform(lines)
            tf_weight = tf_matrix.toarray()
            print("tf统计完毕")
            #print (tf_weight)
            # 该类会统计每个词语的tf-idf权值
            tfidf_transformer = TfidfTransformer()
            # fit_transform是计算tf-idf
            tfidf_matrix = tfidf_transformer.fit_transform(tf_matrix)
            # 获取词袋模型中的所有词语
            word_list = tf_vectorizer.get_feature_names()
            # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
            tfidf_weight = tfidf_matrix.toarray()
            print("idf统计完毕")
            # 聚类分析
            print("聚类开始")
            km = KMeans(n_clusters=num_clusters)
            km.fit(tfidf_matrix)
            print(Counter(km.labels_))  # 打印每个类多少人
            # 每个样本所属的簇
            clusterRes = codecs.open("D:/vain/data_mining_workspace/cluster_Result.txt", 'w', 'utf-8')
            for count in range(1613):
                label=km.labels_[count]
                clusterRes.write(str(lines[count]) + '\t' + str(label))
                clusterRes.write('\r\n')
            clusterRes.close()
            print("聚类完成")
            # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  958.137281791
            # print(km.inertia_)
        except:
            logging.error(traceback.format_exc())
            return False, "process fail"
# 类似于主函数
if __name__ == "__main__":
    # 获取TextProcess对象
    tc = TextCluster()
    tc.process("input1.txt", "tf_Result.txt", "tfidf_Result.txt", 3)