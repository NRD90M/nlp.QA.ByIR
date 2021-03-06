#coding:utf8

import sys
# print >> sys.stderr, 'baike.py', sys.path

from backend.SearchEngineCrawler.common_tools import html_tools as To
from backend.utils import TextProcess as T
from .baidu import BaiduEngine
import os

class BaiKe(BaiduEngine):
    """
    百度百科内容抓取
    """
    def __init__(self):
        self.query = super().__init__().query
        self.url = "http://baike.baidu.com/item/"

    def get_info(self,basicInfo_block):
        info = {}
        # basicInfo_left = basicInfo_block.contents[1]
        # basicInfo_right = basicInfo_block.contents[2]
        for bI_LR in basicInfo_block.contents[1:3]:
            for bI in bI_LR:
                if bI.name == None:
                    continue
                # print bI.name
                # print bI.string
                if bI.name == 'dt':
                    tempName = ''
                    for bi in bI.contents:
                        tempName += bi.string.strip().replace(u" ",u"")
                elif bI.name == 'dd':
                    # print bI.contents
                    info[tempName] = bI.contents
        return info

    def ptr_Info(self,info):
        for i in info:
            attr_name = i.encode('utf8').replace(" ","")
            attr_value = str(info[i])
            print('属性名=  ' + attr_name)
            print('属性值=  ' + attr_value)


    '''
    根据实体和属性查询百科列表中的属性值
    '''
    def query(self,entity,attr):
        soup = To.get_html_baidu(self.url + entity)
        basicInfo_block = soup.find(class_= 'basic-info cmn-clearfix')
        if basicInfo_block == None:
            # print 'info None'
            return attr + "::找不到"
        else:
            info = get_info(basicInfo_block)
            # for i in info:
            #     print i
            #     print info[i]
            # print '-----------'
            #if info.has_key(attr.decode('utf8')):
            if attr.decode('utf8') in info:
                # print 'has key'+attr.decode('utf8')
                return info[attr.decode('utf8')]
            else:
                # print 'no key 进行同义词判断'
                # 同义词判断
                attr_list = T.load_baikeattr_name(os.path.dirname(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))+'/resources/Attribute_name.txt')
                attr = T.load_synonyms_word_inattr(attr,os.path.dirname(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))+'/resources/SynonDic.txt',attr_list)
                # if info.has_key(attr.decode('utf8')):
                if attr.decode('utf8') in info:
                    return info[attr.decode('utf8')]
                else:
                    return attr + "::找不到"

