# -*- coding: utf-8 -*-
"""
    scrapy初始Url的两种写法，
    一种是常量start_urls，并且需要定义一个方法parse（）
    另一种是直接定义一个方法：star_requests()
"""
import scrapy


class mingyan(scrapy.Spider):
    name = "list_spider"
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn']

    def parse(self, response):
        mingyan = response.css('div.quote')

        for i in mingyan:
            text1 = i.css('.text::text').extract_first()  # 提取标题
            autor = i.css('.author::text').extract_first()  # 提取作者
            tags = i.css('.tags .tag::text').extract()  # 提取盘条价格
            tags = ','.join(tags)  # 数组转换为字符串

            fileName = '%s.txt' % autor  # 爬取的内容存入文件，文件名为：作者-语录.txt
            with open(fileName, 'a') as f:
                f = open(fileName, "a+")  # 追加写入文件
                f.write(text1)  # 写入名言内容
                f.write('\n')  # 换行
                f.write('作者：' + autor)  # 写入标签
                f.write('\n')  # 换行
                f.write('标签：' + tags)  # 写入标签
                # f.close()  # 关闭文件操作

        next_page = response.css('li.next a::attr(href)').extract_first()  # css选择器提取下一页链接

        if next_page is not None:  # 判断是否存在下一页

            """
             如果是相对路径，如：/page/1
             urljoin能替我们转换为绝对路径，也就是加上我们的域名
             最终next_page为：http://lab.scrapyd.cn/page/2/

            """
            next_page = response.urljoin(next_page)

            """
            接下来就是爬取下一页或是内容页的秘诀所在：
            scrapy给我们提供了这么一个方法：scrapy.Request()
            这个方法还有许多参数，后面我们慢慢说，这里我们只使用了两个参数
            一个是：我们继续爬取的链接（next_page），这里是下一页链接，当然也可以是内容页
            另一个是：我们要把链接提交给哪一个函数(callback=self.parse)爬取，这里是parse函数，也就是本函数
            当然，我们也可以在下面另写一个函数，比如：内容页，专门处理内容页的数据
            经过这么一个函数，下一页链接又提交给了parse，那就可以不断的爬取了，直到不存在下一页

            """
            yield scrapy.Request(next_page, callback=self.parse)