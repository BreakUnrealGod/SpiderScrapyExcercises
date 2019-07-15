# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dushuProject.items import DushuprojectItem

class DushuSpider(CrawlSpider):
    name = 'dushu'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/1181.html']

    rules = (
        # allow 使用正则匹配链接，提取
        # restrict_xpaths 使用xpath路径提取，注意不用写到a标签，只需定位到a标签上一层即可
        # callback 是一个字符串，不是self.parse
        # follow 是否进一步提取链接中的链接
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]'), callback='parse_item', follow=False),
        # 【注意】请求的回调是这样写的
        # scrapy.Request(url = "www.baiud.com", callback=self.parse_item)
    )

    def parse_item(self, response):
        # 查看当前被下载器处理下载任务的url都是哪些
        # print(response.url)
        # aNodeList是一个SelectorList
        aNodeList = response.xpath('//div[@class="bookslist"]//li/div[@class="book-info"]/h3/a')
        # 获取每一页书的信息（书名、二级界面链接）
        for aNode in aNodeList:
            detailUrl = "https://www.dushu.com" + aNode.xpath('./@href').extract_first()
            title = aNode.xpath('./text()').extract_first()
            # 请求详情页信息
            yield scrapy.Request(detailUrl, callback=self.parse_detail, meta={"title": title})

    # 解析详情页数据据
    def parse_detail(self, response):
        # 将完整信息打包传给管道
        yield DushuprojectItem({
            "title": response.meta['title'],
            "price": response.xpath('//p[@class="price"]//span/text()').extract_first()
        })
