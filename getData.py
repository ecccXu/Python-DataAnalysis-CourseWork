"""爬取豆瓣top250"""
import re
import pymysql
import requests
from bs4 import BeautifulSoup

def getDB():
    """链接数据库"""
    db = pymysql.connect(host='localhost', user='root', password="123456", database='mysql')
    return db
def Agent_info():
    """用于保存Cookie、url、user-agent信息"""
    headers = {
        'Cookie': 'bid=GLLctzwSij4; _pk_id.100001.4cf6=aa31c11de3623546.1694509694.; __yadk_uid=Ea8Jntv2V2ur3PunO1bmIaMYKrYr83hO; ll="108306"; _vwo_uuid_v2=DA8667D812586CFB22749BDFF8B94DB6D|572e268a0cf169b276c60aac3046f078; __utmc=30149280; __utmc=223695111; viewed="36145665"; __utma=30149280.999830536.1694509694.1703591079.1703595509.6; __utmz=30149280.1703595509.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.960270262.1694509694.1703591079.1703595510.6; __utmz=223695111.1703595510.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1703595510%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DzLdfOn8PaI-ch13luRbkcmUs9DBNB-AeraPIhFoO3lkHjhifQ6A6eSGP7Qu9Qj_qZI-i4uGTIZJhqRO-CKB2xq%26wd%3D%26eqid%3Dba79c11d001fae1d00000006658ab301%22%5D; _pk_ses.100001.4cf6=1; ap_v=0,6.0; douban-fav-remind=1; regpop=1; __utmb=30149280.3.10.1703595509; dbcl2="140454707:HW7ChACwyc0"; ck=2W1s; push_noty_num=0; push_doumail_num=0; frodotk_db="1c77fa24701474325567ee6d503d5c96"; __utmt=1; __utmb=223695111.13.10.1703595510',
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    return headers
# 获取到电影详情的url地址列表和电影的其他名字
def get_url(url):
    print("抓取网址：", url)
    headers = Agent_info()
    request = requests.get(url, headers=headers)  # 后一个headers是上面变量
    soup = BeautifulSoup(request.text, 'lxml')  # 转换获取页面的格式

    pic = soup.find_all(attrs={'class': 'pic'})
    film_urls = []  # 电影详情地址列表
    # 遍历
    for x in pic:
        href = x.a.get('href')
        film_urls.append(href)
    movie_list = []  # 获取电影的其他名字
    div_list = soup.find_all(attrs={'class': 'hd'})
    # 遍历
    for each in div_list:
        # 获取第一个斜杠后的其他名
        movie = each.a.contents[3].text.strip()  # 获取并去掉斜杠前的空格
        movie = movie[2]  # 去斜杠和斜杠后的空格
        movie_list.append(movie)

    return film_urls, movie_list  # 获取到每个电影详情的url地址
# 获取电影详情信息页面
def get_url_info(film_url, file_name_other, id):
    print("抓取网址：", film_url)
    headers = Agent_info()
    request = requests.get(film_url, headers=headers)  # 后一个headers是上面变量
    soup = BeautifulSoup(request.text, 'lxml')  # 转换获取页面的格式
    # 排名
    rank = soup.find(attrs={'class': 'top250-no'}).text.split('.')[1]
    # 电影名
    filmname = soup.find(attrs={'property': 'v:itemreviewed'}).text.split(' ')[0]
    # 导演
    director = soup.find(attrs={'id': 'info'}).text.split('\n')[1].split(':')[1].strip()
    # 编剧
    scriptwriter = soup.find(attrs={'id': 'info'}).text.split('\n')[2].split(':')[1].strip()
    # 主演
    actor = soup.find(attrs={'id': 'info'}).text.split('\n')[3].split(':')[1].strip()
    # 类型
    filmtype = soup.find(attrs={'id': 'info'}).text.split('\n')[4].split(':')[1].strip()
    types = filmtype.split("/")

    if soup.find(attrs={'id': 'info'}).text.split('\n')[5].split(':')[0] == '官方网站':
        # 制片国家/地区
        area = soup.find(attrs={'id': 'info'}).text.split('\n')[6].split(':')[1].strip()
        # 语言
        language = soup.find(attrs={'id': 'info'}).text.split('\n')[7].split(':')[1].strip()
        # 上映日期
        release_date = soup.find(attrs={'id': 'info'}).text.split('\n')[8].split(':')[1].split("(")[0].strip()
    else:
        # 制片国家/地区
        area = soup.find(attrs={'id': 'info'}).text.split('\n')[5].split(':')[1].strip()
        # 语言
        language = soup.find(attrs={'id': 'info'}).text.split('\n')[6].split(':')[1].strip()
        # 上映日期
        release_date = soup.find(attrs={'id': 'info'}).text.split('\n')[7].split(':')[1].split("(")[0].strip()
    # 片长
    runtime = soup.find(attrs={'property': 'v:runtime'}).text
    # 豆瓣评分(平均分)
    rating_num = soup.find(attrs={'property': 'v:average'}).text
    # 五星评分比例
    star5_rating_per = soup.find(attrs={'class': 'rating_per'}).text
    # 评价人数
    rating_people = soup.find(attrs={'property': 'v:votes'}).text
    # 剧情简介
    summary = soup.find(attrs={'property': 'v:summary'}).text
    summary = pymysql.converters.escape_str(summary)

    # 存到数据库
    sql = 'insert into movies(`film_name`,`director`,`scriptwriter`,`actor`,`filmtype`,`area`,`language`,`release_date`,`runtime`,`ranks`,`rating_num`,`star5_rating_per`,`rating_people`,`summary`,`file_name_other`,`links`) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");'.format(filmname, director, scriptwriter, actor, filmtype, area, language, release_date, runtime, rank, rating_num,star5_rating_per, rating_people, summary, file_name_other, film_url)
    db = getDB()
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        cursor.execute('insert into moviehash(`movieid`) values ("{}");'.format(id))
        for j in range(len(types)):
            cursor.execute('insert into movietype(`movieid`,`filmtype`) values ("{}","{}");'.format(id, types[j].strip()))
        db.commit()
    except Exception as e:
        print(e)  # 查看是否报错
        db.rollback()
    cursor.close()
    db.close()
if __name__ == '__main__':
    print("开始抓取")
    film_urls, movie_list = get_url("https://movie.douban.com/top250")
    db = getDB()
    cursor = db.cursor()
    for i in range(0, 250, 25):     # 翻页循环抓取
        film_urls, movie_list = get_url("https://movie.douban.com/top250?start="+str(i)+"&filter=")
        for film_url in range(len(film_urls)):
            id = re.search('\d\d+', film_urls[film_url]).group()  # 正则表达式
            # 增加已录入电影的判断
            sql = 'select movieid from moviehash where movieid="{}";'.format(id)
            cursor.execute(sql)
            data = cursor.fetchall()
            if not data:    # 未找到数据，执行以下语句爬取网页数据
                get_url_info(film_urls[film_url], movie_list, id)