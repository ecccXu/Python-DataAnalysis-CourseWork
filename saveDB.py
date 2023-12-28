""" 保存sql表 """
import pandas as pd
from sqlalchemy import create_engine
# 链接mysql
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_USER = 'root'
MYSQL_PASSWORD = "123456"
MYSQL_DB = 'mysql'
engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB))
# 读取movies
Movie = pd.read_sql('select * from movies', engine)
Types = pd.read_sql('select * from movietype', engine)
def saveDB():
    # 存储movies
    Movie.to_csv("moviesInfo.csv")
    Types.to_csv("movieTypes.csv")
if __name__ == '__main__':
    saveDB()