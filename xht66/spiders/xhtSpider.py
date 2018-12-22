# coding:utf-8
import requests
import logging

import scrapy
from scrapy.spiders import CrawlSpider
from xht66.items import Xht66Item
import pymysql


class FilmInfo(object):
    douban = '-1'
    file_format = '未知'
    duration = '未知'
    film_translated_name = '未知'
    film_name = '未知'
    place = '未知'
    language = '未知'
    release_date = '未知'
    release_year = '9999'
    director = '9999'
    actor = '9999'
    imdb = '-1'
    pass

    @staticmethod
    def getFieldValue(result):
        arr = result.split("◎")
        filmInfo = FilmInfo()
        filmInfo.download_url = arr[0]
        for item in arr:
            item = item.replace("\u3000", "").replace("'","").replace("\xa0","")
            if item.startswith("译名"):
                filmInfo.film_translated_name = item.replace("译名", "")
            elif item.startswith("片名"):
                filmInfo.film_name = item.replace("片名", "")
            elif item.startswith("年代"):
                filmInfo.release_year = item.replace("年代", "")
            elif item.startswith("产地"):
                filmInfo.place = item.replace("产地", "")
            # elif item.find("类别"):
            #     filmInfo.film_en_name = item.replace("类别", "")
            elif item.startswith("语言"):
                filmInfo.language = item.replace("语言", "")
            # elif item.find("字幕"):
            #     filmInfo.film_en_name = item.replace("字幕", "")
            elif item.startswith("上映日期"):
                filmInfo.release_date = item.replace("上映日期", "")
            elif item.startswith("IMDb"):
                replace = item.replace("IMDb评分", "")
                find = replace.find("/")
                filmInfo.imdb = replace[0:find]
            elif item.startswith("豆瓣评分"):
                replace = item.replace("豆瓣评分", "")
                find = replace.find("/")
                filmInfo.douban = replace[0:find]
            elif item.startswith("文件格式"):
                filmInfo.file_format = item.replace("文件格式", "")
            # elif item.find("视频尺寸"):
            #     filmInfo.duration = item.replace("视频尺寸", "")
            elif item.startswith("片长"):
                filmInfo.duration = item.replace("片长", "")
            elif item.startswith("导演"):
                filmInfo.director = item.replace("导演", "")
            elif item.startswith("主演"):
                filmInfo.actor = item.replace("主演", "")
        return filmInfo


class Spider(CrawlSpider):
    name = 'xhtSpider'
    url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_'
    BASE_URL = 'https://www.dytt8.net'
    offset = 56
    singleOffset = 1
    start_urls = [url + str(offset) + ".html"]

    def parse(self, response):
        xpath = list(response.xpath("//a[@class='ulink']"))
        for each in xpath:
            # 初始化模型对象
            # item = Xht66Item()
            print('item')
            # print(xpath)
            paths = each.xpath("//a/@href").extract()
            # item['name'] = each.xpath("./img/@alt").extract()[0]
            index = paths[::-1].index('/html/gndy/dyzz/index.html')
            # print(index)
            length = len(paths)
            for i in range(index, length):
                # print(i)
                path = paths[i]
                # print(path)
                if path.find('dyzz') > -1 and path.find('index') == -1:
                    # print(path)
                    # item['link'] = path;
                    # yield item
                    yield scrapy.Request(self.BASE_URL + path, callback=self.parsePage)
            # print(item['link'][-(len(item['link'])-index)])
            # yield item

        # print(len(xpath))
        # print(xpath)
        if len(xpath) == 0:
            if self.offset < 185:
                self.offset += 1
                self.singleOffset = 1
            yield scrapy.Request(self.url + str(self.offset) + ".html", callback=self.parse)
        else:
            self.singleOffset += 1
            yield scrapy.Request(
                self.url + str(self.offset) + "_" + str(self.singleOffset) + ".html",
                callback=self.parse)

            # 每次处理完一页的数据之后，重新发送下一页页面请求
            # self.offset自增10，同时拼接为新的url，并调用回调函数self.parse处理Response
            # yield scrapy.Request(self.url + str(self.offset) + ".html", callback=self.parse)

    def parsePage(self, response):
        xpath = response.xpath('//div[@id="Zoom"]').extract()
        hrefs = response.xpath('//a/@href').extract()
        # print('xpath')
        # print(tds)
        # print(xpath)
        result = ""
        arr = xpath[0].split('<br>')
        for item in hrefs:
            if item.find("ftp") > -1:
                # print(item)
                result += item
        for item in arr:
            # if item.find('<a href') > -1:
            # print('<a href')
            # print(item)
            if item.find("◎") > -1:
                # print("◎")
                # print(item)
                result += item
        self.save2Sql(result)

    @staticmethod
    def prn_obj(obj):
        # print('\n输出对象：'.join(['%s:%s' % item for item in obj.__dict__.items()]))
        print(['%s:%s' % item for item in obj.__dict__.items()])

    def save2Sql(self, item):
        db = pymysql.connect("127.0.0.1", "root", "root", "dytt")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        filmInfo = FilmInfo.getFieldValue(item)
        # self.prn_obj(filmInfo)
        # self.getFieldValue(item)
        # SQL 插入语句
        # arr=self.getFieldValue(item)
        # print(len(arr))
        sql = "INSERT INTO film_info \
                (download_url,film_translated_name,film_name,release_year,place,language,release_date,imdb,douban,file_format,duration,director,actor) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
              (filmInfo.download_url, filmInfo.film_translated_name, filmInfo.film_name,filmInfo.release_year,filmInfo.place, filmInfo.language, filmInfo.release_date, filmInfo.imdb, filmInfo.douban, filmInfo.file_format, filmInfo.duration, filmInfo.director, filmInfo.actor)
        try:
            cursor. execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            db.rollback()
        db.close()
