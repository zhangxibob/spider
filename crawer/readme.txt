1、安装依赖包
pip install jieba numpy pandas matplotlib bs4 wordcloud -i https://pypi.douban.com/simple

2、安装其他系统依赖包
yum install -y libjpeg-turbo-devel freetype-devel

3、停用词
通用中文stopwords.txt 已经下载

4、词云字体
下载中文字体simfang.ttf，放到 /usr/share/fonts默认目录下
wordcloud=WordCloud(font_path="simfang.ttf",background_color="white",max_font_size=80,width=1400, height=1400, margin=2)

5、保存图片
plt.savefig('savefig_movie.png')