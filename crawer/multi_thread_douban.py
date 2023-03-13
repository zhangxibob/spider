from atexit import register
from threading import Thread
import requests
from bs4 import BeautifulSoup
from time import ctime

import pymysql


def run():
    # 模拟浏览器访问网站服务器
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    # 分页查询访问服务器
    for start_num in range(0, 250, 25):
        response = requests.get("https://movie.douban.com/top250?start="+str(start_num)+"&filter=", headers=headers)
        # print(response.status_code)
        # print(response.text)
    
        # 获取返回页面内容
        html = response.text
        # 网页html格式
        soup = BeautifulSoup(html, "html.parser")
        # 查询span标签class类型为title的内容
        all_titles = soup.findAll("span", attrs={"class", "title"})
        # 遍历数组，找到题目的内容，并且不包含“/”
        for title in all_titles:
            title_str = title.string
            if "/" not in title_str:
                # 打开数据库连接
                db = pymysql.connect(host='192.168.192.10',
                     user='root',
                     password='123456',
                     database='test')
                # 使用cursor()方法获取操作游标 
                cursor = db.cursor()
 
                # SQL 插入语句
                sql = "INSERT INTO BOOK(TITLE) \
                VALUES ('%s')" % (str(title_str))
                print(sql)
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 执行sql语句
                    db.commit()
                except:
                # 发生错误时回滚
                    db.rollback()
 
                # 关闭数据库连接
                db.close()
                #print(title_str)
@register
def _atexit():
    print('all done at: ', ctime())

if __name__ == '__main__':
    print('At', ctime(), 'start')    
    Thread(target=run).start()
    #run()




