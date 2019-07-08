import scrapy


class ListSpider(scrapy.Spider):
    name = "list"

    def start_requests(self):
        urls = [
            'https://www.nichibenren.jp/member_general/lawyer/lawyerSearchResultsList/goToPage',
        ]

        for url in urls:
            yield scrapy.Request(
                url=url,
                method='POST',
                headers = {
                    'Cookie:': 'JSESSIONID=3256340A8CB52AFED780B678EE07F6EC',
                },
                body='page=1',
                callback=self.parse
            )

    def parse(self, response):
        xpath = '/html/body/div[@class="container"]/div[@id="wrapper"]/div[@class="mainCont"]/form[@id="form1"]/table[@class="table table-bordered table-striped tableFix"]/tbody'
        self.log(response.xpath(xpath).extract())
