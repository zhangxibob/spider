1����װ������
pip install jieba numpy pandas matplotlib bs4 wordcloud -i https://pypi.douban.com/simple

2����װ����ϵͳ������
yum install -y libjpeg-turbo-devel freetype-devel

3��ͣ�ô�
ͨ������stopwords.txt �Ѿ�����

4����������
������������simfang.ttf���ŵ� /usr/share/fontsĬ��Ŀ¼��
wordcloud=WordCloud(font_path="simfang.ttf",background_color="white",max_font_size=80,width=1400, height=1400, margin=2)

5������ͼƬ
plt.savefig('savefig_movie.png')