#!/usr/bin/python3
import pymysql
# 打开数据库连接
db = pymysql.connect(host='192.168.192.10',
                     user='root',
                     password='123456',
                     database='test')
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
# 使用 execute()  方法执行 SQL 查询 
#cursor.execute("SELECT count(1) from BOOK")
 
# 使用 fetchone() 方法获取单条数据.
#data = cursor.fetchone()
 
#print ("BOOK count: %s " % data)
 
# 使用 execute() 方法执行 SQL，如果表存在则删除
#cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
 
# 使用预处理语句创建表
#sql = """CREATE TABLE BOOK (
#         TITIE  CHAR(50) NOT NULL)"""
 
#cursor.execute(sql)
 
# SQL 插入语句
sql = "INSERT INTO BOOK(TITLE) VALUES ('flower')" 
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
