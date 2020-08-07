import json

import scrapy

NUMOFCRAWLPAPERS=100

class CrawlvnExpressSpider(scrapy.Spider):
    num=1
    crawled_count=0
    name = 'CrawlVN_Express'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/thoi-su-p1','https://vnexpress.net/giai-tri','https://vnexpress.net/giao-duc']


    def parse(self, response):
        # links = response.css('ul.list-news.hidden a::attr(href)').getall()
        #for i in self.start_urls:
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_link)
    def parse_link(self,response):
        if CrawlvnExpressSpider.num < NUMOFCRAWLPAPERS :
            links = response.css('div.width_common h3.title-news a::attr(href)').getall()
            for i in links:

                self.logger.info('Crawling %s' + ' SO ' + str(CrawlvnExpressSpider.num), i)
                pagelink=response.urljoin(i)
                CrawlvnExpressSpider.num += 1
                yield scrapy.Request(url=pagelink, callback=self.parse_page)
            NEXT_PAGE= response.css('div.button-page a::attr(href)').getall()
            index=NEXT_PAGE.index('javascript:;')
            NEXT_PAGE=NEXT_PAGE[index+1]
            if NEXT_PAGE is not None:
                NEXT_PAGE = response.urljoin(NEXT_PAGE)
                yield scrapy.Request(url=NEXT_PAGE, callback=self.parse_link)

    def parse_page(self, response):
        self.logger.info("Parse PAGE")
        #f=open('/Users/user/Desktop/VNexpress/VNexpress/Out/Ketqua.txt','a+',encoding='utf8')
        time = response.css('span.date::text').get()
        #f.write('Time: '+time+'\n')
        title = response.css('h1.title-detail::text').get()
        #f.write('Title: '+title+'\n')
        description=response.css('p.description::text').get()
        #f.write('Description: '+description+'\n')
        article = response.css('article.fck_detail p.Normal::text').getall()
        #f.write('Noi dung: ')
        #for p in article:
            #f.write(p+'\n')
        author=response.css('p.author_mail strong::text').get(default='KhongTacGia')
        if author=='KhongTacGia':
            author=response.css('p.Normal strong::text')[-1].get()
        self.logger.info(author)
        #f.write('Tac gia: '+author+'\n')
        #response.css('meta[name="its_tag"]::attr(content)').getall()
        tag=response.xpath("//meta[@name='its_tag']/@content").get()
        # f.write('Tag: '+tag)
        self.crawled_count+=1
        self.crawler.stats.set_value('Crawled Count',self.crawled_count)
        yield  {
            'time': time,
            'title': title,
            'description':description,
            'article':article,
            'author':author,
            'tag':tag
        }
        #f.write(json.dumps(data,ensure_ascii=False))
        #f.write(data)




