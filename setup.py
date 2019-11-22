import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='Cloud',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
