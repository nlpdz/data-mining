# encoding:utf-8
import json

def loadFont():
    with open("data_valid.json", encoding='utf-8') as f:
        for line in f:
            text = json.loads(line)
            accusation = text['meta']['accusation']
            # print(type(accusation))

            if len(accusation) == 1 and "污染环境" in accusation:
                with open("data_valid1.txt", "a", encoding='utf-8') as ff:
                    ff.write("污染环境"+":"+text['fact']+"\n")


t = loadFont()



