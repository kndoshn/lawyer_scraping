import scrapy


class ListSpider(scrapy.Spider):
    name = "list"
    all_numbers = []

    def start_requests(self):
        urls = [
            'https://www.nichibenren.jp/member_general/lawyer/lawyerSearchResultsList/goToPage?page=',
        ] * 10

        for i, value in enumerate(urls):
            url = value + str(i+1)
            yield scrapy.Request(
                url=url,
                method='POST',
                headers = {
                    'Cookie:': 'JSESSIONID=3256340A8CB52AFED780B678EE07F6EC',
                },
                callback=self.parse
            )

    def parse(self, response):
        xpath = '/html/body/div[@class="container"]/div[@id="wrapper"]/div[@class="mainCont"]/form[@id="form1"]/table[@class="table table-bordered table-striped tableFix"]/tbody/tr/td[2]/a/span/text()'
        numbers = response.xpath(xpath).extract()
        self.all_numbers = self.all_numbers + numbers

    def closed(self, reason):
        self.all_numbers = set(self.all_numbers)
        self.log(self.all_numbers)
