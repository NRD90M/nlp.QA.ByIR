#coding:utf8

# 分词模块后期替换为rises.seg

import jieba
import jieba.posseg as pseg
import os,sys
sys.path.append("..")

'''
initialize jieba Segment
'''
def jieba_initialize():
    # 这个写的也太耦合了吧，跟据不同的文件调用，有不同的path结果，但是resource的位置是固定的。
    # 主要问题在于使用的是__file__的参数，导致的问题。
    # 在原本的工程中，这个函数只在QA目录下的文件中被使用。
    jieba.load_userdict(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+'/resources/QAattrdic.txt')
    jieba.initialize()


'''
Segment words by jieba
'''
def wordSegment(text):
    text = text.strip()
    seg_list = jieba.cut(text)
    result = " ".join(seg_list)
    return result


'''
POS Tagging
'''
def postag(text):
    words = pseg.cut(text)
    # for w in words:
    #     print w.word, w.flag
    return words


'''
proecss xiaohuangji corpus
'''
def xiaohuangji_textprocess(fr_path,fw_path):
    fr = open(fr_path,'r')
    fw = open(fw_path,'a')
    line = fr.readline()
    i = 0

    while line:
        if line[0] == 'E':
            question = fr.readline()[2:].strip()
            answer = fr.readline()[2:]
            print(question)
            print(answer)
            if len(question)<20 and len(answer)<30:
                i +=1
                qa_pair = question+":::"+answer
                fw.write(qa_pair)
        line = fr.readline()

    fw.close()
    fr.close()
    print('Finished')

'''
q:::a text processing
'''
def tp2(fr_path,fw_path):
    fr = open(fr_path,'r')
    fw = open(fw_path,'a')
    line = fr.readline()
    while line:
        flag = 0
        words = pseg.cut(line)
        for w in words:
            print(w.word, w.flag)
            if w.flag == 'nr':
                flag = 1
        if flag == 0:
            fw.write(line)
        line = fr.readline()

    fw.close()
    fr.close()
    print('Finished')



'''
Load baike attributi name
'''
def load_baikeattr_name(attrdic):
    fr = open(attrdic,'r')
    attr = []
    line = fr.readline()
    while line:
        attr.append(line.strip())
        line = fr.readline()
    fr.close()
    return  attr

'''
Synonyms Analysis,return word in baike attr
word 原始词
synsdic 同义词典
attr 属性
'''
def load_synonyms_word_inattr(word,synsdic,attr):
    fr = open(synsdic,'r')
    tar_word = ''
    line = fr.readline().strip()
    while line:
        words = line.split(" ")
        if word in words:
            for w in words:
                if w in attr:
                  tar_word = w
                  break
        if tar_word != '':
            break
        line = fr.readline()
    fr.close()
    if tar_word == '':
        tar_word = 'Empty'
    return  tar_word


'''
对百度、Bing 的搜索摘要进行答案的检索
（需要加问句分类接口）
'''

def entity_extract_by_postag(words,pattern):
    """
    按照词性标注结果抽取实体,jieba分词和词性标注
    :param words: 分词列表
    :param pattern: 词性模式
    :return: 实体列表
    """
    keywords=[]
    for k in words:
        if k.flag.__contains__(pattern):
            keywords.append(k.word)
    return keywords

if __name__ == '__main__':
    pass
    # tp2('./corpus/xiaohuangji50w_clean2.txt','./corpus/xiaohuangji50w_clean3.txt')
    # postag("华中科技大学校长是谁？")
