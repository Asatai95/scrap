from scrapy.item import Item, Field

class PageInfoItem(Item):
    URL = Field()
    title = Field()
    pass
