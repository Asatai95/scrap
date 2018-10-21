from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector

from setting import *

from HelloScrapy.items import PageInfoItem

class HelloSpider(CrawlSpider):
    # scrapyをCLIから実行するときの識別子
    name = 'hello'
    # spiderに探査を許可するドメイン
    allowed_domains = ["www.example.com"]
    # 起点(探査を開始する)URL
    start_urls = ["http://www.example.com"]
    # LinkExtractorの引数で特定のルール(例えばURLにnewを含むページのみスクレイプするなど)を指定可能だが、今回は全てのページを対象とするため引数はなし
    # Ruleにマッチしたページをダウンロードすると、callbackに指定した関数が呼ばれる
    # followをTrueにすると、再帰的に探査を行う
    rules = [Rule(LinkExtractor(), callback='parse_pageinfo', follow=True)]

    def parse_pageinfo(self, response):
        sel = Selector(response)
        item = PageInfoItem()
        item['URL'] = response.url
        # ページのどの部分をスクレイプするかを指定
        # xPath形式での指定に加え、CSS形式での指定も可能
        item['title'] = sel.xpath('/html/head/title/text()').extract()
        return item
