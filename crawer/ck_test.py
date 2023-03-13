from clickhouse_driver import Client

client = Client(host='localhost', port=None, database='default', user='default', password='123456')
table = client.execute('show tables')
print(table)
#client.execute('CREATE TABLE book_test (title String) ENGINE = Memory')

client.execute('INSERT INTO book_test (title) VALUES', [['花']])
