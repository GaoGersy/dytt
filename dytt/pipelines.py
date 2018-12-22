# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import urllib
# import requests
#
# from gevent import os
# from scrapy.utils.project import get_project_settings
# from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.spiders import CrawlSpider

class Xht66Pipeline(CrawlSpider):
    name = 'pageSpider'
    # IMAGES_STORE = get_project_settings().get("IMAGES_STORE")
    url = 'https://www.dytt8.net'

    def parse(self, response):
        xpath = list(response.xpath("//div[@id='zoom']"))
        # for each in xpath:
            # 初始化模型对象
            # paths = each.xpath("//a/@href").extract()
            # print(item['link'][-(len(item['link'])-index)])
            # yield item
        print('xpath')
        print(xpath)
        yield scrapy.Request(self.url);
    def process_item(self, item, spider):
        print('Xht66Pipeline')
        print(item)
        print(spider)
        self.url=self.url+item['link'];
        # self.parse(self,item)
        # dirName = item['name']
        # arr = list(str(item['link']).split("/"))
        # imageName = arr[len(arr) - 1]
        # path = self.IMAGES_STORE + "/" + dirName
        # isExists = os.path.exists(path)
        # if not isExists:
        #     os.makedirs(path)
        # absoluteSrc= item['link']
        # file_name="%s/%s"%(dirName,imageName)
        # file_path=os.path.join(self.IMAGES_STORE,file_name)
        # print(absoluteSrc)
        # print(file_path)
        # # urllib.request.urlretrieve(absoluteSrc,file_path)
        # # f = open(file_path, 'wb')
        # # f.write((urllib.request.urlopen(absoluteSrc)).read())
        # # f.close()
        # try:
        #     ir = requests.get(absoluteSrc, timeout=3)
        #     print(ir.status_code)
        #     if ir.status_code == 200:
        #         open(file_path, 'wb').write(ir.content)
        # except requests.exceptions.ConnectTimeout:
        #     NETWORK_STATUS = False
        #
        # return item

        # def get_media_requests(self, item, info):
        #     image_url = item["link"]
        #     print(image_url)
        #     yield scrapy.Request(image_url)
        #
        # def item_completed(self, result, item, info):
        #     image_path = [x["path"] for ok, x in result if ok]
        #     print(image_path[0])
        #     dirName = item['name']
        #     arr = list(str(item['link']).split("/"))
        #     imageName = arr[len(arr) - 1]
        #     path = self.IMAGES_STORE + "/" + dirName
        #     isExists = os.path.exists(path)
        #     if not isExists:
        #         os.makedirs(path)
        #     os.rename(self.IMAGES_STORE + "/" + image_path[0], path + "/" + imageName)
        #
        #     item["imagePath"] = self.IMAGES_STORE + "/" + item["name"]
        #
        #     return item
