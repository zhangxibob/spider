#coding:utf-8
__author__ = 'hang'

import warnings
warnings.filterwarnings("ignore")
import jieba    #分词包
import numpy    #numpy计算包
import codecs   #codecs提供的open方法来指定打开的文件的语言编码，它会在读取的时候自动转换为内部unicode
import re
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
# %matplotlib inline  (ipython中应用)
# from skimage import data
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud#词云包

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

class KetWord:
    def __init__(self,name,count):
        self.name =name
        self.count = count

    def __cmp__(self, other):

        if isinstance(KetWord,other):
            if self.count > other.count:
                return 1
            elif self.count < other.count:
                return -1
            else:
                return 0

    def __str__(self):
        return '[name='+ self.name +':count='+ str(self.count) +']'

#分析网页函数
def getNowPlayingMovie_list():
    url = "https://movie.douban.com/nowplaying/hangzhou/"
    ret = Request(url, headers=headers)
    resp = urlopen(ret)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    nowplaying_movie = soup.find_all('div', id='nowplaying')
    nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')
    nowplaying_list = []
    for item in nowplaying_movie_list:
        nowplaying_dict = {}
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowplaying_dict['name'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
    return nowplaying_list

#爬取评论函数
def getCommentsById(movieId, pageNum):
    eachCommentList = [];
    if pageNum>0:
        start = (pageNum-1) * 20
    else:
        return False
    requrl = 'https://movie.douban.com/subject/' + movieId + '/comments' +'?' +'start=' + str(start) + '&limit=20'
    ret = Request(requrl, headers=headers)
    resp = urlopen(ret)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    comment_div_lits = soup.find_all('div', class_='comment')
    for item in comment_div_lits:
        comment = item.find_all('span', class_="short")[0].string
        if comment is not None:
            eachCommentList.append(comment)
    return eachCommentList

def main():
    #循环获取第一个电影的前10页评论
    commentList = []
    NowPlayingMovie_list = getNowPlayingMovie_list()
    for i in range(3):
        num = i + 1
        commentList_temp = getCommentsById(NowPlayingMovie_list[4]['id'], num)
        commentList.append(commentList_temp)

    #将列表中的数据转换为字符串
    comments = ''
    for k in range(len(commentList)):
        comments = comments + (str(commentList[k])).strip()

    #使用正则表达式去除标点符号
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    cleaned_comments = ''.join(filterdata)

    #使用结巴分词进行中文分词
    segment = jieba.lcut(cleaned_comments)
    words_df=pd.DataFrame({'segment':segment})

    #去掉停用词
    stopwords=pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='gbk')#quoting=3全不引用
    words_df=words_df[~words_df.segment.isin(stopwords.stopword)]

    #统计词频
    words_stat=words_df.groupby(by=['segment'])['segment'].agg([("计数",numpy.size)])
    words_stat=words_stat.reset_index().sort_values(by=["计数"],ascending=False)

    #用词云进行显示
    # wordcloud=WordCloud(font_path="simhei.ttf",background_color="white",max_font_size=80)
    wordcloud=WordCloud(font_path="simfang.ttf",background_color="white",max_font_size=80,width=1400, height=1400, margin=2)
    word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}

    #利用字典存放
    word_frequence_list = {}

    for key in word_frequence:
        word_frequence_list[str(key)] = word_frequence[key]

    wordcloud=wordcloud.generate_from_frequencies(word_frequence_list)

    plt.imshow(wordcloud)
    #既然是IPython的内置magic函数，那么在Pycharm中是不会支持的。但是我们可以在matplotlib中的pyplot身上下功夫，pyplot不会不提供展示图像的功能。
    plt.colorbar()
    plt.savefig('savefig_movie.png')
    plt.show()

#主函数
main()